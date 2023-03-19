
import os
import cv2

# Variables
width = 1280
height = 720
folder_path = "Presentation_Slides"

# Getting list of presentation Files
pathImages = sorted(os.listdir(folder_path), key=len)
print(pathImages)

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