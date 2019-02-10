#!/usr/bin/env python3
# encoding: utf-8

import os
import os.path
import re
from argparse import ArgumentParser
import sqlite3
import hashlib
import datetime
import shutil
import json
from typing import Union, List

EN = 'en'
CN = 'cn'
HOME = 'home'
MISC = 'misc'
DECLARATION = '''
**
Things on this page are fragmentary and immature notes/thoughts of the author.
It is not meant to readers but rather for convenient reference of the author and future improvement.
**

'''
DASHES = '-' * 80
NOW_DASH = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TODAY_DASH = NOW_DASH[:10]
EDITOR = 'code'


def _update_post_move(post):
    """ Update the post after move.
    There are two possible change.
    First, the declaration might be added/removed depending on whether the post is moved to the misc sub blog directory.
    Second, the slug of the post is updated to match the path of the post.
    """
    # slug = 'Slug: ' + _slug(os.path.basename(post)[11:])
    if blog_dir(post) == MISC:
        with open(post, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()
        index = [line.strip() for line in lines].index('')
        with open(post, 'w', encoding='utf-8') as fout:
            fout.writelines(lines[:index])
            fout.writelines(DECLARATION)
            fout.writelines(lines[index:])
    else:
        with open(post, 'r', encoding='utf-8') as fin:
            text = fin.read()
        text = text.replace(DECLARATION, '')
        # text = re.sub('\nSlug: .*\n', slug, text)
        with open(post, 'w', encoding='utf-8') as fout:
            fout.write(text)


def _update_time(post):
    with open(post, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
    for i, line in enumerate(lines):
        if line.startswith('Date: '):
            lines[i] = f'Date: {NOW_DASH}\n'
            break
    with open(post, 'w') as fout:
        fout.writelines(lines)


def blog_dir(post: str):
    dir_ = os.path.dirname(post)
    dir_ = os.path.dirname(dir_)
    return os.path.basename(dir_)


def _slug(title: str):
    return title.replace(' ', '-').replace('/', '-')


def _format_title(title, file_words):
    with open(file_words, 'r', encoding='utf-8') as fin:
        words = json.load(fin)
    title = title.title()
    for word in words:
        title = title.replace(' ' + word[0] + ' ', ' ' + word[1] + ' ')
        if title.startswith(word[0] + ' '):
            title = title.replace(word[0] + ' ', word[1] + ' ')
        if title.endswith(' ' + word[0]):
            title = title.replace(' ' + word[0], ' ' + word[1])
    return title


def _fts_version():
    options = sqlite3.connect(':memory:').execute('pragma compile_options').fetchall()
    if ('ENABLE_FTS5',) in options:
        return 'fts5'
    return 'fts4'


class Blogger:

    def __init__(self, db: str = ''):
        """Create an instance of Blogger.

        :param dir_: the root directory of the blog.
        :param db: the path to the SQLite3 database file.
        """
        self._fts = _fts_version()
        self._db = db if db else os.path.join(os.path.expanduser('~'), '.blogger.sqlite3')
        self._conn = sqlite3.connect(self._db)
        self._create_vtable_posts()
        self.root_dir = self._root_dir()

    def _root_dir(self):
        sql = 'SELECT path FROM posts LIMIT 1'
        row = self._conn.execute(sql).fetchone()
        if row:
            dir_ = os.path.dirname(row[0])
            dir_ = os.path.dirname(dir_)
            return os.path.dirname(dir_)
        return ''

    def _create_vtable_posts(self):
        sql = f'''
        CREATE VIRTUAL TABLE IF NOT EXISTS posts USING {self._fts} (
            path, dir, status, date, author, slug, title, category, tags, content, md5sum, updated
        )
        '''
        self._conn.execute(sql)

    def _create_table_srps(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS srps (
            path, dir, status, date, author, slug, title, category, tags, content, md5sum, updated
        )
        '''
        self._conn.execute(sql)

    def commit(self):
        self._conn.commit()

    def update_category(self, post, category):
        with open(post, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()
        for i, line in enumerate(lines):
            if line.startswith('Category: '):
                lines[i] = f'Category: {category}\n'
                break
        with open(post, 'w') as fout:
            fout.writelines(lines)
        sql = 'UPDATE posts SET category = ? WHERE path = ?'
        self._conn.execute(sql, [category, post])

    def update_tags(self, post, from_tag, to_tag):
        with open(post, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()
        for i, line in enumerate(lines):
            if line.startswith('Tags: '):
                tags = (tag.strip() for tag in line[5:].split(','))
                tags = (to_tag if tag == from_tag else tag for tag in tags)
                lines[i] = 'Tags: ' + ', '.join(tags)
                break
        with open(post, 'w') as fout:
            fout.writelines(lines)
        sql = 'UPDATE posts SET tags = ? WHERE path = ?'
        self._conn.execute(sql, [tags + ',', post])

    def reload_posts(self, root_dir: str, md5: str, updated: int):
        self._create_vtable_posts()
        self._conn.execute('DELETE FROM posts')
        for dir_ in (HOME, CN, EN, MISC):
            self._load_posts(os.path.join(root_dir, dir_, 'content'), md5, updated)
        self._conn.commit()
        self.root_dir = self._root_dir()

    def _load_posts(self, post_dir, md5, updated):
        if not os.path.isdir(post_dir):
            return
        for post in os.listdir(post_dir):
            if post.endswith('.markdown'):
                post = os.path.join(post_dir, post)
                self._load_post(post, md5, updated)

    def _load_post(self, post, md5, updated):
        with open(post, 'r') as fin:
            lines = fin.readlines()
        for index, line in enumerate(lines):
            if not re.match('[A-Za-z]+: ', line):
                break
        # parse meta data 0 - index (exclusive)
        status = ''
        date = ''
        author = ''
        slug = ''
        title = ''
        category = ''
        tags = ''
        for i in range(0, index):
            line = lines[i]
            if line.startswith('Status: '):
                status = line[8:].strip()
            elif line.startswith('Date: '):
                date = line[6:].strip()
            elif line.startswith('Author: '):
                author = line[8:].strip()
            elif line.startswith('Slug: '):
                slug = line[6:].strip()
            elif line.startswith('Title: '):
                title = line[7:].strip()
            elif line.startswith('Category: '):
                category = line[10:].strip()
            elif line.startswith('Tags: '):
                tags = line[6:].strip()
                if not tags.endswith(','):
                    tags = tags + ','
        # parse content index to end
        content = ''.join(lines[index:])
        sql = '''
        INSERT INTO posts (
            path, dir, status, date, author, slug, title, category, tags, content, md5sum, updated
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        '''
        self._conn.execute(sql, [
            post, 
            blog_dir(post), 
            status, 
            date, 
            author, 
            slug, 
            title, 
            category, 
            tags, 
            content,
            md5,
            updated,
        ])

    def delete(self, post: Union[str, List[str]]):
        if isinstance(post, str):
            post = [post]
        for file in post:
            os.remove(file)
        qmark = ', '.join(['?'] * len(post))
        sql = f'DELETE FROM posts WHERE path in ({qmark})'
        self._conn.execute(sql, post)
        self._conn.commit()

    def move(self, post, target):
        if target in (EN, CN, MISC):
            target = os.path.join(self.root_dir, target, 'content', os.path.basename(post))
        if post == target:
            return
        shutil.move(post, target)
        _update_post_move(target)
        sql = 'UPDATE posts SET path = ?, dir = ? WHERE path = ?'
        self._conn.execute(sql, [target, blog_dir(target), post])

    def _check_update_time(self, post):
        with open(post, 'r', encoding='utf-8') as f:
            hash1 = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        if hash1 != hash0:
            _update_time(post)

    def edit(self, post, editor):
        with open(post, 'r', encoding='utf-8') as f:
            md5 = hashlib.md5(f.read().encode('utf-8')).hexdigest()
        sql = 'UPDATE posts SET md5sum = ?, updated = 1 WHERE path = ?'
        self._conn.execute(sql, [md5, post])
        os.system(f'{editor} "{post}"')
        # todo: the logic here doesn't seem right to me ...
        # better to use a upsert statement
        # sql = 'DELETE FROM posts WHERE path = ?'
        # self._conn.execute(sql, [post])
        # self._load_post(post)
        # self._conn.commit()

    def _create_post(self, post, title):
        file_words = os.path.join(self.root_dir, 'words.json')
        with open(post, 'w', encoding='utf-8') as fout:
            fout.writelines('Status: published\n')
            fout.writelines(f'Date: {NOW_DASH}\n')
            fout.writelines('Author: Benjamin Du\n')
            fout.writelines('Slug: {}\n'.format(title.replace(' ', '-').replace('/', '-')))
            fout.writelines(f'Title: {_format_title(title, file_words)}\n')
            fout.writelines('Category: Programming\n')
            fout.writelines('Tags: programming\n')
            if blog_dir(post) == MISC:
                    fout.writelines(DECLARATION)

    def add(self, title, dir_) -> str:
        file = self.find_post(title, dir_)
        if not file:
            file = f'{TODAY_DASH}-{_slug(title)}.markdown'
            file = os.path.join(self.root_dir, dir_, 'content', file)
            self._create_post(file, title)
        # todo: similar to edit time update, do it later
        # self._load_post(file, '', 0)
        # sql = 'DELETE FROM srps'
        # self._conn.execute(sql)
        # sql = 'INSERT INTO srps SELECT * FROM posts WHERE path = ?'
        # self._conn.execute(sql, [file])
        # self._conn.commit()
        return file

    def find_post(self, title, dir_):
        """Find existing post matching the given title.

        :return: Return the path of the existing post if any, otherwise return empty string.
        """
        # find all posts and get rid of leading dates
        sql = 'SELECT path FROM posts WHERE path LIKE ? AND dir = ?'
        row = self._conn.execute(sql, [f'%{_slug(title)}.markdown', dir_]).fetchone()
        if row:
            return row[0]
        return ''

    def search(self, phrase: str, filter_: str = '', dry_run=False):
        self._create_table_srps()
        self._conn.execute('DELETE FROM srps')
        conditions = []
        if phrase:
            conditions.append(f"posts MATCH '{phrase}'")
        if filter_:
            filter_ =  conditions.append(filter_)
        where = ' AND '.join(conditions)
        if where:
            where = 'WHERE ' + where
        sql = f'''
            INSERT INTO srps
            SELECT 
                * 
            FROM 
                posts 
            {where} 
            ORDER BY rank
            '''
        if args.dry_run:
            print(sql)
            return
        self._conn.execute(sql)
        self._conn.commit()

    def path(self, id_: Union[int, List[int]]):
        if isinstance(id_, int):
            id_ = [id_]
        qmark = ', '.join(['?'] * len(id_))
        sql = f'SELECT path FROM srps WHERE rowid in ({qmark})'
        return [row[0] for row in self._conn.execute(sql, id_).fetchall()]

    def fetch(self, n: int):
        sql = 'SELECT rowid, * FROM srps LIMIT {}'.format(n)
        return self._conn.execute(sql).fetchall()

    def query(self, sql: str):
        return self._conn.execute(sql).fetchall()

    def publish(self, dirs):
        """Publish the specified blog to GitHub.
        """
        for dir_ in dirs:
            self._publish(dir_)

    def _publish(self, dir_):
        # pelican
        os.system(f'cd "{os.path.join(self.root_dir, dir_)}" && pelican . -s pconf_sd.py')
        # git push
        os.system(f'cd "{self.root_dir}" && ./git.sh {dir_}')
        print('\n' + DASHES)
        print('Please consider COMMITTING THE SOURCE CODE as well!')
        print(DASHES + '\n')

    def tags(self, dir_: str = '', where=''):
        sql = 'SELECT tags FROM posts {where}'
        if where:
            sql = sql.format(where=where)
        else:
            # todo you can support quicker specific filtering in future
            sql = sql.format(where=where)
        cursor = self._conn.execute(sql)
        tags = {}
        row = cursor.fetchone()
        while row is not None:
            for tag in row[0].split(','):
                tag = tag.strip() 
                if tag == '':
                    continue
                if tag in tags:
                    tags[tag] += 1
                else:
                    tags[tag] = 1
            row = cursor.fetchone()
        return sorted(tags.items(), key=lambda pair: pair[1], reverse=True)

    def categories(self, dir_: str = '', where=''):
        sql = '''
            SELECT 
                category,
                count(*) as n
            FROM
                posts
            {where}
            GROUP BY
                category
            ORDER BY
                n desc
            '''
        if where:
            sql = sql.format(where=where)
        else:
            # todo you can support quicker specific filtering in future
            sql = sql.format(where=where)
        cats = (row for row in self._conn.execute(sql).fetchall())
        return cats


def query(blogger, args):
    rows = blogger.query(' '.join(args.sql))
    for row in rows:
        print(row)


def delete(blogger, args):
    if re.search('^d\d+$', args.sub_cmd):
        args.index = int(args.sub_cmd[1:])
    if args.index:
        args.file = blogger.path(args.index)
    if args.file:
        blogger.delete(args.file)


def move(blogger, args):
    if re.search('^m\d+$', args.sub_cmd):
        args.index = int(args.sub_cmd[1:])
    if args.index:
        args.file = blogger.path(args.index)[0]
    if args.file:
        blogger.move(args.file, args.target)
    blogger.commit()


def edit(blogger, args):
    if re.search('^e\d+$', args.sub_cmd):
        args.index = int(args.sub_cmd[1:])
    if args.index:
        args.file = blogger.path(args.index)[0]
    if args.file:
        if not shutil.which(args.editor):
            args.editor = 'vim'
        blogger.edit(args.file, args.editor)


def search(blogger, args):
    filter_ = []
    args.filter = ' '.join(args.filter)
    if args.filter:
        filter_.append(args.filter)
    if args.sub_dir:
        args.sub_dir = ', '.join(f"'{dir_}'" for dir_ in args.sub_dir)
        filter_.append(f'dir IN ({args.sub_dir})')
    if args.neg_sub_dir:
        args.neg_sub_dir = ', '.join(f"'{dir_}'" for dir_ in args.neg_sub_dir)
        filter_.append(f'dir NOT IN ({args.neg_sub_dir})')
    if args.categories:
        args.categories = ', '.join(f"'{cat}'" for cat in args.categories)
        filter_.append(f'category IN ({args.categories})')
    if args.neg_categories:
        args.neg_sub_dir = ', '.join(f"'{cat}'" for cat in args.neg_catgories)
        filter_.append(f'category NOT IN ({args.neg_categories})')
    if args.tags:
        args.tags = ''.join(f'% {tag},%' for tag in args.tags).replace('%%', '%')
        filter_.append(f"tags LIKE '{args.tags}'")
    if args.neg_tags:
        args.neg_tags = ''.join(f'% {tag},%' for tag in args.neg_tags).replace('%%', '%')
        filter_.append(f"tags NOT LIKE '{args.neg_tags}'")
    if args.status:
        args.status = ', '.join(f"'{stat}'" for stat in args.status)
        filter_.append(f'status IN ({args.status})')
    if args.neg_status:
        args.neg_status = ', '.join(f"'{stat}'" for stat in args.neg_status)
        filter_.append(f'status NOT IN ({args.neg_status})')
    args.author = ' '.join(args.author)
    if args.author:
        filter_.append(f"author = '{args.author}'")
    args.neg_author = ' '.join(args.neg_author)
    if args.neg_author:
        filter_.append(f"author != '{args.neg_author}'")
    args.title = ' '.join(args.title)
    if args.title:
        filter_.append(f"title LIKE '%{args.title}%'")
    args.neg_title = ' '.join(args.neg_title)
    if args.neg_title:
        filter_.append(f"title NOT LIKE '%{args.neg_title}%'")
    args.phrase = [token for token in args.phrase if token.lower() != 'the' and token.lower() != 'a']
    blogger.search(' '.join(args.phrase), ' AND '.join(filter_), args.dry_run)
    show(blogger, args)


def show(blogger, args):
    for row in blogger.fetch(args.n):
        print('{id}: {path}'.format(id=row[0], path=row[1]))


def reload(blogger, args):
    blogger.reload_posts(args.root_dir, '', 0)


def add(blogger, args):
    file = blogger.add(' '.join(args.title), args.sub_dir)
    args.index = None
    args.file = file
    edit(blogger, args)


def publish(blogger, args):
    blogger.publish(args.sub_dirs)


def categories(blogger, args):
    cats = blogger.categories(dir_=args.sub_dir, where=args.where)
    for cat in cats:
        print(cat)


def update_category(blogger, args):
    if re.search('^ucat\d+$', args.sub_cmd):
        args.indexes = int(args.sub_cmd[4:])
    if args.indexes:
        args.files = blogger.path(args.indexes)
    if args.files:
        for post in args.files:
            blogger.update_category(post, args.to_cat)
    elif args.from_cat:
        sql = 'SELECT path FROM posts WHERE category = ?'
        posts = (row[0] for row in blogger.query(sql))
        for post in posts:
            blogger.update_category(post, args.to_cat)
    blogger.commit()


def update_tags(blogger, args):
    if re.search('^utag\d+$', args.sub_cmd):
        args.indexes = int(args.sub_cmd[4:])
    if args.indexes:
        args.files = blogger.path(args.indexes)
    if args.files:
        for post in args.files:
            blogger.update_tags(post, args.from_tag, args.to_tag)
    else:
        sql = f'''
            SELECT 
                path 
            FROM 
                posts 
            WHERE 
                tags LIKE '%, {args.from_tag},%'
                OR tags LIKE '%: {args.from_tag},%'
            '''
        posts = (row[0] for row in blogger.query(sql))
        for post in posts:
            blogger.update_tags(post, args.from_tag, args.to_tag)
    blogger.commit()


def tags(blogger, args):
    tags = blogger.tags(dir_=args.sub_dir, where=args.where)
    for tag in tags:
        print(tag)


def parse_args(args=None, namespace=None):
    """Parse command-line arguments for the blogging util.
    """
    INDEXES = [''] + [str(i) for i in range(1, 11)]
    parser = ArgumentParser(
        description='Write blog in command line.')
    subparsers = parser.add_subparsers(dest='sub_cmd', help='Sub commands.')
    # parser for the update_tags command
    parser_utag = subparsers.add_parser('update_tags', aliases=['utag' + i for i in INDEXES], help='update tags of posts.')
    parser_utag.add_argument(
        '-i',
        '--indexes',
        nargs='+',
        dest='indexes',
        type=int,
        default=(),
        help='row IDs in the search results.')
    parser_utag.add_argument(
        '--files',
        nargs='+',
        dest='files',
        default=(),
        help='paths of the posts whose categories are to be updated.')
    parser_utag.add_argument(
        '-f',
        '--from-tag',
        dest='from_tag',
        default='',
        help='the tag to change from.')
    parser_utag.add_argument(
        '-t',
        '--to-tag',
        dest='to_tag',
        default='',
        help='the tag to change to.')
    parser_utag.set_defaults(func=update_tags)
    # parser for the update_category command
    parser_ucat = subparsers.add_parser('update_category', aliases=['ucat' + i for i in INDEXES], help='update category of posts.')
    parser_ucat.add_argument(
        '-i',
        '--indexes',
        nargs='+',
        dest='indexes',
        type=int,
        default=(),
        help='row IDs in the search results.')
    parser_ucat.add_argument(
        '--files',
        nargs='+',
        dest='files',
        default=(),
        help='paths of the posts whose categories are to be updated.')
    parser_ucat.add_argument(
        '-f',
        '--from-category',
        dest='from_cat',
        default='',
        help='the category to change from.')
    parser_ucat.add_argument(
        '-t',
        '--to-category',
        dest='to_cat',
        default='',
        help='the category to change to.')
    parser_ucat.set_defaults(func=update_category)
    # parser for the tags command
    parser_tags = subparsers.add_parser('tags', aliases=['t'], help='List all tags and their frequencies.')
    parser_tags.add_argument(
        '-w',
        '---where',
        dest='where',
        default='',
        help='A user-specified filtering condition.')
    parser_tags.add_argument(
        '-d',
        '---dir',
        dest='sub_dir',
        default='',
        help='The sub blog directory to list categories; by default list all categories.')
    parser_tags.set_defaults(func=tags)
    # parser for the categories command
    parser_cats = subparsers.add_parser('cats', aliases=['c'], help='List all categories and their frequencies.')
    parser_cats.add_argument(
        '-w',
        '---where',
        dest='where',
        default='',
        help='A user-specified filtering condition.')
    parser_cats.add_argument(
        '-d',
        '---dir',
        dest='sub_dir',
        default='',
        help='The sub blog directory to list categories; by default list all categories.')
    parser_cats.set_defaults(func=categories)
    # parser for the reload command
    parser_reload = subparsers.add_parser('reload', aliases=['r'], help='Reload information of posts.')
    parser_reload.add_argument(
        '-d',
        '--root-dir',
        dest='root_dir',
        default=os.getenv('blog_dir'),
        help='The root directory of the blog.')
    parser_reload.set_defaults(func=reload)
    # parser for the show command
    parser_list = subparsers.add_parser('list', aliases=['l'], help='List last search results.')
    parser_list.add_argument(
        '-n',
        dest='n',
        type=int,
        default=10,
        help='Number of matched records to show.')
    parser_list.set_defaults(func=show)
    # parser for the search command
    parser_search = subparsers.add_parser('search', aliases=['s'], 
        help='Search for posts. ' \
            'Tokens separated by spaces ( ) or plus signs (+) in the search phrase ' \
            'are matched in order with tokens in the text. ' \
            'ORDERLESS match of tokens can be achieved by separating them with the AND keyword. ' \
            'You can also limit match into specific columns. ' \
            'For more information, please refer to https://sqlite.org/fts5.html')
    parser_search.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        help='print out the SQL query without running it.')
    parser_search.add_argument(
        'phrase',
        nargs='+',
        default=(),
        help='the phrase to match in posts. ' \
            'Notice that tokens "a" and "the" are removed from phrase, ' \
            'which can be used as a hack way to make phrase optional. ' \
            'For example if you want to filter by category only without constraints on full-text search, ' \
            'you can use ./blog.py a -c some_category.')
    parser_search.add_argument(
        '-i',
        '--title',
        nargs='+',
        dest='title',
        default='',
        help='search for posts with the sepcified title.')
    parser_search.add_argument(
        '-I',
        '--neg-title',
        nargs='+',
        dest='neg_title',
        default='',
        help='search for posts without the sepcified title.')
    parser_search.add_argument(
        '-a',
        '--author',
        nargs='+',
        dest='author',
        default='',
        help='search for posts with the sepcified author.')
    parser_search.add_argument(
        '-A',
        '--neg-author',
        nargs='+',
        dest='neg_author',
        default='',
        help='search for posts without the sepcified author.')
    parser_search.add_argument(
        '-s',
        '--status',
        nargs='+',
        dest='status',
        default='',
        help='search for posts with the sepcified status.')
    parser_search.add_argument(
        '-S',
        '--neg-status',
        nargs='+',
        dest='neg_status',
        default='',
        help='search for posts without the sepcified status.')
    parser_search.add_argument(
        '-t',
        '--tags',
        nargs='+',
        dest='tags',
        default='',
        help='search for posts with the sepcified tags.')
    parser_search.add_argument(
        '-T',
        '--neg-tags',
        nargs='+',
        dest='neg_tags',
        default='',
        help='search for posts without the sepcified tags.')
    parser_search.add_argument(
        '-c',
        '--categories',
        nargs='+',
        dest='categories',
        default='',
        help='search for posts with the sepcified categories.')
    parser_search.add_argument(
        '-C',
        '--neg-categories',
        nargs='+',
        dest='neg_categories',
        default='',
        help='search for posts without the sepcified categories.')
    parser_search.add_argument(
        '-d',
        '--sub-dir',
        dest='sub_dir',
        nargs='+',
        default='',
        help='search for posts in the specified sub blog directory.')
    parser_search.add_argument(
        '-D',
        '--neg-sub-dir',
        dest='neg_sub_dir',
        nargs='+',
        default='',
        help='search for posts not in the specified sub blog directory.')
    parser_search.add_argument(
        '-f',
        '--filter',
        dest='filter',
        nargs='+',
        default=(),
        help='futher filtering conditions in addition to the full-text match.')
    parser_search.add_argument(
        '-n',
        dest='n',
        type=int,
        default=10,
        help='number of matched records to show.')
    parser_search.set_defaults(func=search)
    # parser for the add command
    parser_add = subparsers.add_parser('add', aliases=['a'], help='Add a new post.')
    parser_add.add_argument(
        '-v',
        '--vim',
        dest='editor',
        action='store_const',
        const='vim',
        default=EDITOR,
        help='edit the post using vim.')
    parser_add.add_argument(
        '-e',
        '--en',
        dest='sub_dir',
        action='store_const',
        const=EN,
        default=MISC,
        help='create a post in the en sub blog directory.')
    parser_add.add_argument(
        '-c',
        '--cn',
        dest='sub_dir',
        action='store_const',
        const=CN,
        help='create a post in the cn sub blog directory.')
    parser_add.add_argument(
        'title',
        nargs='+',
        help='title of the post to be created.')
    parser_add.set_defaults(func=add)
    # parser for the edit command
    parser_edit = subparsers.add_parser('edit', aliases=['e' + i for i in INDEXES], help='edit a post.')
    parser_edit.add_argument(
        '-v',
        '--vim',
        dest='editor',
        action='store_const',
        const='vim',
        default=EDITOR,
        help='edit the post using vim.')
    parser_edit.add_argument(
        '-i',
        '--index',
        dest='index',
        type=int,
        help='rowid in the search results.')
    parser_edit.add_argument(
        '-f',
        '--file',
        dest='file',
        help='path of the post to be edited.')
    parser_edit.set_defaults(func=edit)
    # parser for the move command
    parser_move = subparsers.add_parser('move', aliases=['m' + i for i in INDEXES], help='Move a post.')
    parser_move.add_argument(
        '-i',
        '--index',
        dest='index',
        type=int,
        help='rowid in the search results.')
    parser_move.add_argument(
        '-f',
        '--file',
        dest='file',
        help='path of the post to be moved.')
    parser_move.add_argument(
        '-t',
        '--target',
        dest='target',
        default=MISC,
        help='path of destination file')
    parser_move.add_argument(
        '-c',
        '--cn',
        dest='target',
        action='store_const',
        const=CN,
        help='move to the cn sub blog directory.')
    parser_move.add_argument(
        '-e',
        '--en',
        dest='target',
        action='store_const',
        const=EN,
        help='move to the en sub blog directory.')
    parser_move.add_argument(
        '-m',
        '--misc',
        dest='target',
        action='store_const',
        const=MISC,
        help='move to the misc sub blog directory.')
    parser_move.set_defaults(func=move)
    # parser for the publish command
    parser_publish = subparsers.add_parser('publish', aliases=['p'], help='Publish the blog.')
    parser_publish.add_argument(
        '-c',
        '--cn',
        dest='sub_dirs',
        action='append_const',
        const=CN,
        default=[HOME],
        help='add the cn sub blog directory into the publish list.')
    parser_publish.add_argument(
        '-e',
        '--en',
        dest='sub_dirs',
        action='append_const',
        const=EN,
        help='add the en sub blog directory into the publish list.')
    parser_publish.add_argument(
        '-m',
        '--misc',
        dest='sub_dirs',
        action='append_const',
        const=MISC,
        help='add the misc sub blog directory into the publish list.')
    parser_publish.set_defaults(func=publish)
    # parser for the remove command
    parser_delete = subparsers.add_parser('delete', aliases=['d' + i for i in INDEXES], help='Delete a post/page.')
    parser_delete.add_argument(
        '-i',
        '--index',
        dest='index',
        type=int,
        help='rowid of the file (in the search results) to delete.')
    parser_delete.add_argument(
        '-f',
        '--file',
        dest='file',
        help='path of the post to delete.')
    parser_delete.set_defaults(func=delete)
    # parser for the query command
    parser_query = subparsers.add_parser('query', aliases=['q'], help='Run a SQL query.')
    parser_query.add_argument(
        'sql',
        nargs='+',
        help='the SQL to run')
    parser_query.set_defaults(func=query)
    # parse and run
    return parser.parse_args(args=args, namespace=namespace)


if __name__ == '__main__':
    blogger = Blogger()
    args = parse_args()
    args.func(blogger, args)
