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
    if count == 20:
        count = 0

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda message: json.dumps(message).encode('utf-8')
)

if __name__=="__main__":

    rospy.init_node('odomSubscriber', anonymous=True)
    rospy.Subscriber('odom',Odometry,callback)
    rospy.spin()

