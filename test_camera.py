import cv2

cap = cv2.VideoCapture(0)

print("isOpened:", cap.isOpened())

while True:
    ret, frame = cap.read()

    print("ret =", ret)

    if not ret:
        print("Tidak bisa membaca webcam")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()