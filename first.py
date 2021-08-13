import cv2 as cv
import json
from json import JSONEncoder
import numpy
from recognition.contour_extractor import extract_contours

capture = cv.VideoCapture(0)


def getImage(inputFrame=None):
    while inputFrame is None:
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
        frameCount += 1

    return background


bgMask = getBackground()


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


while True:
    _, image = capture.read()

    diff = cv.absdiff(bgMask.astype("uint8"), getImage(image))
    contours = extract_contours(diff)
    if len(contours) > 0:
        drawing = image.copy()
        hull_list = []
        big_hull_list = []
        for contour in contours:
            if len(contour) > 200:
                hull = cv.convexHull(contour)
                big_hull_list.append(hull)
            elif len(contour) > 50:
                hull = cv.convexHull(contour)
                hull_list.append(hull)

        colour = ()

        cv.drawContours(drawing, hull_list, -1, (0, 0, 255))
        cv.drawContours(drawing, big_hull_list, -1, (255, 0, 0))
        # if (len(big_hull_list) > 2):
        #    encodedNumpyData = json.dumps(hull_list, cls=NumpyArrayEncoder)
        #    print(encodedNumpyData)
        #    print("*****")

        cv.imshow('Contours', drawing)
    cv.imshow('Video', image)

    keyboard = cv.waitKey(30)
    if keyboard in (ord('q'), ord('Q'), 27):
        break

capture.release()
cv.destroyAllWindows()
