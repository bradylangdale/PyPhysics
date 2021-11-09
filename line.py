from vector import Vector


class Line:

    def __init__(self, p1=Vector(), p2=Vector(1, 1)):
        self.p1 = p1
        self.p2 = p2

    def slope(self):
        if self.p2.x != self.p1.x:
            return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
        else:
            return 0

    def intersection(self, b):
        d = ((self.p1.x - self.p2.x) * (b.p1.y - b.p2.y)) - ((self.p1.y - self.p2.y) * (b.p1.x - b.p2.x))
        if d == 0:
            return False, Vector()

        u1 = ((self.p1.x - b.p1.x) * (self.p1.y - self.p2.y)) - ((self.p1.y - b.p1.y) * (self.p1.x - self.p2.x))
        t1 = ((self.p1.x - b.p1.x) * (b.p1.y - b.p2.y)) - ((self.p1.y - b.p1.y) * (b.p1.x - b.p2.x))

        t = t1 / d
        u = u1 / d

        if 0 <= t <= 1 and 0 <= u <= 1:
            return True, Vector(self.p1.x + (t * (self.p2.x - self.p1.x)),
                                self.p1.y + (t * (self.p2.y - self.p1.y)))
        else:
            return False, Vector()

    def isLeft(self, point):
        return (point.x - self.p1.x) * (self.p2.y - self.p1.y) - (point.y - self.p1.y) * (self.p2.x - self.p1.x)
