import cv2
import mediapipe as mp

print("STEP 1")

mp_hands = mp.solutions.hands
print("STEP 2")

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

print("STEP 3")

mp_draw = mp.solutions.drawing_utils
print("STEP 4")

cap = cv2.VideoCapture(0)
print("STEP 5")

if not cap.isOpened():
    print("Webcam gagal dibuka!")
    exit()

print("STEP 6")

while True:
    success, frame = cap.read()

    if not success:
        print("Gagal membaca frame")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()