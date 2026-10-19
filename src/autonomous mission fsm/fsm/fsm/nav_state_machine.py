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

class NavStateMachine(Node):
    def __init__(self):
        super().__init__('nav_state_machine')
        self.confidence = 0.0
        self.obstacle_importance = 0.0
        self.distance_from_goal = 100.0
        self.marker_detection = False
        self.state = Status.INIT

        # Subscriptions
        self.confidence_sub = self.create_subscription(
            Float32,
            'confidence',
            self.listener_callback_confidence,
            10
        )
        self.obstacle_importance_sub = self.create_subscription(
            Float32,
            'obstacle_importance',
            self.listener_callback_obstacle_importance,
            10
        )
        self.distance_from_goal_sub = self.create_subscription(
            Float32,
            'distance_from_goal',
            self.listener_callback_distance_from_goal,
            10
        )
        self.marker_detection_sub = self.create_subscription(
            Bool,
            'marker_detection',
            self.listener_callback_marker_detection,
            10
        )

        # Publisher
        self.state_publisher = self.create_publisher(
            String,
            'nav_state',
            10
        )

        self.broadcast_state()
        self.get_logger().info('Nav State Machine Node Initialized.')

    def broadcast_state(self):
        msg = String()
        msg.data = self.state.name
        self.state_publisher.publish(msg)

    def evaluate_state(self):
        previous_state = self.state
        
        if self.state == Status.INIT:
            if self.confidence > 0.5:
                self.state = Status.NAVAGATING

        elif self.state == Status.NAVAGATING:
            if self.confidence < .65:
                self.state = Status.STOP
            if self.obstacle_importance > 0.5:
                self.state = Status.OBSTACLE_AVOIDANCE
            elif self.distance_from_goal < 15.0:
                self.state = Status.SEARCH_FOR_MARKER
                

        elif self.state == Status.OBSTACLE_AVOIDANCE:
            if self.obstacle_importance < 0.5:
                self.state = Status.NAVAGATING
        elif self.state == Status.STOP:
            if self.confidence > .85: 
                self.state = Status.NAVAGATING
        elif self.state == Status.SEARCH_FOR_MARKER:
            if self.marker_detection:
                self.state = Status.MISSION_COMPLETE
        
        elif self.state in (Status.MISSION_COMPLETE, Status.STOP, Status.FAULT):
            pass

        if self.state != previous_state:
            self.get_logger().info(f'State Changed: {previous_state.name} -> {self.state.name}')

    def listener_callback_confidence(self, msg: Float32):
        self.confidence = float(msg.data)
        self.evaluate_state()
        self.broadcast_state()

    def listener_callback_obstacle_importance(self, msg: Float32):
        self.obstacle_importance = float(msg.data)
        self.evaluate_state()
        self.broadcast_state()

    def listener_callback_distance_from_goal(self, msg: Float32):
        self.distance_from_goal = float(msg.data)
        self.evaluate_state()
        self.broadcast_state()

    def listener_callback_marker_detection(self, msg: Bool):
        self.marker_detection = bool(msg.data)
        self.evaluate_state()
        self.broadcast_state()


def main(args=None):
    rclpy.init(args=args)
    fsm = NavStateMachine()
    try:
        rclpy.spin(fsm)
    except KeyboardInterrupt:
        pass
    finally:
        fsm.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()