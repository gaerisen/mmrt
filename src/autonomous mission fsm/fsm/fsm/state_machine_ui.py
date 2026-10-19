from random import Random

from ursina import Ursina, Slider, Entity, camera, color
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool

app = Ursina()
def update_confidence():
    print("confidence_slider value: ", confidence_slider.value)
    
def obstacle_importance():
    print("obstacle_importance_slider value: ", obstacle_importance_slider.value)
    
def update_distance_from_goal():
    print("distance_from_goal_slider value: ", distance_from_goal_slider.value)


def update_state():
    pass
controls_box = Entity(parent=camera.ui, position = (0,-.3,0),model='quad', scale=(.7, .24), color=color.gray)
slider_scale = (1 / .7, 1 / .24, 1)
confidence_slider = Slider(parent=controls_box, position=(-.4, .28, -.01), scale=slider_scale, min=0, max=100, on_value_changed=update_confidence, dynamic=True)
obstacle_importance_slider = Slider(parent=controls_box, position=(-.4, 0, -.01), scale=slider_scale, min=0, max=100, on_value_changed=obstacle_importance, dynamic=True)
distance_from_goal_slider = Slider(parent=controls_box, position=(-.4, -.28, -.01), scale=slider_scale, min=0, max=100, on_value_changed=update_distance_from_goal, dynamic=True)



app.run()


class RoverSim(Entity):
    def __init__(self):
        self.confidence = 0
        self.obstacle_importance = 0
        self.distance_from_goal = 100
        self.marker_detection = False
        self.current_state = "INIT"
        
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
        self.current_state = msg.data

    #In practice, this function should be called in pieces. Just for easierness purposes, I will call it in one function.
    #The states might end up jittering between each other with each update because of this.
    def update(self):
        msg_confidence = Float32()
        msg_confidence.data = confidence_slider.value
        self.confidence_pub.publish(msg_confidence)

        msg_obstacle_importance = Float32()
        msg_obstacle_importance.data = obstacle_importance_slider.value
        self.obstacle_importance_pub.publish(msg_obstacle_importance)

        msg_distance_from_goal = Float32()
        msg_distance_from_goal.data = distance_from_goal_slider.value
        self.distance_from_goal_pub.publish(msg_distance_from_goal)

    def found_marker(self):
        msg_marker_detection = Bool()
        msg_marker_detection.data = True
        self.marker_detection_pub.publish(msg_marker_detection)

    
def main(args=None):

    rclpy.init(args=args)

    fsm_sim = RoverSim()
    
    rclpy.spin(fsm_sim)

    simloop (fsm_sim)
    rclpy.shutdown()


#this simulates what the sensors might be reporting.
def simloop(fsm_sim):
    print(fsm_sim.current_state)
    while True:
        fsm_sim.update()
        match fsm_sim.current_state:
            case "INIT":
                confidence_slider.value = 0
                obstacle_importance_slider.value = 0
                distance_from_goal_slider.value = 0
            case "NAVAGATING":
                confidence_slider.value -= confidence_slider.value * (Random.random() * .1)
                
                distance_from_goal_slider.value += 1
            case "OBSTACLE_AVOIDANCE":
                confidence_slider.value -= confidence_slider.value * (Random.random() * .1)
                distance_from_goal_slider.value -= .5

            case "SEARCH_FOR_MARKER":
                if Random.random() >= .95:
                    fsm_sim.found_marker()

            case "MARKER_DETECTED":
                print("Marker detected!")
                break

            case "MISSION_COMPLETE":
                print("Mission complete!")
                #idk why it would ever be here but yeah
                break
            case "STOP":
                confidence_slider.value += 5
                confidence_slider.value += confidence_slider.value * (Random.random() * .1)

            case "FAULT":
                print("Fault")
            case _:
                pass

        confidence_slider.value += (100 - confidence_slider.value) * .1

app.run()
