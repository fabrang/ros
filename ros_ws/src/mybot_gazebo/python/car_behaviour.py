#!/usr/bin/env python

# ROS python api with lots of handy ROS functions
import rospy

# to be able to subcribe to laser scanner data
from sensor_msgs.msg import LaserScan

# to be able to publish Twist data (and move the robot)
from geometry_msgs.msg import Twist

# to be able to receive the message from static sensor
from std_msgs.msg import String

class carSimpleBehavior(object):
    '''
    Exposes a behavior for the catvehicle so that moves forward until
    it has an obstacle at 1.0 m then stops rotates for some time to the
    right and resumes motion.
    '''
    def __init__(self):
        '''
        Class constructor: will get executed at the moment
        of object creation
        '''
        # register node in ROS network
        rospy.init_node('car_smart_behavior', anonymous=False)
        # print message in terminal
        rospy.loginfo('Car started driving')
        # subscribe to pioneer laser scanner topic
        rospy.Subscriber("/mybot/laser/scan", LaserScan, self.laserCallback)
        # subscribe to stationary laser scanner topic warning message
        rospy.Subscriber('/stat/detect_msg', String, self.sensorCallback)
        # setup publisher to later on move the car
        self.pub_cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        # define member variable and initialize with a big value
        # it will store the distance from the robot to the walls
        self.distance = 10.0


    def stop_car(self):
            '''
            Stop the car when passenger is detected
            '''
            # create empty message of Twist type (check http://docs.ros.org/api/geometry_msgs/html/msg/Twist.html)
            twist_msg = Twist()
            # liner speed
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.linear.z = 0.0
            # angular speed
            twist_msg.angular.x = 0.0
            twist_msg.angular.y = 0.0
            twist_msg.angular.z = 0.0
            # base needs this msg to be published constantly for the robot to keep moving
            for i in range(1,20):
                # publish message
                self.pub_cmd_vel.publish(twist_msg)
                # sleep for a small amount of time
                rospy.sleep(0.1)
                print("Passenger was detected")
                quit()


    def move_forward_until_distance_is_short(self):
        '''
        Move the car forward until it detects an obstacle 5 m in front of him
        then calls stop_car
        '''
        # create empty message of Twist type (check http://docs.ros.org/api/geometry_msgs/html/msg/Twist.html)
        twist_msg = Twist()
        # linear speed
        twist_msg.linear.x = 3.0
        twist_msg.linear.y = 0.0
        twist_msg.linear.z = 0.0
        # angular speed
        twist_msg.angular.x = 0.0
        twist_msg.angular.y = 0.0
        twist_msg.angular.z = 0.0
	
        # base needs this msg to be published constantly for the robot to keep moving so we publish
        # in a loop
        # while the distance from the robot to the walls is bigger than 1m or stat. sensor detected
	    # a passenger keep looping
        while self.distance > 5.0 or self.warning != "data: Warning!":
            self.pub_cmd_vel.publish(twist_msg)
            rospy.sleep(0.1)

        # distance was reported to be less than 5.0 m, lets rotate for some time (to avoid collision)
        self.stop_car()


    def laserCallback(self, msg):
        '''
        This function gets executed every time a laser scanner msg is received on the
        topic: /robot_0/base_scan_1
        '''
        # msg contains the laser scanner msg
        # check http://docs.ros.org/api/sensor_msgs/html/msg/LaserScan.html
        self.distance = min(msg.ranges)


    def sensorCallback(self, msg):
        '''
        This function gets executed every time a laser scanner msg is received on the
        topic: /robot_0/base_scan_1
        '''
        # msg contains the warning about detected passenger
        self.warning = msg
        print(self.warning)
        print(type(self.warning))


    def run_behavior(self):
        print("Started")
        while not rospy.is_shutdown():
            self.move_forward_until_distance_is_short()
  

if __name__ == '__main__':
    # create object of the class carsimpleBehavior (constructor will get executed!)
    my_object = carSimpleBehavior()
    # call run_behavior method of class pioneerSimpleBehavior
    my_object.run_behavior()
