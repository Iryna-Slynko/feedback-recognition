class Decider:
    def __init__(self, np_array):
        self.upvote = True
        self.decided = True
        self.__process__(np_array)

    def __process__(self, np_array):
        if len(np_array) < 2:
            self.decided = False
            return
        thumb_area = np_array[0]
        palm_area = np_array[0]
        for block in np_array:
            if len(block) > len(palm_area):
                palm_area = block
            elif len(block) < len(thumb_area):
                thumb_area = block

        def give_me_center(block):
            total_x = 0
            total_y = 0
            for point in block:
                x = point[0][0]
                y = point[0][1]
                total_x += x
                total_y += y
            return (total_x / len(block), total_y / len(block))

        _, thumb_y = give_me_center(thumb_area)
        _, palm_y = give_me_center(palm_area)
        self.upvote = thumb_y < palm_y

    def is_upvote(self):
        return self.upvote

    def is_decided(self):
        return self.decided
