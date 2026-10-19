from builtins import KeyboardInterrupt
from random import random

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, Float32, String


class MockNavFeed(Node):
    def __init__(self):
        super().__init__('mock_nav_feed')
        self.pub_conf = self.create_publisher(
            Float32, 'confidence', 10)
        self.pub_obs = self.create_publisher(
            Float32, 'obstacle_importance', 10)
        self.pub_dist = self.create_publisher(
            Float32, 'distance_from_goal', 10)
        self.pub_marker = self.create_publisher(
            Bool, 'marker_detection', 10)
        self.state_sub = self.create_subscription(
            String,
            'nav_state',
            self.state_callback,
            10)

        self.current_state = 'INIT'
        self.confidence = 0.0
        self.obstacle_importance = 0.0
        self.distance_from_goal = 100.0
        self.marker_detection = False
        self.timer = self.create_timer(1, self.step_scenario)
        self.get_logger().info('Mock Telemetry Feed Initialized.')

    def state_callback(self, msg: String):
        self.current_state = msg.data

    def step_scenario(self):
        if self.current_state == 'INIT':
            self.confidence = min(
                self.confidence + 0.06 + random() * 0.06,
                1.0)
            self.obstacle_importance = 0.0
            self.distance_from_goal = 100.0
            self.marker_detection = False
        elif self.current_state == 'NAVAGATING':
            if random() < 0.015:
                self.confidence = max(
                    self.confidence - (0.2 + random() * 0.35),
                    0.0)
            else:
                self.confidence += (
                    (0.98 - self.confidence) * (0.02 + random() * 0.06))

            self.distance_from_goal = max(
                self.distance_from_goal - (0.5 + random() * 0.8),
                0.0)

            if random() < 0.035:
                self.obstacle_importance = 0.7 + random() * 0.25
            else:
                self.obstacle_importance = max(
                    self.obstacle_importance - (0.005 + random() * 0.02),
                    0.05)
        elif self.current_state == 'OBSTACLE_AVOIDANCE':
            if random() < 0.04:
                self.confidence = max(
                    self.confidence - (0.1 + random() * 0.2),
                    0.0)
            else:
                self.confidence = max(
                    self.confidence - random() * 0.025,
                    0.0)
            self.obstacle_importance = max(
                self.obstacle_importance - (0.02 + random() * 0.025),
                0.0)
            self.distance_from_goal = max(
                self.distance_from_goal - (0.1 + random() * 0.35),
                0.0)
        elif self.current_state == 'SEARCH_FOR_MARKER':
            self.confidence += (
                (0.98 - self.confidence) * (0.02 + random() * 0.06))
            if not self.marker_detection and random() < 0.04:
                self.marker_detection = True
        elif self.current_state == 'MISSION_COMPLETE':
            self.confidence = 1.0
            self.obstacle_importance = 0.0
            self.distance_from_goal = 0.0
            self.marker_detection = True
        elif self.current_state == 'STOP':
            self.confidence = min(
                self.confidence + 0.025 + random() * 0.04,
                1.0)
        elif self.current_state == 'FAULT':
            self.confidence = max(
                self.confidence - (0.02 + random() * 0.08),
                0.0)
            self.obstacle_importance = max(self.obstacle_importance, 0.85)

        confidence_msg = Float32()
        confidence_msg.data = float(self.confidence)
        obstacle_msg = Float32()
        obstacle_msg.data = float(self.obstacle_importance)
        distance_msg = Float32()
        distance_msg.data = float(self.distance_from_goal)
        marker_msg = Bool()
        marker_msg.data = self.marker_detection

        self.pub_conf.publish(confidence_msg)
        self.pub_obs.publish(obstacle_msg)
        self.pub_dist.publish(distance_msg)
        self.pub_marker.publish(marker_msg)


def main(args=None):
    rclpy.init(args=args)
    node = MockNavFeed()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
