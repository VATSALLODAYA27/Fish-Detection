# live.py → FIXED: No double labels, only your 34 fish names
import cv2
from ultralytics import YOLO

# Load model
model = YOLO('model.pt')

# Your 34 fish classes
class_map = {
    0: "Anabas", 1: "Bangus", 2: "Black Spotted Barb", 3: "Clarias", 4: "Clownfish",
    5: "Common Silver Carp", 6: "Fighting Fish", 7: "Nile Tilapia", 8: "Pangasiidae",
    9: "Rainbowfish", 10: "Red Tilapia Fish", 11: "Silver Angelfish", 12: "Siriped Catfish",
    13: "Spotted Featherback", 14: "Tilapia", 15: "aair", 16: "boal", 17: "catfish",
    18: "chapila", 19: "deshi puti", 20: "foli", 21: "goldfish", 22: "ilish",
    23: "kal baush", 24: "katla", 25: "koi", 26: "magur", 27: "mrigel", 28: "pabda",
    29: "pangas", 30: "puti", 31: "rui", 32: "shol", 33: "taki"
}

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run inference
    results = model(frame, conf=0.3, verbose=False)[0]

    # Draw ONLY our custom boxes and labels
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        conf = box.conf[0].item()
        cls_id = int(box.cls[0].item())
        label = f"{class_map.get(cls_id, 'Unknown')} {conf:.2f}"

        # Beautiful green box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        # Background for text
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), (0, 255, 0), -1)
        
        # White text
        cv2.putText(frame, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show FPS
    cv2.putText(frame, f"FPS: {int(cap.get(cv2.CAP_PROP_FPS))}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Live Fish Detection - 34 Species", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()