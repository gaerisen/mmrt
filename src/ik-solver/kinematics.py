# ---------------------------------------------------------------------------
# Inverse kinematics for the rover arm
# Made by spencer with syntactical help from claude
#
# Frame: x = forward, y = left/right (along the slide), z = up.
# Units: meters and radians.
#
# Inputs (the target you want the claw to reach)
#   x, y, z     target claw tip position, measured from the base frame origin
#   pitch       angle the claw points, measured from horizontal (+ = up)
#   roll        rotation of the claw about its own pointing axis
#   elbow_up    True = elbow bends above the shoulder-wrist line
#
# Geometry (ArmGeometry, fixed for this arm)
#   l1          length from shoulder pivot to elbow pivot
#   l2          length from elbow pivot to wrist pitch pivot
#   l3          length from wrist pitch pivot to claw tip
#   shoulder_x  shoulder pivot position relative to the base frame
#   shoulder_z
#   slide_min   linear slide travel limits
#   slide_max
#
# Intermediate Values (inside solve_planar)
#   px, pz      target claw tip position, measured from the shoulder
#   wx, wz      wrist pitch pivot position, measured from the shoulder
#   r_sq        squared distance from shoulder to wrist (wx^2 + wz^2)
#   cos_elbow   cosine of the elbow bend, from the law of cosines
#
# Outputs (JointSolution)
#   slide        linear slide position
#   shoulder     angle of link 1 above horizontal
#   elbow        angle of link 2 relative to link 1 (0 = straight)
#   wrist_pitch  angle of link 3 relative to link 2
#   wrist_roll   claw rotation about its pointing axis
#
# Note: shoulder + elbow + wrist_pitch = pitch
# ---------------------------------------------------------------------------

from dataclasses import dataclass
import math

# There are 3 main parts to the solution.
# The linear slide. (y axis)
# The shoulder/elbow/wrist_pitch angles (x/z plane)
# The wrist_roll angle. 
# With the way the arm is designed, these three parts are independent of each other, so they can be solved separately.
# So to get the solution, we just solve each part and combine the results.

class UnreachableError(ValueError):
    """Target is outside the arm's reach."""


@dataclass(frozen=True)
class ArmGeometry:
    l1: float
    l2: float
    l3: float
    shoulder_x: float
    shoulder_z: float
    slide_min: float
    slide_max: float


@dataclass(frozen=True)
class JointSolution:
    slide: float
    shoulder: float
    elbow: float
    wrist_pitch: float
    wrist_roll: float
 
    def as_list(self) -> list[float]:
        return [self.slide, self.shoulder, self.elbow,
                self.wrist_pitch, self.wrist_roll]

@dataclass(frozen=True)
class ClawTipPosition:
    x: float
    y: float
    z: float


def wrap_angle(angle: float) -> float:
    """Wrap angle to be within [-pi, pi]."""
    return (angle + math.pi) % (2 * math.pi) - math.pi


# Linear Slide Calculation

def solve_slide(y: float, geo: ArmGeometry) -> float:
    if not geo.slide_min <= y <= geo.slide_max:
        raise UnreachableError(f'y={y:.3f} outside slide range [{geo.slide_min}, {geo.slide_max}]')
    return y


# Shoulder/Elbow/Wrist Pitch Calculation

def solve_planar(x: float, z: float, pitch: float, geo: ArmGeometry, elbow_up: bool = True) -> tuple[float, float, float]:
    px = x - geo.shoulder_x # distance from shoulder to tip of the tool
    pz = z - geo.shoulder_z

    wx = px - geo.l3 * math.cos(pitch) # distance from shoulder to wrist 
    wz = pz - geo.l3 * math.sin(pitch)
    r_sq = wx * wx + wz * wz # distance formula

    # law of cosines for the elbow.
    cos_elbow = (r_sq - geo.l1 ** 2 - geo.l2 ** 2) / (2.0 * geo.l1 * geo.l2)
    if abs(cos_elbow) > 1.0 + 1e-9: # for rounding error Purposes
        raise UnreachableError(f'wrist point ({wx:.3f}, {wz:.3f}) is out of reach of links 1+2')
    cos_elbow = max(-1.0, min(1.0, cos_elbow)) # clamp float noise
 
    elbow = math.acos(cos_elbow)
    if elbow_up:
        elbow = -elbow  # negative bend puts the elbow above the shoulder-wrist line
 
    shoulder = math.atan2(wz, wx) - math.atan2(
        geo.l2 * math.sin(elbow), geo.l1 + geo.l2 * math.cos(elbow)) # use atan2 for quadrant awareness
 
    # whatever pitch is left over goes to the wrist.
    wrist_pitch = pitch - shoulder - elbow
 
    return wrap_angle(shoulder), wrap_angle(elbow), wrap_angle(wrist_pitch)


# Wrist Roll Calculation

def solve_wrist_roll(roll: float) -> float:
    return wrap_angle(roll)


# Full Solve

def solve(x: float, y: float, z: float, pitch: float, roll: float, geo: ArmGeometry, elbow_up: bool = True) -> JointSolution:
    slide = solve_slide(y, geo)
    shoulder, elbow, wrist_pitch = solve_planar(x, z, pitch, geo, elbow_up)
    wrist_roll = solve_wrist_roll(roll)
    return JointSolution(slide, shoulder, elbow, wrist_pitch, wrist_roll)

# Outputs (JointSolution)
#   slide        linear slide position
#   shoulder     angle of link 1 above horizontal
#   elbow        angle of link 2 relative to link 1 (0 = straight)
#   wrist_pitch  angle of link 3 relative to link 2
#   wrist_roll   claw rotation about its pointing axis

#class ClawTipPosition:
#    x: float
#    y: float
#    z: float

def fk_solver(joint_solution: JointSolution, geo: ArmGeometry) -> ClawTipPosition:
    slide = joint_solution.slide
    shoulder = joint_solution.shoulder
    elbow = joint_solution.elbow
    wrist_pitch = joint_solution.wrist_pitch

    l1_x = geo.l1 * math.cos(shoulder)
    l1_z = geo.l1 * math.sin(shoulder)

    l2_x = geo.l2 * math.cos(shoulder + elbow)
    l2_z = geo.l2 * math.sin(shoulder + elbow)

    l3_x = geo.l3 * math.cos(shoulder + elbow + wrist_pitch)
    l3_z = geo.l3 * math.sin(shoulder + elbow + wrist_pitch)

    lx = l1_x + l2_x + l3_x
    lz = l1_z + l2_z + l3_z

    x = geo.shoulder_x + lx
    y = slide
    z = geo.shoulder_z + lz

    return ClawTipPosition(x=x, y=y, z=z)
    

def main():
    # Example usage
    geo = ArmGeometry(
        l1=100.0, l2=100.0, l3=100.0,
        shoulder_x=0.0, shoulder_z=0.0,
        slide_min=-0.1, slide_max=0.1
    )
    try:
        solution = solve(52.5, -0.1, 87.4527, math.radians(30), math.radians(45), geo)
        print("Joint Solution:", "\n", "\n".join(f"{name}: {value*180/math.pi:.3f}" for name, value in zip(solution.__dataclass_fields__.keys(), solution.as_list())))
        tip = fk_solver(solution, geo)
        print(f"FK: x={tip.x:.6f}, y={tip.y:.6f}, z={tip.z:.6f}")
    except UnreachableError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()