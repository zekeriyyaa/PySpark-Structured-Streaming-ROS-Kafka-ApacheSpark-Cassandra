## PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra

The purpose of this project is to demonstrate a structured streaming pipeline with Apache Spark. The process consists of given steps:

0. Installation Process
1. Prepare a robotic simulation environment to generate data to feed into the Kafka. 
2. Prepare Kafka and Zookeeper environment to store discrete data.
3. Prepare Cassandra environment to store analyzed data.
4. Prepare Apache Spark structured streaming pipeline, integrate with Kafka and Cassandra.
5. Result

<p align="center" width="100%">
    <img src="https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/dataPipeline.png"> 
</p>

### 0. Installation Processes
You are able to install all required components to realize this project using the given steps.

#### Installation of ROS and Turtlebot3
We won't address the whole installation process of ROS and Turtlebot3 but you can access all required info from [ROS & Turtlebot3 Installation](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup).

After all installations are completed, you can demo our robotic environment using the given commands:
```
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```
You should see a view like the one given below.
<p align="center" width="100%">
    <img src="https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/turtlebot3.png"> 
</p>

#### Installation of Kafka and Zookeeper
We won't address the whole installation process of Kafka and Zookeeper but you can access all required info from [Kafka & Zookeeper Installation](https://www.linode.com/docs/guides/how-to-install-apache-kafka-on-ubuntu/).

After all installations are completed, you can demo Kafka using the given commands:
```
# Change your path to Kafka folder and then run 
bin/zookeeper-server-start.sh config/zookeeper.properties

# Open second terminal and then run
bin/kafka-server-start.sh config/server.properties

# Create Kafka "demo" topic
bin/kafka-topics.sh --create --topic demo --partitions 1 --replication-factor 1 -bootstrap-server localhost:9092
```

Once you create "demo" topic, you can run [kafka-demo/producer.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/kafka-demo/producer.py) and [kafka-demo/consumer.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/kafka-demo/consumer.py) respectively to check your setup.
>:exclamation: If you haven't installed [kafka-python](https://kafka-python.readthedocs.io/en/master/), use the given command and then run given files.
```
pip install kafka-python
```
- producer.py
```python3
import time,json,random
from datetime import datetime
from data_generator import generate_message
from kafka import KafkaProducer

def serializer(message):
    return json.dumps(message).encode("utf-8")
    
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=serializer
)

if __name__=="__main__":
    while True:
        dummy_messages=generate_message()
        print(f"Producing message {datetime.now()} | Message = {str(dummy_messages)}")
        producer.send("demo",dummy_messages)
        time.sleep(2)
```
- consumer.py
```python3
import json
from kafka import KafkaConsumer

if __name__=="__main__":
    consumer=KafkaConsumer(
        "demo",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest"    )

    for msg in consumer:
        print(json.loads(msg.value))
```
You should see a view like the one given below after run the commands:
```
python3 producer.py
python3 consumer.py
```

<p align="center" width="100%">
    <img src="https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/kafka-demo.png"> 
</p>

#### Installation of Cassandra
We won't address the whole installation process of Cassandra but you can access all required info from [Cassandra Installation](https://phoenixnap.com/kb/install-cassandra-on-ubuntu).

After all installations are completed, you can demo Cassandra using *cqlsh*. You can check this [link](https://www.tutorialspoint.com/cassandra/index.htm).

#### Installation of Apache Spark
We won't address the whole installation process of Apache Spark but you can access all required info from [Apache Spark Installation](https://phoenixnap.com/kb/install-spark-on-ubuntu).

After all installations are completed, you can make a quick example like [here](https://spark.apache.org/docs/latest/streaming-programming-guide.html).


### 1. Prepare a robotic simulation environment
[ROS (Robot Operating System)](http://wiki.ros.org/) allows us to design a robotic environment. We will use [Turtlebot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/), a robot in [Gazebo](http://gazebosim.org/) simulation env, to generate data for our use case. Turtlebot3 publishes its data with ROS topics. Therefore, we will subscribe the topic and send data into Kafka.

#### Run the simulation environment and analysis the data we will use
Turtlebot3 publishes its odometry data with ROS "odom" topic. So, we can see the published data with the given command:
```
# run the simulation environment
roslaunch turtlebot3_gazebo turtlebot3_world.launch

# check the topic to see data
rostopic echo /odom
```
You should see a view like the one given below.
```
header: 
  seq: 10954
  stamp: 
    secs: 365
    nsecs: 483000000
  frame_id: "odom"
child_frame_id: "base_footprint"
pose: 
  pose: 
    position: 
      x: -2.000055643960576
      y: -0.4997879642933192
      z: -0.0010013932644100873
    orientation: 
      x: -1.3486164084605e-05
      y: 0.0038530870521455017
      z: 0.0016676819550213058
      w: 0.9999911861487526
  covariance: [1e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1e-05, 0.0, 0.0, 0.0, 0.0, 0.0,...
twist: 
  twist: 
    linear: 
      x: 5.8050405333644035e-08
      y: 7.749200305343809e-07
      z: 0.0
    angular: 
      x: 0.0
      y: 0.0
      z: 1.15143519181447e-05
  covariance: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,...
```
In this use case, we will just interest the given part of the data:
```
    position: 
      x: -2.000055643960576
      y: -0.4997879642933192
      z: -0.0010013932644100873
    orientation: 
      x: -1.3486164084605e-05
      y: 0.0038530870521455017
      z: 0.0016676819550213058
      w: 0.9999911861487526
```

### 2. Prepare Kafka and Zookeeper environment
The data produced by Turtlebot3 will stored into Kafka clusters. 

#### Prepare Kafka for Use Case
First of all, we will create a new Kafka topic namely *odometry* for ROS odom data using the given commands:
```
# Change your path to Kafka folder and then run 
bin/zookeeper-server-start.sh config/zookeeper.properties

# Open second terminal and then run
bin/kafka-server-start.sh config/server.properties

# Create Kafka "odometry" topic for ROS odom data
bin/kafka-topics.sh --create --topic odometry --partitions 1 --replication-factor 1 -bootstrap-server localhost:9092
```
Then we will write a ROS subscriber to listen to the data from Turtlebot3. Also, since we need to send data to Kafka, it is necessary to add a producer script in it. We will use [ros/publish2kafka.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/ros/publish2kafka.py) to do it. This script subscribes to the odom topic and sends the content of the topic to Kafka.
```python3
import rospy
from nav_msgs.msg import Odometry
import json
from datetime import datetime
from kafka import KafkaProducer

count = 0
def callback(msg):
    global count
    messages={
        "id":count,
        "posex":float("{0:.5f}".format(msg.pose.pose.position.x)),
        "posey":float("{0:.5f}".format(msg.pose.pose.position.y)),
        "posez":float("{0:.5f}".format(msg.pose.pose.position.z)),
        "orientx":float("{0:.5f}".format(msg.pose.pose.orientation.x)),
        "orienty":float("{0:.5f}".format(msg.pose.pose.orientation.y)),
        "orientz":float("{0:.5f}".format(msg.pose.pose.orientation.z)),
        "orientw":float("{0:.5f}".format(msg.pose.pose.orientation.w))
        }

    print(f"Producing message {datetime.now()} Message :\n {str(messages)}")
    producer.send("odometry",messages)
    count+=1

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda message: json.dumps(message).encode('utf-8')
)

if __name__=="__main__":

    rospy.init_node('odomSubscriber', anonymous=True)
    rospy.Subscriber('odom',Odometry,callback)
    rospy.spin()
```
You can use [ros/readFromKafka.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/ros/readFromKafka.py) to check the data is really reach Kafka while ROS and publish2kafka.py is running.
```python3
import json
from kafka import KafkaConsumer

if __name__=="__main__":

    consumer=KafkaConsumer(
        "odometry",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest"
    )

    for msg in consumer:
        print(json.loads(msg.value))
```
### 3. Prepare Cassandra environment

#### Prepare Cassandra for Use Case
Initially, we will create a *keyspace* and then a *topic* in it using given command:
```
# Open the cqlsh and then run the command to create 'ros' keyspace
cqlsh> CREATE KEYSPACE ros WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};

# Then, run the command to create 'odometry' topic in 'ros'
cqlsh> create table ros.odometry(
        id int primary key, 
        posex float,
        posey float,
        posez float,
        orientx float,
        orienty float,
        orientz float,
        orientw float);

# Check your setup is correct
cqlsh> DESCRIBE ros

#and
cqlsh> DESCRIBE ros.odometry
```
> :warning: **The content of topic has to be the same as Spark schema**: Be very careful here!

### 4. Prepare Apache Spark structured streaming pipeline
You are able to write analysis results to either console or Cassandra.
#### (First Way) Prepare Apache Spark Structured Streaming Pipeline Kafka to Cassandra
We will write streaming script that read *odometry* topic from Kafka, analyze it and then write results to Cassandra. We will use [spark-demo/streamingKafka2Cassandra.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/spark-demo/streamingKafka2Cassandra.py) to do it.

First of all, we create a schema same as we already defined in Cassandra.
> :warning: **The content of schema has to be the same as Casssandra table**: Be very careful here!

```python3
odometrySchema = StructType([
                StructField("id",IntegerType(),False),
                StructField("posex",FloatType(),False),
                StructField("posey",FloatType(),False),
                StructField("posez",FloatType(),False),
                StructField("orientx",FloatType(),False),
                StructField("orienty",FloatType(),False),
                StructField("orientz",FloatType(),False),
                StructField("orientw",FloatType(),False)
            ])
```
Then, we create a Spark Session using two packages:
- **for spark kafka connector**     : org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0
- **for spark cassandra connector** : com.datastax.spark:spark-cassandra-connector_2.12:3.0.0
```python3
spark = SparkSession \
    .builder \
    .appName("SparkStructuredStreaming") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0") \
    .getOrCreate()
```
> :warning: **If you use spark-submit you can specify the packages as:** 

- **spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 spark_cassandra.py

In order to read Kafka stream, we use **readStream()** and specify Kafka configurations as the given below:
```python3
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "odometry") \
  .option("delimeter",",") \
  .option("startingOffsets", "latest") \
  .load() 
```
Since Kafka send data as binary, first we need to convert the binary value to String using **selectExpr()** as the given below:
```python3
df1 = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),odometrySchema).alias("data")).select("data.*")
df1.printSchema()
```
Although Apache Spark isn't capable of directly write stream data to Cassandra yet (using **writeStream()**), we can do it with use **foreachBatch()** as the given below:
```python3
def writeToCassandra(writeDF, _):
  writeDF.write \
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="odometry", keyspace="ros")\
    .save()

df1.writeStream \
    .option("spark.cassandra.connection.host","localhost:9042")\
    .foreachBatch(writeToCassandra) \
    .outputMode("update") \
    .start()\
    .awaitTermination()
```
Finally, we got the given script [spark-demo/streamingKafka2Cassandra.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/spark-demo/streamingKafka2Cassandra.py):
```python3
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,FloatType,IntegerType
from pyspark.sql.functions import from_json,col

odometrySchema = StructType([
                StructField("id",IntegerType(),False),
                StructField("posex",FloatType(),False),
                StructField("posey",FloatType(),False),
                StructField("posez",FloatType(),False),
                StructField("orientx",FloatType(),False),
                StructField("orienty",FloatType(),False),
                StructField("orientz",FloatType(),False),
                StructField("orientw",FloatType(),False)
            ])

spark = SparkSession \
    .builder \
    .appName("SparkStructuredStreaming") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "odometry") \
  .option("delimeter",",") \
  .option("startingOffsets", "latest") \
  .load() 

df.printSchema()

df1 = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),odometrySchema).alias("data")).select("data.*")
df1.printSchema()

# It is possible to analysis data here using df1


def writeToCassandra(writeDF, _):
  writeDF.write \
    .format("org.apache.spark.sql.cassandra")\
    .mode('append')\
    .options(table="odometry", keyspace="ros")\
    .save()

df1.writeStream \
    .option("spark.cassandra.connection.host","localhost:9042")\
    .foreachBatch(writeToCassandra) \
    .outputMode("update") \
    .start()\
    .awaitTermination()
```
#### (Second Way) Prepare Apache Spark Structured Streaming Pipeline Kafka to Console
There are a few differences between writing to the console and writing to Cassandra. 
First of all, we don't need to use cassandra connector, so we remove it from packages.
```python3
spark = SparkSession \
    .builder \
    .appName("SSKafka") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()
```
With **writeStream()** we can write stream data directly to the console.
```python3
df1.writeStream \
  .outputMode("update") \
  .format("console") \
  .option("truncate", False) \
  .start() \
  .awaitTermination()
```
The rest of the process takes place in the same way as the previous one. Finally, we got the given script spark-demo/streamingKafka2Console.py:
```python3
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,LongType,IntegerType,FloatType,StringType
from pyspark.sql.functions import split,from_json,col

odometrySchema = StructType([
                StructField("id",IntegerType(),False),
                StructField("posex",FloatType(),False),
                StructField("posey",FloatType(),False),
                StructField("posez",FloatType(),False),
                StructField("orientx",FloatType(),False),
                StructField("orienty",FloatType(),False),
                StructField("orientz",FloatType(),False),
                StructField("orientw",FloatType(),False)
            ])

spark = SparkSession \
    .builder \
    .appName("SSKafka") \
    .config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "odometry") \
  .option("delimeter",",") \
  .option("startingOffsets", "latest") \
  .load() 

df1 = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"),odometrySchema).alias("data")).select("data.*")
df1.printSchema()

df1.writeStream \
  .outputMode("update") \
  .format("console") \
  .option("truncate", False) \
  .start() \
  .awaitTermination()
```
### 5. Result
After all the process is done, we got the data in our Cassandra table as the given below:

You can query the given command to see your table:
```
# Open the cqlsh 
cqlsh
# Then write select query to see content of the table
cqlsh> select * from ros.odometry
```
<p align="center" width="100%">
    <img src="https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/cassandra.png"> 
</p>

