import cv2

URL1 = "http://192.168.43.1:8080/video"
URL2 = "http://192.168.43.71:8080/video"

cam1 = cv2.VideoCapture(URL1)
cam2 = cv2.VideoCapture(URL2)

print("Otwarcie kamery 1:", cam1.isOpened())
print("Otwarcie kamery 2:", cam2.isOpened())
print("Naciśnij Q, aby zakończyć.")

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if ret1:
        cv2.imshow("Kamera 1", frame1)
    if ret2:
        cv2.imshow("Kamera 2", frame2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam1.release()
cam2.release()
cv2.destroyAllWindows()
