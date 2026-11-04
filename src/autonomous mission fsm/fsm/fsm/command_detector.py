from yolozone import PoseDetector
from enum import Enum
import cv2

class Command(Enum):
    FOLLOW = "follow"
    STAY = "stay"
    FETCH = "fetch"
    COME = "come"
    GIVE = "give"

COLORS = {
    Command.STAY: (0, 0, 255),
    Command.COME: (0, 255, 0),
}
DEFAULT_COLOR = (45, 184, 241)

def get_measurements(detector, keypoints):
    person = keypoints.xy[0]

    return {
        'left_arm': detector.angle_between_3_points(keypoints, 5, 7, 9)[0],
        'right_arm': detector.angle_between_3_points(keypoints, 6, 8, 10)[0],
        'left_shoulder': detector.angle_between_3_points(keypoints, 11, 5, 7)[0],
        'right_shoulder': detector.angle_between_3_points(keypoints, 12, 6, 8)[0],
        'left_elbow_shoulder_dy': abs(float(person[5][1] - person[7][1])),
        'right_elbow_shoulder_dy': abs(float(person[6][1] - person[8][1])),
    }

def is_follow(measurements):
    pass

def is_stay(measurements):
    # mostly straight arms, elbows roughly in line with shoulders
    # 40 = max pixels elbow is above or below shoulder.
    return (measurements["left_arm"] >= 90 and measurements["right_arm"] >= 90
            and measurements["left_elbow_shoulder_dy"] < 40 and measurements["right_elbow_shoulder_dy"] < 40)

def is_fetch(measurements):
    pass

def is_come(measurements):
    # arms bent and down
    return (measurements["left_arm"] <= 70 and measurements["right_arm"] <= 70
            and measurements["left_shoulder"] <= 45 and measurements["right_shoulder"] <= 45)

def is_give(measurements):
    pass

def detect_command(measurements):
    if is_stay(measurements):
        return Command.STAY
    if is_come(measurements):
        return Command.COME
    return None

def draw_skeleton(detector, keypoints, frame, color):
    points, lines = detector.draw_pose(keypoints)
    for point in points:
        cv2.circle(frame, point, 5, (0, 0, 0), 2)
    for start, end in lines:
        cv2.line(frame, start, end, color, 2)
    return frame

def display_angles(frame, m):
    y_pos = 30
    for name, value in m.items():
        cv2.putText(frame, f"{name}: {value:.1f}°", (10, y_pos), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y_pos += 25


# def main():
#     cam = cv2.VideoCapture(0) #you an also put a video path here

#     frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

#     detector = PoseDetector(model='yolov8n-pose.pt')

#     while True:
#         got_frame, frame = cam.read()
#         if not got_frame:
#             break

#         keypoints = detector.find_keypoints(frame)
#         if keypoints is not None and keypoints.xy.shape[0] > 0:
#             measurements = get_measurements(detector, keypoints)
#             command = detect_command(measurements)
#             color = COLORS.get(command, DEFAULT_COLOR)
 
#             frame = draw_skeleton(detector, keypoints, frame, color)
#             # display_angles(frame, measurements)

#         cv2.imshow("Camera", frame)
#         if cv2.waitKey(1) == ord('q'):
#             break

#     cam.release()
#     out.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()