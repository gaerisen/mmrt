
import cv2
import numpy as np

MODEL = "/workspaces/mmrt/src/autonomous mission fsm/fsm/fsm/face_detection_yunet_2023mar.onnx"
VIDEO = "/workspaces/mmrt/src/autonomous mission fsm/fsm/fsm/WIN_20261026_11_40_27_Pro.mp4"

INPUT_SIZE = 320
SCORE_THRESHOLD = 0.8
NMS_THRESHOLD = 0.3

# Load network directly; do not use FaceDetectorYN.
net = cv2.dnn.readNetFromONNX(MODEL)

cap = cv2.VideoCapture(VIDEO)
success, frame = cap.read()
cap.release()

if not success:
    raise RuntimeError("Could not read video frame")

original_h, original_w = frame.shape[:2]
image = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))

blob = cv2.dnn.blobFromImage(
    image,
    scalefactor=1.0,
    size=(INPUT_SIZE, INPUT_SIZE),
    mean=(0, 0, 0),
    swapRB=False,
    crop=False
)

net.setInput(blob)
outputs = net.forward(net.getUnconnectedOutLayersNames())
output_names = net.getUnconnectedOutLayersNames()
out = dict(zip(output_names, outputs))

# Decode detections from each output scale.
boxes = []
scores = []

for stride in (8, 16, 32):
    cls = out[f"cls_{stride}"].reshape(-1)
    obj = out[f"obj_{stride}"].reshape(-1)
    bbox = out[f"bbox_{stride}"].reshape(-1, 4)

    # YuNet combines face-class confidence and objectness.
    confidence = cls * obj

    feature_width = INPUT_SIZE // stride

    for i in np.where(confidence >= SCORE_THRESHOLD)[0]:
        row = i // feature_width
        col = i % feature_width

        # Decode the bounding box relative to its feature-map cell.
        x1 = (col * stride) - bbox[i, 0] * stride
        y1 = (row * stride) - bbox[i, 1] * stride
        x2 = (col * stride) + bbox[i, 2] * stride
        y2 = (row * stride) + bbox[i, 3] * stride

        boxes.append([
            float(x1),
            float(y1),
            float(x2 - x1),
            float(y2 - y1)
        ])
        scores.append(float(confidence[i]))

# Remove overlapping duplicate detections.
indices = cv2.dnn.NMSBoxes(
    boxes,
    scores,
    SCORE_THRESHOLD,
    NMS_THRESHOLD
)

face_count = len(indices) if indices is not None else 0
print("Faces detected:", face_count)

# Draw detections on the resized frame.
if face_count:
    for idx in np.array(indices).flatten():
        x, y, w, h = boxes[idx]
        x, y, w, h = map(int, (x, y, w, h))

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"{scores[idx]:.2f}",
            (x, max(15, y - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1
        )

# Save a result image so no GUI is needed in the container.
cv2.imwrite("face_detection_result.jpg", image)
print("Saved result to face_detection_result.jpg")
