from enum import Enum
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32, Bool

class ScienceState(Enum):
    INIT = 0
    SITE_SURVEY = 1
    DRILL_SAMPLING = 2
    SEAL_AND_STORE = 3
    ASSAY_ANALYSIS = 4
    MISSION_COMPLETE = 5
    FAULT = 6
    ESTOP = 7

class ScienceStateMachine(Node):
    def __init__(self):
        super().__init__('science_state_machine')
        self.state = ScienceState.INIT
        self.site_arrived = False
        self.site_survey_complete = False
        self.drill_depth_cm = 0.0
        self.target_drill_depth_cm = 10.0
        self.drill_current_amps = 0.0
        self.drill_stall_threshold = 8.5
        self.sample_chamber_sealed = False
        self.assay_progress_pct = 0.0
        self.hardware_fault = False
        self.estop_active = False

        self.site_arrived_sub = self.create_subscription(Bool, '/science/site_arrived', self.callback_site_arrived, 10)
        self.survey_done_sub = self.create_subscription(Bool, '/science/survey_complete', self.callback_survey_complete, 10)
        self.drill_depth_sub = self.create_subscription(Float32, '/science/drill/depth_cm', self.callback_drill_depth, 10)
        self.drill_current_sub = self.create_subscription(Float32, '/science/drill/motor_current', self.callback_drill_current, 10)
        self.chamber_sealed_sub = self.create_subscription(Bool, '/science/sample_sealed', self.callback_chamber_sealed, 10)
        self.assay_progress_sub = self.create_subscription(Float32, '/science/assay/progress_pct', self.callback_assay_progress, 10)
        self.estop_sub = self.create_subscription(Bool, '/rover/estop', self.callback_estop, 10)

        self.state_pub = self.create_publisher(String, '/science/fsm_state', 10)
        self.command_pub = self.create_publisher(String, '/science/actuator_command', 10)
        self.timer = self.create_timer(0.2, self.control_loop)

    def transition_to(self, new_state: ScienceState):
        if self.state == new_state:
            return
        old_state = self.state
        self.state = new_state
        self.get_logger().warn(f'TRANSITION: {old_state.name} -> {self.state.name}')

        cmd_msg = String()
        if self.state == ScienceState.SITE_SURVEY:
            cmd_msg.data = 'START_RAMAN_SPECTROMETER_AND_PANO'
        elif self.state == ScienceState.DRILL_SAMPLING:
            cmd_msg.data = 'DEPLOY_DRILL_CAROUSEL'
        elif self.state == ScienceState.SEAL_AND_STORE:
            cmd_msg.data = 'RETRACT_DRILL_AND_SEAL_CONTAINER'
        elif self.state == ScienceState.ASSAY_ANALYSIS:
            cmd_msg.data = 'BEGIN_REAGENT_MIXING'
        elif self.state == ScienceState.MISSION_COMPLETE:
            cmd_msg.data = 'ALL_ACTUATORS_STANDBY_LOG_DATA'
        elif self.state == ScienceState.FAULT:
            cmd_msg.data = 'STOP_ALL_ACTUATORS_HOLD_POSITION'
        elif self.state == ScienceState.ESTOP:
            cmd_msg.data = 'HARD_POWER_KILL'

        if cmd_msg.data:
            self.command_pub.publish(cmd_msg)

    def evaluate_state(self):
        if self.estop_active:
            self.transition_to(ScienceState.ESTOP)
            return
        if self.hardware_fault:
            self.transition_to(ScienceState.FAULT)
            return

        if self.state == ScienceState.INIT:
            if self.site_arrived:
                self.transition_to(ScienceState.SITE_SURVEY)
        elif self.state == ScienceState.SITE_SURVEY:
            if self.site_survey_complete:
                self.transition_to(ScienceState.DRILL_SAMPLING)
        elif self.state == ScienceState.DRILL_SAMPLING:
            if self.drill_current_amps > self.drill_stall_threshold:
                self.hardware_fault = True
                self.transition_to(ScienceState.FAULT)
            elif self.drill_depth_cm >= self.target_drill_depth_cm:
                self.transition_to(ScienceState.SEAL_AND_STORE)
        elif self.state == ScienceState.SEAL_AND_STORE:
            if self.sample_chamber_sealed:
                self.transition_to(ScienceState.ASSAY_ANALYSIS)
        elif self.state == ScienceState.ASSAY_ANALYSIS:
            if self.assay_progress_pct >= 100.0:
                self.transition_to(ScienceState.MISSION_COMPLETE)

    def callback_site_arrived(self, msg: Bool):
        self.site_arrived = msg.data
        self.evaluate_state()

    def callback_survey_complete(self, msg: Bool):
        self.site_survey_complete = msg.data
        self.evaluate_state()

    def callback_drill_depth(self, msg: Float32):
        self.drill_depth_cm = msg.data
        self.evaluate_state()

    def callback_drill_current(self, msg: Float32):
        self.drill_current_amps = msg.data
        self.evaluate_state()

    def callback_chamber_sealed(self, msg: Bool):
        self.sample_chamber_sealed = msg.data
        self.evaluate_state()

    def callback_assay_progress(self, msg: Float32):
        self.assay_progress_pct = msg.data
        self.evaluate_state()

    def callback_estop(self, msg: Bool):
        self.estop_active = msg.data
        self.evaluate_state()

    def control_loop(self):
        state_msg = String()
        state_msg.data = self.state.name
        self.state_pub.publish(state_msg)

def main(args=None):
    rclpy.init(args=args)
    science_node = ScienceStateMachine()
    try:
        rclpy.spin(science_node)
    except KeyboardInterrupt:
        pass
    finally:
        science_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()