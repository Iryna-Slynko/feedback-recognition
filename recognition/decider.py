class Dimension:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def aspect_ratio(self):
        if self.height > 0:
            return self.width / self.height

        return self.width

    def wider(self, other_dimension):
        return self.aspect_ratio > other_dimension.aspect_ratio


class Decider:
    def __init__(self, np_array):
        self.upvote = True
        self.decided = True
        self.__process__(np_array)

    def __process__(self, np_array):
        if len(np_array) < 2:
            self.decided = False
            return

        dimensions = []

        def give_me_dimensions(block):
            min_x = block[0][0][0]
            min_y = block[0][0][1]
            max_x = block[0][0][0]
            max_y = block[0][0][1]
            for point in block:
                x = point[0][0]
                y = point[0][1]
                if min_x > x:
                    min_x = x
                elif max_x < x:
                    max_x = x
                if min_y > y:
                    min_y = y
                elif max_y < y:
                    max_y = y
            return Dimension(min_x, min_y, max_x, max_y)

        self.thumb_area = 0
        self.palm_area = 0
        i = 0

        for i, hull in enumerate(np_array):
            hull_rectangle = give_me_dimensions(hull)
            dimensions.append(hull_rectangle)
            if hull_rectangle.wider(dimensions[self.palm_area]):
                self.palm_area = i
            elif dimensions[self.thumb_area].wider(hull_rectangle):
                self.thumb_area = i

        if dimensions[self.thumb_area].aspect_ratio < 0.2:
            print(
                "Too low aspect ratio {}".format(
                    dimensions[self.thumb_area].aspect_ratio
                )
            )
            self.decided = False
        if dimensions[self.thumb_area].y2 > dimensions[self.palm_area].y2:
            self.upvote = True  # thumb_y < palm_y
        elif dimensions[self.thumb_area].y1 < dimensions[self.palm_area].y1:
            self.upvote = False
        else:
            print(
                "Position is too hard thumb {} palm {}",
                dimensions[self.thumb_area],
                dimensions[self.palm_area],
            )
            self.decided = False

    def is_upvote(self):
        return self.upvote

    def is_decided(self):
        return self.decided

    def __thumb_area(self):
        return self.thumb_area

    def __palm_area(self):
        return self.palm_area
