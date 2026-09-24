
from enum import Enum

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32

class Status(Enum):
    INIT = 0
    NAVAGATING = 1
    OBSTACLE_AVOIDANCE = 2
    SEARCH_FOR_MARKER = 3
    MISSION_COMPLETE = 4
    STOP = 5
    FAULT = 6
    #SEARCH_FOR_MARKER = 7

class Nav_State_Machine(Node):

    


    def __init__(self):
        super().__init__('Nav_State_Machine')
        self.confidence = 0
        self.obstacle_importance = 0
        self.distance_from_goal = 100
        self.marker_detection = 0

        self.confidence_sub = self.create_subscription(
            Float32,
            'confidence',
            self.listener_callback_confidence,
            10)
        self.obstacle_importance_sub = self.create_subscription(
            Float32,
            'obstacle_importance',
            self.listener_callback_obstacle_importance,
            10)
        self.distance_from_goal = self.create_subscription(
            Float32,
            'distance_from_goal',
            self.listener_callback_distance_from_goal,
            10)
        self.distance_from_goal = self.create_subscription(
            Float32,
            'marker_detection',
            self.listener_callback_marker_detection,
            10)
        self.state = Status.INIT

    def evaluate_state():
        pass

    def listener_callback_confidence(self, msg):
        self.get_logger().info('Confidence: "%f"' % msg.data)
        self.confidence = msg.data
        self.evaluate_state()

        

    def listener_callback_obstacle_importance(self, msg):
        self.get_logger().info('Obstacle_importance: "%f"' % msg.data)
        self.obstacle_importance = msg.data
        self.evaluate_state()

    def listener_callback_distance_from_goal(self, msg):
        self.get_logger().info('Distance_from_goal: "%f"' % msg.data)
        self.distance_from_goal = msg.data
        self.evaluate_state()

    def listener_callback_marker_detection(self, msg):
        self.get_logger().info('Marker_detection: "%f"' % msg.data)
        self.marker_detection = msg.data
        



    