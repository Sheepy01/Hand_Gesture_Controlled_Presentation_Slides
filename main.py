
# GESTURE DETECTION PRESENTATION MODEL

import os
import cv2
import numpy
from cvzone.HandTrackingModule import HandDetector

# Variables
width = 1280
height = 720
width_small = int(213*1)
height_small = int(120*1)
folder_path = "Presentation_Slides"
imageNumber = 0
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationNumber = 0
annotationStart = False

# Getting list of presentation Files
pathImages = sorted(os.listdir(folder_path), key=len)
print(pathImages)

# Video Capture
capture = cv2.VideoCapture(0)
capture.set(3, width)
capture.set(4, height)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Showing image
while True:
    # importing images
    success, image = capture.read()
    image = cv2.flip(image, 1)
    pathFullImage = os.path.join(folder_path, pathImages[imageNumber])
    imageCurrent = cv2.imread(pathFullImage)

    # Gesture Line
    cv2.line(image, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    # Displaying hands
    hands, image = detector.findHands(image)
    if hands and buttonPressed == False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        center_x, center_y = hand['center']

        # Getting the lmList if the Index Finger
        lmList = hand['lmList']
        xval = int(numpy.interp(lmList[8][0], [width//2, width], [0, width]))
        yval = int(numpy.interp(lmList[8][1], [150, height-150], [0, height]))
        indexFinger = xval, yval

        print(fingers)
        #print(center_x, center_y)

        # If hand is at the height of the face
        if center_y <= gestureThreshold:
            annotationStart = False

            # Gesture-1 Left
            if fingers == [1,0,0,0,0]:
                annotationStart = False                    
                print("Left")
                if imageNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imageNumber -= 1
            
            # Gesture-2 Right
            if fingers == [0,0,0,0,1]:
                annotationStart = False
                print("Right")
                if imageNumber < len(pathImages) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    imageNumber += 1

        # Gesture - 4 Showing Pointer
        if fingers == [0,1,1,0,0]:
            #print("Pointer")
            cv2.circle(imageCurrent, indexFinger, 10, (0, 0, 255), cv2.FILLED)
            annotationStart = False
            
        # Gesture - 5 Drawing Pointer Line
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
                print("Line")
                print(f"annotationNumber: ", annotationNumber)
            cv2.circle(imageCurrent, indexFinger, 10, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
            print(annotations)
        else:
            annotationStart = False

        # Gesture - 6 Undo
        if fingers == [0,1,1,1,0]:
            print("Cleared")
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True
                    print(annotationNumber)

    else:
        annotationStart = False


    # Switching between Button Pressed boolean
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(imageCurrent, annotations[i][j-1], annotations[i][j], (0,0,255), 5)

    # showing webcam on top of the slides
    image_small = cv2.resize(image, (width_small, height_small))
    slide_height, slide_width, _ = imageCurrent.shape
    imageCurrent[0:height_small, width-width_small:width] = image_small

    cv2.imshow("Image", image)
    cv2.imshow("Slides", imageCurrent)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
