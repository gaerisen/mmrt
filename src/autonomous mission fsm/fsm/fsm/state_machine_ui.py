from random import Random
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge     # Tool to convert between ROS and OpenCV images
import cv2
import numpy as np

class RoverUI(Node):
    def __init__(self):
        super().__init__('rover_sim')
        self.confidence = 0
        self.obstacle_importance = 0
        self.distance_from_goal = 100
        self.marker_detection = False
        self.current_state = "INIT"
        
        

        self.model = "/workspaces/mmrt/src/autonomous mission fsm/fsm/fsm/face_detection_yunet_2023mar.onnx"

        self.detector = cv2.dnn.readNetFromONNX(self.model)
        self.detector_output_names = self.detector.getUnconnectedOutLayersNames()
        self.detector_input_size = 320

        print("Face detector initialized")

        
        self.camera = cv2.VideoCapture("src/autonomous mission fsm/fsm/fsm/WIN_20261026_11_40_27_Pro.mp4")
        self.bridge = CvBridge()
        self.camera_timer = self.create_timer(
            1.0 / 30.0,
            self.publish_camera_image
        )
        
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
            Bool,
            'marker_detection',
            self.listener_callback_marker_detection,
            10)
        self.state_sub = self.create_subscription(
            String,
            'nav_state', 
            self.reported_state,
            10)
        self.pub_cam = self.create_publisher(
                    Image, 'camera_image', 10)
        self.pub_face_detected = self.create_publisher(
                    Bool, 'face_detected', 10)

        self.pub_face_detected.publish(
                        Bool(data=bool(True))
                    )
    def publish_camera_image(self):
    
        success, frame = self.camera.read()

        if not success:
            self.get_logger().warning("Could not read video frame")
            return

        input_size = self.detector_input_size
        frame = cv2.resize(frame, (input_size, input_size))

        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=1.0,
            size=(input_size, input_size),
            mean=(0, 0, 0),
            swapRB=False,
            crop=False
        )

        try:
            self.detector.setInput(blob)
            outputs = self.detector.forward(
                self.detector_output_names
            )

            out = dict(zip(self.detector_output_names, outputs))

            boxes = []
            scores = []

            for stride in (8, 16, 32):
                cls = out[f"cls_{stride}"].reshape(-1)
                obj = out[f"obj_{stride}"].reshape(-1)
                bbox = out[f"bbox_{stride}"].reshape(-1, 4)

                confidence = cls * obj
                feature_width = input_size // stride

                for i in np.where(confidence >= 0.8)[0]:
                    row = i // feature_width
                    col = i % feature_width

                    x1 = col * stride - bbox[i, 0] * stride
                    y1 = row * stride - bbox[i, 1] * stride
                    x2 = col * stride + bbox[i, 2] * stride
                    y2 = row * stride + bbox[i, 3] * stride

                    boxes.append([
                        float(x1),
                        float(y1),
                        float(x2 - x1),
                        float(y2 - y1)
                    ])
                    scores.append(float(confidence[i]))

            indices = cv2.dnn.NMSBoxes(
                boxes, scores, 0.8, 0.3
            )

            face_detected = indices is not None and len(indices) > 0

            self.publish_face_detected(face_detected)

            ros_image = self.bridge.cv2_to_imgmsg(
                frame,
                encoding="bgr8"
            )
            self.pub_cam.publish(ros_image)

        except cv2.error as e:
            self.get_logger().error(f"Face detection failed: {e}")

    def publish_face_detected(self, detected: bool):
            msg = Bool()
            msg.data = detected
            self.pub_face_detected.publish(msg) 
            print(msg.data)   
            
    def listener_callback_confidence(self, msg: Float32):
        self.confidence = float(msg.data)

    def listener_callback_obstacle_importance(self, msg: Float32):
        self.obstacle_importance = float(msg.data)

    def listener_callback_distance_from_goal(self, msg: Float32):
        self.distance_from_goal = float(msg.data)

    def listener_callback_marker_detection(self, msg: Bool):
        self.marker_detection = bool(msg.data)

    def reported_state(self, msg):
        self.current_state = msg.data

    def found_marker(self):
        self.marker_detection = True

 
def main(args=None):
    rclpy.init(args=args)

    ui = RoverUI()

    try:
        rclpy.spin(ui)

    except KeyboardInterrupt:
        pass

    finally:
        ui.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


