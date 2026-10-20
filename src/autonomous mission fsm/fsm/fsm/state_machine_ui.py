from random import Random
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool

class RoverUI(Node):
    def __init__(self):
        super().__init__('rover_sim')
        self.confidence = 0
        self.obstacle_importance = 0
        self.distance_from_goal = 100
        self.marker_detection = False
        self.current_state = "INIT"
        
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

    #In practice, this function should be called in pieces. Just for easierness purposes, I will call it in one function.
    #The states might end up jittering between each other with each update because of this.
    def found_marker(self):
        self.marker_detection = True

    
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
