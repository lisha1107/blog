Status: published
Date: 2019-12-20 11:30:37
Author: Benjamin Du
Slug: tips-on-pyspark
Title: Tips on PySpark
Category: Programming
Tags: programming, PySpark, Python, Spark, tips, HPC, high performance computing

**
Things on this page are fragmentary and immature notes/thoughts of the author.
It is not meant to readers but rather for convenient reference of the author and future improvement.
**

1. You can run PySpark interactively using the `pyspark` command
  and submit a PySpark job to the cluster using the `spark-submit` command.
	For more details, 
	please refer to
	[Launching Applications with spark-submit](https://spark.apache.org/docs/latest/submitting-applications.html#launching-applications-with-spark-submit).
    Below is an example of shell script for submitting a PySpark job using `spark-submit`.

        :::Bash
        #!/bin/bash

        /apache/spark2.3/bin/spark-submit \
                --files "file:///apache/hive/conf/hive-site.xml,file:///apache/hadoop/etc/hadoop/ssl-client.xml,file:///apache/hadoop/etc/hadoop/hdfs-site.xml,file:///apache/hadoop/etc/hadoop/core-site.xml,file:///apache/hadoop/etc/hadoop/federation-mapping.xml" \
                --master yarn \
                --deploy-mode cluster \
                --queue your_queue \
                --num-executors 200 \
                --executor-memory 10G \
                --driver-memory 15G \
                --executor-cores 4 \
                --conf spark.yarn.maxAppAttempts=2 \
                --conf spark.dynamicAllocation.enabled=true \
                --conf spark.dynamicAllocation.maxExecutors=1000 \
                --conf spark.network.timeout=300s \
                --conf spark.executor.memoryOverhead=2G \
                --conf spark.pyspark.driver.python=/usr/share/anaconda3/bin/python \
                --conf spark.pyspark.python=/usr/share/anaconda3/bin/python \
                /path/to/_pyspark.py

    And below is a simple example of `_pyspark.py`.

        :::Python
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.appName('Test PySpark').enableHiveSupport().getOrCreate()
        spark.sql('select * from some_table limit 5').write.mode('overwrite').parquet('output')

    Notice that I have prefixed an underscore to the name of the file.
    This is a simple but useful trick to avoid unintentional module conflictions in Python. 
    For example, 
    if you name your PySpark script `pyspark.py`,
    your PySpark application will fail to work 
    as your script `pyspark.py` is loaded as a module named `pyspark` 
    which hides the official `pyspark` module in Python.
    It is suggestion that adopt the trick of "prefixing an underscore to file names"
    when submitting a PySpark job.

2. PySpark does not support converting `$"col"` to a Column implicitly. 
    However, 
    the function `pyspark.sql.functions.col` works the same as in Spark.

## Dependencies

[PEX](https://github.com/pantsbuild/pex)
sounds like a good tool!

1. Create a directory named `lib`.

        :::bash
        mkdir lib

2. Install dependencies into the library.

        :::bash
        pip3 install -r requirements.txt -t lib

3. Zip the library.

        :::bash
        cd lib
        zip -r ../lib.zip .

4. Call `SparkContext.addPyFile` to add the zip file before using the packages/moduels.

        :::bash
        spark.sparkContext.addPyFile("/path/to/python/file")

Issues:

1. This approach works with only pure Python package.
    No dependecny on C/C++, Fortran is allowed.
    It is OK for a Python package to rely on JAR files.

2. No easy way to exclude dependencies.

3. Does wheel work or not with this approach?

## References

[Managing dependencies and artifacts in PySpark](https://bytes.grubhub.com/managing-dependencies-and-artifacts-in-pyspark-7641aa89ddb7)

https://stackoverflow.com/questions/51450462/pyspark-addpyfile-to-add-zip-of-py-files-but-module-still-not-found

https://becominghuman.ai/real-world-python-workloads-on-spark-standalone-clusters-2246346c7040

https://community.cloudera.com/t5/Community-Articles/Running-PySpark-with-Conda-Env/ta-p/247551

https://stackoverflow.com/questions/36461054/i-cant-seem-to-get-py-files-on-spark-to-work

[Best Practices Writing Production-Grade PySpark Jobs](https://developerzen.com/best-practices-writing-production-grade-pyspark-jobs-cb688ac4d20f)

[Packaging code with PEX — a PySpark example](https://medium.com/criteo-labs/packaging-code-with-pex-a-pyspark-example-9057f9f144f3)
