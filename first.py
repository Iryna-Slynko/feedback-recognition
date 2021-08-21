import cv2 as cv
from json import JSONEncoder
import numpy
from recognition.contour_extractor import extract_contours
from recognition.repeated_decider import RepeatedDecider
import os
from client.api_client import ApiClient


capture = cv.VideoCapture(0)
apiClient = ApiClient(
    os.environ["API_ADDRESS"], os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]
)


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


def draw_hulls(image, hulls, colour):
    drawing = image.copy()
    cv.drawContours(drawing, hulls, -1, colour)
    cv.imshow("Contours", drawing)


def debug_output(image, big_hull_list):
    from recognition.decider import Decider

    decider = Decider(big_hull_list)
    if decider.is_decided():
        if decider.is_upvote():
            cv.drawContours(image, [big_hull_list[decider.palm_area]], -1, (0, 0, 255))
            cv.drawContours(image, [big_hull_list[decider.thumb_area]], -1, (0, 255, 0))
        else:
            cv.drawContours(image, [big_hull_list[decider.palm_area]], -1, (0, 0, 255))
            cv.drawContours(
                image, [big_hull_list[decider.thumb_area]], -1, (255, 0, 255)
            )


bg_mask = get_background()


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


decider = RepeatedDecider()
while True:
    _, image = capture.read()
    diff = cv.absdiff(bg_mask.astype("uint8"), get_image(image))
    contours = extract_contours(diff)
    if len(contours) > 0:
        #
        # hull_list = []
        big_hull_list = []
        for contour in contours:
            if len(contour) > 150:
                hull = cv.convexHull(contour)
                big_hull_list.append(hull)
        #    elif len(contour) > 50:
        #        hull = cv.convexHull(contour)
        #        hull_list.append(hull)
        decider.analyze(big_hull_list)
        # cv.drawContours(drawing, hull_list, -1, (0, 0, 255))
        # draw_hulls(image, big_hull_list, (255, 0, 0))
        if decider.is_decided():
            apiClient.record(decider.is_upvote())
        elif decider.has_input():
            text = "Thanks for"
            if decider.is_upvote():
                text += " upvoting"
                """
                cv.drawContours(
                    image, [big_hull_list[decider.palm_area]], -1, (0, 0, 255)
                )
                cv.drawContours(
                    image, [big_hull_list[decider.thumb_area]], -1, (0, 255, 0)
                )
                """
            else:
                text += " downvoting"
                """
                cv.drawContours(
                    image, [big_hull_list[decider.palm_area]], -1, (0, 0, 255)
                )
                cv.drawContours(
                    image, [big_hull_list[decider.thumb_area]], -1, (255, 0, 255)
                )
                """
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
        else:
            cv.putText(
                image,
                text="Can not recognize please move your hand",
                org=(100, 400),
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(127, 127, 127),
                thickness=2,
                lineType=cv.LINE_AA,
            )
        debug_output(image, big_hull_list)

    else:
        cv.putText(
            image,
            text="Waiting for input",
            org=(100, 400),
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(127, 127, 127),
            thickness=2,
            lineType=cv.LINE_AA,
        )

    window = cv.imshow("Video", image)

    keyboard = cv.waitKey(30)
    if keyboard in (ord("q"), ord("Q"), 27):
        break

capture.release()
cv.destroyAllWindows()
