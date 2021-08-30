import cv2 as cv
from json import JSONEncoder
import numpy as np
from recognition.contour_extractor import extract_contours
from recognition.repeated_decider import RepeatedDecider
from recognition.decider2 import Decider
import os
from client.api_client import ApiClient


capture = cv.VideoCapture(0)

width = 1280
height = 720
"""
width = 1024
height = 576
"""
# capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc("M", "J", "P", "G"))
capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)

apiClient = ApiClient(
    os.environ["API_ADDRESS"], os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]
)


def get_image(inputFrame=None):
    while inputFrame is None:
        _, inputFrame = capture.read()
    hsv_image = cv.cvtColor(inputFrame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(
        hsv_image,
        np.array([0, 50, 120], dtype=np.uint8),
        np.array([180, 150, 250], dtype=np.uint8),
    )
    return mask


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
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def get_contour_center(contour):
    """Calculates the center of the contour"""
    M = cv.moments(contour)
    cx = -1
    cy = -1
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    return cx, cy


decider = RepeatedDecider()
while True:
    _, image = capture.read()
    diff = cv.absdiff(bg_mask.astype("uint8"), get_image(image))
    contours = extract_contours(get_image(image))
    rgb_image = image.copy()
    biggest = None
    biggest_area = 130
    biggest_radius = 0
    for c in contours:
        area = cv.contourArea(c)
        perimeter = cv.arcLength(c, True)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        if area > biggest_area:
            biggest_area = area
            biggest = c
            biggest_radius = radius

    if biggest is not None:
        cx, cy = get_contour_center(biggest)
        cv.circle(rgb_image, (cx, cy), (int)(biggest_radius), (0, 0, 255), 1)
        hull = cv.convexHull(biggest)
        cv.drawContours(rgb_image, [hull], -1, (255, 0, 0), 1)
        for i, point in enumerate(hull):
            cv.circle(
                rgb_image, point[0], 3, ((i * 10) % 255, (100 + i * 20) % 255, 0), 1
            )
        cv.drawContours(rgb_image, [biggest], -1, (150, 250, 150), 1)
    cv.imshow("RGB Image Contours", rgb_image)

    if decider.is_reseting():
        cv.putText(
            image,
            text="Thank you for your feedback",
            org=(100, 400),
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 127, 127),
            thickness=2,
            lineType=cv.LINE_AA,
        )
        decider.analyze([])
    elif len(contours) > 0:
        decider.analyze(contours)

        # cv.drawContours(drawing, hull_list, -1, (0, 0, 255))
        if decider.is_decided():
            white_rect = np.ones(image.shape, dtype=np.uint8) * 255
            cv.addWeighted(white_rect, 0.5, image, 0.5, 1.0)
            cv.putText(
                image,
                text="Thank you for your feedback",
                org=(100, 400),
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(0, 127, 127),
                thickness=2,
                lineType=cv.LINE_AA,
            )
            window = cv.imshow("Video", image)

            apiClient.record(decider.is_upvote())
            decider.reset()
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
