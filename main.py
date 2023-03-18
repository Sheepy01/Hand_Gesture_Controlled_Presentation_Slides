
import cv2

# Video variables
width = 1280
height = 720

# Video Capture
capture = cv2.VideoCapture(0)
capture.set(3, width)
capture.set(4, height)

# Showing image
while True:
    success, image = capture.read()
    cv2.imshow("Image", image)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break