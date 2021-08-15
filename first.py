import cv2 as cv
from json import JSONEncoder
import numpy
from recognition.contour_extractor import extract_contours
from recognition.decider import Decider

capture = cv.VideoCapture(0)


def get_image(inputFrame=None):
    while inputFrame is None:
        _, inputFrame = capture.read()
    gray = cv.cvtColor(inputFrame, cv.COLOR_BGR2GRAY)
    # gray = cv.GaussianBlur(gray, (11, 11), 10)
    return gray


def get_background():
    while not capture.read():
        print("Waiting")
    background = get_image().copy().astype("float")
    frame_count = 0
    while frame_count < 30:
        cv.accumulateWeighted(get_image(), background, 0.5)
        frame_count += 1

    return background


def print_info(info):
    import json

    encodedNumpyData = json.dumps(info, cls=NumpyArrayEncoder)
    print(encodedNumpyData)


bg_mask = get_background()


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


while True:
    _, image = capture.read()

    diff = cv.absdiff(bg_mask.astype("uint8"), get_image(image))
    contours = extract_contours(diff)
    if len(contours) > 0:
        # drawing = image.copy()
        # hull_list = []
        big_hull_list = []
        for contour in contours:
            if len(contour) > 150:
                hull = cv.convexHull(contour)
                big_hull_list.append(hull)
        #    elif len(contour) > 50:
        #        hull = cv.convexHull(contour)
        #        hull_list.append(hull)
        decider = Decider(big_hull_list)
        # cv.drawContours(drawing, hull_list, -1, (0, 0, 255))
        # cv.drawContours(drawing, big_hull_list, -1, (255, 0, 0))

        # cv.imshow('Contours', drawing)
        if decider.is_decided():
            text = "Thanks for"
            if decider.is_upvote():
                text += " upvoting"
            else:
                text += " downvoting"
            cv.putText(
                image,
                text=text,
                org=(100, 400),
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(57, 127, 127),
                thickness=2,
                lineType=cv.LINE_AA,
            )
    window = cv.imshow("Video", image)

    keyboard = cv.waitKey(30)
    if keyboard in (ord("q"), ord("Q"), 27):
        break

capture.release()
cv.destroyAllWindows()
