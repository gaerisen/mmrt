import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge     # Tool to convert between ROS and OpenCV images
from yolozone import PoseDetector
import cv2
from . import command_detector as CommandDetector

class RoverVision(Node):
    def __init__(self):
        super().__init__('rover_sim')

        self.camera = cv2.VideoCapture(0) # this is the default camera on the device
        self.detector = PoseDetector(model='yolov8n-pose.pt') # TODO: research what model to use
        self.bridge = CvBridge()

        self.publish_frame = self.create_publisher(Image, 'camera_frame', 10)
        self.publish_human_detected = self.create_publisher(Bool, 'human_detected', 10)
        self.publish_command = self.create_publisher(String, 'command', 10)

        self.camera_timer = self.create_timer(1.0 / 10.0, self.process_frame)

    def process_frame(self): # I am assuming this is like a while loop but idk
        got_frame, frame = self.camera.read()
        if not got_frame:
            self.get_logger().warning("Could not read camera frame", throttle_duration_sec=5.0)
            return

        keypoints = self.detector.find_keypoints(frame)
        human_detected = keypoints is not None and keypoints.xy.shape[0] > 0
        self.publish_human_detected.publish(Bool(data=human_detected))

        if human_detected:
            measurements = CommandDetector.get_measurements(self.detector, keypoints)
            command = CommandDetector.detect_command(measurements)
            color = CommandDetector.COLORS.get(command, CommandDetector.DEFAULT_COLOR)
            frame = CommandDetector.draw_skeleton(self.detector, keypoints, frame, color)

            if command is not None:
                self.publish_command.publish(String(data=command.value))
 
        self.publish_frame.publish(self.bridge.cv2_to_imgmsg(frame, encoding="bgr8"))

    def destroy_node(self):
        self.camera.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    vision = RoverVision()

    try:
        rclpy.spin(vision)
    except KeyboardInterrupt:
        pass
    finally:
        vision.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()