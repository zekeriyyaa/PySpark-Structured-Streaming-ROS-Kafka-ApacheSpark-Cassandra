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
We won't address the whole installation process of Kafka and Zookeeper but you can access all required info from [Kakfa & Zookeeper Installation](https://www.linode.com/docs/guides/how-to-install-apache-kafka-on-ubuntu/).

After all installations are completed, you can demo Kafka using the given commands:
```
# Change your path to Kafka folder and then run 
bin/zookeeper-server-start.sh config/zookeeper.properties

# Open second terminal and then run
bin/kafka-server-start.sh config/server.properties

# Create Kafka "demo" topic
bin/kafka-topics.sh --create --topic demo --partitions 1 --replication-factor 1 -bootstrap-server localhost:9092
```



