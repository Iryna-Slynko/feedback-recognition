import cv2 as cv


def extract_contours(diff):
    threshold = 29
    canny_output = cv.Canny(diff, threshold, threshold * 2)

    contours, hierarchy = cv.findContours(
        canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    filtered = []
    if hierarchy is not None and len(hierarchy[0]) > 5:

        subarray = hierarchy[0]
        for i in range(len(subarray)):
            if subarray[i][3] < 0:
                filtered.append(contours[i])
    return filtered
