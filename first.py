import cv2 as cv
import numpy as np
import random as rng

capture = cv.VideoCapture(0)

def getImage(inputFrame=None):
    if inputFrame is None:
        _, inputFrame = capture.read()
    gray = cv.cvtColor(inputFrame, cv.COLOR_BGR2GRAY)
    # gray = cv.GaussianBlur(gray, (11, 11), 10)
    return gray


def getBackground():
    while not capture.read():
        print("Waiting")
    background = getImage().copy().astype("float")
    frameCount = 0
    while frameCount < 30:
        cv.accumulateWeighted(getImage(), background, 0.5)
        frameCount+=1
    return background

bgMask = getBackground()

def extractContours():
    threshold = 29
    canny_output = cv.Canny(diff, threshold, threshold * 2)
    
    cv.imshow('FG Mask', canny_output)
    contours, hierarchy = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

while True:
    _, image = capture.read()
    
    diff = cv.absdiff(bgMask.astype("uint8"), getImage(image))
    contours = extractContours()
    if len(contours) > 0:
        drawing = image.copy()
        hull_list = []
        for contour in contours:
            if len(contour)>200:
                hull = cv.convexHull(contour)
                hull_list.append(hull)
        
        colour = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        
        cv.drawContours(drawing, hull_list, -1, colour)
        cv.imshow('Contours', drawing)
    cv.imshow('Video', image)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 'Q' or keyboard == 27:
        break

capture.release()
cv.destroyAllWindows()
