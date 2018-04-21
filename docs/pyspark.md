# PySpark Setup

## Overview

This documents my setup of PySpark on my machine. I am using Windows 10.

### Prerequisites

Python, Jupyter Notebook, and Java 8+ are needed. Downloading Anaconda will provide Python and Jupyter Notebook. 

### Downloads

I downloaded Spark 2.3.0 with package for Apache Hadoop 2.7 using this [link](https://spark.apache.org/downloads.html).

I also downloaded the winutils.exe file for Hadoop 2.7.1 using this [link](https://github.com/steveloughran/winutils/blob/master/hadoop-2.7.1/bin/winutils.exe). This will be saved in \bin folder of our Spark distribution as shown later.

### Shell Commands

Install findspark to be able to utilize/import PySpark.
```shell
python -m pip install findspark
```

Make a directory for extracting our spark distribution.
```shell
mkdir C:\opt\spark

mv C:\Users\Chris\Downloads\spark-2.3.0-bin-hadoop2.7.tgz C:\opt\spark\spark-2.3.0-bin-hadoop2.7.tgz 
```

### Unzip Spark Files 

I used [7-Zip](https://www.7-zip.org/download.html) to extract files. Do 7-zip > Extract Here on the tgz file and then the tar file.

### Move Winutils

```shell
mv C:\Users\Chris\Downloads\winutils.exe C:\opt\spark\spark-2.3.0-bin-hadoop2.7\bin\winutils.exe 
```

### Environment Variables

Set the below user environment variables.

```
SPARK_HOME C:\opt\spark\spark-2.3.0-bin-hadoop2.7
HADOOP_HOME C:\opt\spark\spark-2.3.0-bin-hadoop2.7
PYSPARK_DRIVER_PYTHON jupyter
PYSPARK_DRIVER_PYTHON_OPTS notebook
```

Add the below path to the user Path environment variable.
```C:\opt\spark\spark-2.3.0-bin-hadoop2.7\bin``` 

### Testing PySpark in Jupyter Notebook

Restart the terminal or open a new terminal then start juypter notebook. 

```shell
jupyter notebook
```

```python
import findspark
findspark.init()
```

```python
import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

df = spark.sql('''select 'spark' as hello ''')
df.show()
```

If this works then PySpark is working properly.

### References
- [Install PySpark Windows Jupyter](http://changhsinlee.com/install-pyspark-windows-jupyter/)
- [Install PySpark on Windows PySpark](https://medium.com/@GalarnykMichael/install-spark-on-windows-pyspark-4498a5d8d66c/)