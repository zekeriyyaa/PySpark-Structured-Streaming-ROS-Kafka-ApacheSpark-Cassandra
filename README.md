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
[ROS (Robot Operating System)](http://wiki.ros.org/) allows us to design a robotic environment. We will use [Turtlebot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/), a robot in [Gazebo](http://gazebosim.org/) simulation env, to generate data for our use case. Turtlebot3 publishes its data across ROS topic. Therefore, we will subscribe the topic and send data into Kafka.

