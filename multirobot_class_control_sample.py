#!/usr/bin/env python3

import rospy
import numpy as np
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Twist
from move_base_msgs.msg import MoveBaseActionResult


class bot_container():
    def __init__(self, uid_name:str, odom_topic="odom", movement_topic="cmd_vel", goal_result_topic="move_base/result", goal_pub_topic="move_base_simple/goal") -> None:
        """ 
        This object acts as a container for the bot.
        It creates all of the publishers and subscribers. 
        It also stores the position and other things

        Args:
            uid_name (str): unique robot prefix
            odom_topic (str, optional): topic name for the odom of robot. Defaults to "odom".
            movement_topic (str, optional): topic to control motion of robot. Defaults to "cmd_vel".
            goal_result_topic (str, optional): move_base result topic. Defaults to "move_base/result".
            goal_pub_topic (str, optional): move_base publish goal topic. Defaults to "move_base_simple/goal".
        """
        self.prefix = uid_name
        
        
        #-- movement publisher
        rospy.logdebug(f"setting up move_publisher to /{self.prefix}/{movement_topic}")
        self.movement_pub = rospy.Publisher(f"/{self.prefix}/cmd_vel", Twist, queue_size=1) 
        #probably unneccessary in real version
        
        
        #-- odom subscriber
        rospy.logdebug(f"setting up odom_subscriber to /{self.prefix}/{odom_topic}")
        
        #---- initial
        self.current_pose = Odometry()
        
        #---- subscriber
        rospy.Subscriber(f"/{self.prefix}/odom", Odometry, self.cb_odom)
        
        
        #-- move_base 
        rospy.logdebug(f"setting up goal movement control for {self.prefix} (pub:{goal_pub_topic}) (result:{goal_result_topic})")
        
        #---- initial
        self.action_result = MoveBaseActionResult()
        self.action_result.result = -5
        self.action_being_done = False 
        
        #---- subscriber
        rospy.Subscriber(f"/{self.prefix}/{goal_result_topic}", MoveBaseActionResult, self.cb_action_result)
        
        #---- publisher
        self.goal_publisher = rospy.Publisher(f"/{self.prefix}/{goal_pub_topic}", PoseStamped, queue_size=1)
        
        
        
    def publish_movement(self, twist_msg: Twist):
        """publisher for direct speed commands"""
        self.goal_publisher.publish(twist_msg)
        
    def publish_goal(self, goal_msg: PoseStamped):
        """publish for action_goal"""
        self.action_being_done = True 
        self.goal_publisher.publish(goal_msg)
        
    def cb_odom(self, msg:Odometry):
        """callback for odom"""
        self.current_pose = msg
        
    def cb_action_result(self, msg:MoveBaseActionResult):
        """callback for action_result"""
        self.action_result = msg
        self.action_being_done = False 




class test_spawn():
    def __init__(self, num_to_spawn) -> None:
        rospy.init_node("multibot_via_class_test")    
        self.bot_list = list()

        for idx in range(num_to_spawn):
            # A unique name prefix for each robot
            uid = f"robot_{idx}"

            rospy.loginfo(f"Creating bot called \"{uid}\" as object")

            # create all publishers and subscribers for bot
            bot = bot_container(uid)

            # add the bot object to the list
            self.bot_list.append(bot)
    
    
    
    def spin(self):
        rospy.loginfo("Now spinning (ctrl + c  to close)")
        rospy.spin()
            
            
            
    def example(self):
        """Just some random test points to demo the functionality"""
        print('\n')
        
        # test 1
        print("Bot 1's prefix:", self.bot_list[1].prefix, '\n')
        
        
        # test 2
        #-- a test position
        test_point = PoseStamped()
        test_point.pose.position.x = 3
        test_point.pose.position.y = 7
        test_point.pose.orientation.w = 1
        
        print("Bot 1 publish message:", test_point, '\n')
        self.bot_list[1].publish_goal(test_point)
        
        
        # test 3
        #-- a test position
        test_point = PoseStamped()
        test_point.pose.position.x = -4
        test_point.pose.position.y = -2
        test_point.pose.orientation.w = 1
        
        print("Bot 3 publish message:", test_point, '\n')
        self.bot_list[3].publish_goal(test_point)
        
        
        # test 4
        print("action_result of number 4: ", self.bot_list[4].action_result, '\n')
        
        
        # test 5
        print("action_being_done for 0: ", self.bot_list[0].action_being_done, '\n')
        
        
        # test 6
        print("action_being_done for 1: ", self.bot_list[1].action_being_done, '\n')
        
        
        
if __name__ == "__main__": 
    example = test_spawn(5)
    example.example()
    example.spin()