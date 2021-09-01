import cv2 as cv


class Decider:
    def __init__(self, contours):
        self.decided = False
        self.upvote = False

        biggest = None
        biggest_area = 130
        for c in contours:
            area = cv.contourArea(c)
            if area > biggest_area:
                biggest_area = area
                biggest = c
        if biggest is None:
            return

        tmp = cv.convexHull(biggest)
        # points in convex hull are wrapped into one more array
        hull = [point[0] for point in tmp]
        # bubble sort is sufficient since the context hull will have 50 items max and usually have 25
        for i in range(len(hull) - 1):
            for j in range(0, len(hull) - i - 1):
                if hull[j][0] > hull[j + 1][0]:
                    tmp = hull[j + 1]
                    hull[j + 1] = hull[j]
                    hull[j] = tmp
        """
        Assumption:
            For upvote the hull will have its angle on the top,
            for downvote the hull will have its angle to the down

            The angle would be a group of dots thathave their x coordinates relatively far from two extremes
            if the y for that group would be significantly higher that for sides, that would mean downvote 
            otherwise if the y coordinate for that group is smaller, then it is upvote

            To check it we need coordinates for y on the left and right part of the hull.
            They can go up and down closer to the edge, 
            so we will have ten extra pixels to get upper and bottom side 
            and will check the max and min y coordinates on these sides.
            (top/bottom y)

            For the y in the middle we will just check to most top and bottom that are far from edges
        """

        left_x = hull[0][0]
        left_top_y = hull[0][1]
        left_bottom_y = hull[0][1]
        right_x = hull[-1][0]
        right_bottom_y = hull[-1][0]
        right_top_y = hull[-1][0]
        middle_top_y = left_bottom_y
        middle_top_x = hull[0][0]
        middle_bottom_x = hull[0][0]
        middle_bottom_y = left_top_y
        for point in hull:
            if (point[0] - left_x) < 15:
                if point[1] > left_bottom_y:
                    left_bottom_y = point[1]
                elif point[1] < left_top_y:
                    left_top_y = point[1]
            elif (right_x - point[0]) < 15:
                if point[1] > right_bottom_y:
                    right_bottom_y = point[1]
                elif point[1] < right_top_y:
                    right_top_y = point[1]
            elif point[1] > middle_bottom_y:
                middle_bottom_y = point[1]
                middle_bottom_x = point[0]
            elif point[1] < middle_top_y:
                middle_top_y = point[1]
                middle_top_x = point[0]

        if (middle_bottom_y - left_bottom_y) > 80 or (
            middle_bottom_y - right_bottom_y
        ) > 80:
            self.upvote = False
            self.decided = True

        if (left_top_y - middle_top_y) > 80 or (right_top_y - middle_top_y) > 80:
            if self.upvote:
                pass
            else:
                self.upvote = True
                self.decided = True

    def is_upvote(self):
        return self.upvote

    def is_decided(self):
        return self.decided
