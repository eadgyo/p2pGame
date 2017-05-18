
class Position:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __eq__(self, position):
        return self.x == position.x and self.y == position.y

    def __ne__(self, position):
        return not self.__eq__(position)

