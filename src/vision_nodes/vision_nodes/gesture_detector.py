import rclpy
from rclpy.node import Node
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

from custom_interfaces.msg import HandGesture


def RunInference(processor, model):
    image = Image.open("/home/mmrt/assets/images/hand.jpeg")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    return logits.argmax(-1).item()


class GestureDetector(Node):
    def __init__(self):
        super().__init__('gesture_detector')
        self.pub = self.create_publisher(HandGesture, 'gesture', 10)

        model_path = "/home/mmrt/assets/models/dima806"
        self.processor = AutoImageProcessor.from_pretrained(model_path)
        self.model = AutoModelForImageClassification.from_pretrained(model_path)

        msg = HandGesture()
        msg.gesture = RunInference(self.processor, self.model)

        self.pub.publish(msg)


def main(args=None):
    print("Gesture detector spinning up")
    rclpy.init(args=args)
    node = GestureDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
