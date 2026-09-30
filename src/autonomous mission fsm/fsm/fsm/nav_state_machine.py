
from enum import Enum

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool

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
        self.marker_detection = False

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
        self.distance_from_goal_sub = self.create_subscription(
            Float32,
            'distance_from_goal',
            self.listener_callback_distance_from_goal,
            10)
        self.marker_detection_sub = self.create_subscription(
            bool,
            'marker_detection',
            self.listener_callback_marker_detection,
            10)
        self.state = Status.INIT

    def evaluate_state(self):
        if self.state == Status.INIT:
            if self.confidence > 0.5:
                self.state = Status.NAVAGATING
        elif self.state == Status.NAVAGATING:
            if self.obstacle_importance > 0.5:
                self.state = Status.OBSTACLE_AVOIDANCE
            elif self.distance_from_goal < 15.0:
                self.state = Status.SEARCH_FOR_MARKER
        elif self.state == Status.OBSTACLE_AVOIDANCE:
            if self.obstacle_importance < 0.5:
                self.state = Status.NAVAGATING
        elif self.state == Status.SEARCH_FOR_MARKER:
            if self.marker_detection == True:
                self.state = Status.MISSION_COMPLETE
            else:
                pass
        elif self.state == Status.MISSION_COMPLETE:
            pass
        elif self.state == Status.STOP:
            pass
        elif self.state == Status.FAULT:
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
        self.get_logger().info('Marker_detection: "%b"' % msg.data)
        self.marker_detection = msg.data


def main(args=None):
    rclpy.init(args=args)

    fsm = Nav_State_Machine()
    fsm.get_logger().info('Marker_detection: "%b"' % fsm.confidence)
    print (fsm.confidence)
    rclpy.spin(fsm)

    rclpy.shutdown()


if __name__ == '__main__':
    main()

    # def control_loop(self):
    #     """Called at 5 Hz. Dispatches to the handler for the current state."""
    #     self.publish_state()
 
    #     handlers = {
    #         Status.INIT: self.do_init,
    #         Status.NAVIGATE_TO_WAYPOINT: self.do_navigate,
    #         Status.OBSTACLE_AVOIDANCE: self.do_obstacle_avoidance,
    #         Status.SEARCH_FOR_MARKER: self.do_search_for_marker,
    #         Status.APPROACH_MARKER: self.do_approach_marker,
    #         Status.MISSION_COMPLETE: self.do_mission_complete,
    #         Status.FAULT: self.do_fault,
    #     }
    #     handlers[self.state]()