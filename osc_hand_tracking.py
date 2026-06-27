import cv2
import mediapipe as mp
from pythonosc.udp_client import SimpleUDPClient

# ==========================
# OSC
# ==========================
client = SimpleUDPClient("127.0.0.1", 8000)

# ==========================
# MediaPipe
# ==========================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ==========================
# Webcam
# ==========================
cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # gambar landmark
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Ambil ujung telunjuk (landmark 8)
            index_tip = hand_landmarks.landmark[8]

            x = index_tip.x
            y = index_tip.y

            # Kirim ke TouchDesigner
            client.send_message("/hand/x", x)
            client.send_message("/hand/y", y)

            # Tampilkan di layar
            cv2.putText(
                frame,
                f"X:{x:.2f}  Y:{y:.2f}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

    cv2.imshow("OSC Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()