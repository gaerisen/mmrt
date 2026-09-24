import rclpy
from rclpy.node import Node
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

from custom_interfaces.srv import HandGesture

class GestureDetector(Node):
    def __init__(self):
        super().__init__('gesture_detector')

        model_path = "/home/mmrt/assets/models/dima806"
        self.processor = AutoImageProcessor.from_pretrained(model_path)
        self.model = AutoModelForImageClassification.from_pretrained(model_path)

        self.srv = self.create_service(HandGesture, 'get_gesture',
                                       self.callback)
        print("Ready")

    def callback(self, req, resp):
        image = Image.open(req.image_path)
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits
        idx = logits.argmax(-1).item()

        resp.gesture = self.model.config.id2label[idx]

        return resp



def main(args=None):
    print("Gesture detector spinning up")

    rclpy.init(args=args)

    node = GestureDetector()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
