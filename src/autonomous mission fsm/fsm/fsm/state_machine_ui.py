from ursina import *
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool

app = Ursina()
def update_confidence():
    print("Slider1 value: ", slider1.value)
    
def obstacle_importance():
    print("Slider2 value: ", slider2.value)
    
def update_distance_from_goal():
    print("Slider3 value: ", slider3.value)


def update_state():
    pass
controls_box = Entity(parent=camera.ui, position = (0,-.3,0),model='quad', scale=(.7, .24), color=color.gray)
slider_scale = (1 / .7, 1 / .24, 1)
slider1 = Slider(parent=controls_box, position=(-.4, .28, -.01), scale=slider_scale, min=0, max=100, on_value_changed=update_confidence, dynamic=True)
slider2 = Slider(parent=controls_box, position=(-.4, 0, -.01), scale=slider_scale, min=0, max=100, on_value_changed=obstacle_importance, dynamic=True)
slider3 = Slider(parent=controls_box, position=(-.4, -.28, -.01), scale=slider_scale, min=0, max=100, on_value_changed=update_distance_from_goal, dynamic=True)



app.run()


class RoverSim(Entity):
    def __init__(self):
        self.confidence = 0
        self.obstacle_importance = 0
        self.distance_from_goal = 100
        self.marker_detection = False
        self.reported_state = "INIT"
        
        self.confidence_pub = self.create_publisher(
            Float32,
            'confidence',
            10)
        self.obstacle_importance_pub = self.create_publisher(
            Float32,
            'obstacle_importance',
            10)
        self.distance_from_goal_pub = self.create_publisher(
            Float32,
            'distance_from_goal',
            10)
        self.marker_detection_pub = self.create_publisher(
            Bool,
            'marker_detection',
            10)
        self.state_sub = self.create_subscription(
            String,
            'nav_state', 
            self.reported_state,
            10)
    def reported_state(self, msg):
        self.reported_state = msg.data

    #In practice, this function should be called in pieces. Just for easierness purposes, I will call it in one function.
    #The states might end up jittering between each other with each update because of this.
    def update(self):
        msg_confidence = Float32()
        msg_confidence.data = slider1.value
        self.confidence_pub.publish(msg_confidence)

        msg_obstacle_importance = Float32()
        msg_obstacle_importance.data = slider2.value
        self.obstacle_importance_pub.publish(msg_obstacle_importance)

        msg_distance_from_goal = Float32()
        msg_distance_from_goal.data = slider3.value
        self.distance_from_goal_pub.publish(msg_distance_from_goal)

    
def main(args=None):

    rclpy.init(args=args)

    fsm_sim = RoverSim()
    
    rclpy.spin(fsm_sim)

    rclpy.shutdown()


