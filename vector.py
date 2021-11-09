import math


class Vector:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def cross(self, b):
        return (self.x * b.y) - (self.y * b.x)

    def normal(self, b=None):
        if b is None:
            return Vector(self.y, -self.x)
        else:
            return Vector(math.copysign(self.y, b.y), math.copysign(self.x, b.x))

    def dot(self, b):
        return (self.x * b.x) + (self.y * b.y)

    def unit(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector()
        else:
            return Vector(self.x / mag, self.y / mag)

    def distance(self, b):
        return math.sqrt((self.x - b.x)**2 + (self.y - b.y)**2)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "{0}, {1}".format(self.x, self. y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __neg__(self):
        return Vector(-self.x, -self.y)
