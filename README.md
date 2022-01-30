## PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra

The purpose of this project is to demonstrate a structured streaming pipeline with Apache Spark. The process consists of given steps:
1. Prepare a robotic simulation environment to generate data to feed into the Kafka. 
2. Prepare Kafka and Zookeeper environment to store discrete data.
3. Prepare Cassandra environment to store analyzed data.
4. Prepare Apache Spark structured streaming pipeline, integrate with Kafka and Cassandra.

<p align="center" width="100%">
    <img src="https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/architecture.PNG"> 
</p>

### 1. Prepare a robotic simulation environment
[ROS (Robot Operating System)](http://wiki.ros.org/) allows us to design a robotic environment. We will use [Turtlebot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/), a robot in [Gazebo](http://gazebosim.org/) simulation env, to generate data for our use case. Turtlebot3 publishes its data with ROS topics. Therefore, we will subscribe the topic and send data into Kafka.

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

#### Analysis the data we will use
Turtlebot3 publishes its odometry data with ROS "odom" topic. So, we can see the published data with the given command:
```
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
In this case, we will just use the given part of the data:
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

Once you create "demo" topic, you can run [kafka-demo/producer.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/kafka-demo/producer.py) and [kafka-demo/consumer.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/kafka-demo/consumer.py) respectively to check your setup. If you haven't installed [kafka-python](https://kafka-python.readthedocs.io/en/master/), use the given command and then run given files.
```
pip install kafka-python
```
You should see a view like the one given below.
<p align="center" width="100%">
    <img src="https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/kafka-demo.png"> 
</p>

#### Prepare Kafka for Use Case
First of all, we will create a new Kafka topic for ROS odom data using the given command:
```
# Change your path to Kafka folder and then run 
bin/zookeeper-server-start.sh config/zookeeper.properties

# Open second terminal and then run
bin/kafka-server-start.sh config/server.properties

# Create Kafka "odometry" topic for ROS odom data
bin/kafka-topics.sh --create --topic odometry --partitions 1 --replication-factor 1 -bootstrap-server localhost:9092
```
Then we will write a ROS subscriber to listen to the data from Turtlebot3. Also, since we need to send data to Kafka, it is necessary to add a producer script in it. We will use [ros/publish2kafka.py](https://github.com/zekeriyyaa/PySpark-Structured-Streaming-ROS-Kafka-ApacheSpark-Cassandra/blob/main/ros/publish2kafka.py) to do it. This script subscribes to the odom topic and sends the content of the topic to Kafka.

### 3. Prepare Cassandra environment

#### Installation of Cassandra
We won't address the whole installation process of Cassandra but you can access all required info from [Cassandra Installation](https://phoenixnap.com/kb/install-cassandra-on-ubuntu).

After all installations are completed, you can demo Cassandra using *cqlsh*.

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


