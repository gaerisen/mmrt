import pytest
import rclpy
from rclpy.node import Node
from custom_interfaces.srv import HandGesture
import time

@pytest.fixture(scope="module")
def ros_context():
    rclpy.init()
    yield
    rclpy.shutdown()

@pytest.mark.timeout(5)
def test_service(ros_context):
    test_node = Node('gesture_detector')
    assert test_node.get_name() == "gesture_detector", "Node creation failed"

    client = test_node.create_client(HandGesture, 'get_gesture')
    assert client.wait_for_service(timeout_sec=10), "Service not available"

    request = HandGesture.Request()
    request.image_path = "/home/mmrt/assets/images/peace.jpg"

    future = client.call_async(request)
    rclpy.spin_until_future_complete(test_node, future, timeout_sec = 3.0)

    assert future.done(), "Service call failed to complete"
    response = future.result()
    assert response.gesture == "peace", f"Expected 'peace', got {response.gesture}"

    test_node.destroy_node()
