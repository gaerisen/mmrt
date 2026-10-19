import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool

class MockNavFeed(Node):
    def __init__(self):
        super().__init__('mock_nav_feed')
        self.pub_conf = self.create_publisher(Float32, 'confidence', 10)
        self.pub_obs = self.create_publisher(Float32, 'obstacle_importance', 10)
        self.pub_dist = self.create_publisher(Float32, 'distance_from_goal', 10)
        self.pub_marker = self.create_publisher(Bool, 'marker_detection', 10)

        self.timer = self.create_timer(0.2, self.step_scenario)
        self.start_time = time.time()
        self.get_logger().info('Mock Telemetry Feed Initialized.')

    def step_scenario(self):
        # 30-second repeating mission run
        elapsed = (time.time() - self.start_time) % 30.0

        c = Float32()
        o = Float32()
        d = Float32()
        m = Bool()

        # 0s - 4s: INIT (Confidence increases past threshold 0.5)
        if elapsed < 4.0:
            c.data = float(elapsed / 4.0)
            o.data = 0.05
            d.data = 100.0
            m.data = False

        # 4s - 10s: NAVAGATING (Rover drives toward destination)
        elif elapsed < 10.0:
            c.data = 0.95
            o.data = 0.10
            progress = (elapsed - 4.0) / 6.0
            d.data = 100.0 - (progress * 55.0)  # 100m down to 45m
            m.data = False

        # 10s - 15s: OBSTACLE_AVOIDANCE (Obstacle importance spikes > 0.5)
        elif elapsed < 15.0:
            c.data = 0.90
            o.data = 0.85
            d.data = 45.0
            m.data = False

        # 15s - 20s: NAVAGATING (Obstacle clears, distance drops below 15m)
        elif elapsed < 20.0:
            c.data = 0.95
            o.data = 0.15
            progress = (elapsed - 15.0) / 5.0
            d.data = 45.0 - (progress * 33.0)  # 45m down to 12m
            m.data = False

        # 20s - 24s: SEARCH_FOR_MARKER (Rover searches in marker zone)
        elif elapsed < 24.0:
            c.data = 0.98
            o.data = 0.05
            d.data = 10.0
            m.data = False

        # 24s - 30s: MISSION_COMPLETE (Marker detected)
        else:
            c.data = 1.0
            o.data = 0.0
            d.data = 2.0
            m.data = True

        self.pub_conf.publish(c)
        self.pub_obs.publish(o)
        self.pub_dist.publish(d)
        self.pub_marker.publish(m)

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