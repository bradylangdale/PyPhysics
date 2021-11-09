from vector import Vector
from line import Line
import math


class Body:

    def __init__(self, points=(), position=Vector(), velocity=Vector(), acceleration=Vector(),
                 angle=0, angular_velocity=0, angular_acceleration=0, mass=1,
                 lin_drag=0, rot_drag=0, elasticity=1, dynamic=True, user=None):
        self._points = points
        self.points = []
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.angular_acceleration = angular_acceleration
        self.mass = mass
        self.lin_drag = lin_drag
        self.rot_drag = rot_drag
        self.elasticity = elasticity
        self.dynamic = dynamic
        self.user = user

        self._center = Vector()

        for point in points:
            self._center.x += point.x
            self._center.y += point.y

        self._center.x /= len(points)
        self._center.y /= len(points)

        self.update_points()

    def update_points(self):
        self.points.clear()
        self.center = self.position - self._center

        for point in self._points:
            r = point.distance(self._center)
            p = Vector(self._center.x - (r * math.cos(self.angle + math.atan2(self._center.y - point.y,
                                                                              self._center.x - point.x))),
                       self._center.y - (r * math.sin(self.angle + math.atan2(self._center.y - point.y,
                                                                              self._center.x - point.x))))
            p += self.center
            self.points.append(p)

    def moment_of_inertia(self, axis):
        working_points = []
        for point in self.points:
            working_points.append(Vector(point.x + axis.x, point.y + axis.y))

        moment = 0
        for i in range(-1, len(working_points) - 1):
            p1 = working_points[i]
            p2 = working_points[i + 1]
            moment += (p1.x * p2.y - p2.x * p1.y) * (p1.x * p2.y + 2 * p1.x * p1.y + 2 * p2.x * p2.y + p2.x * p1.y)

        return 0.001 * abs(moment)

    def intersects(self, lineB):
        for a in range(-1, len(self.points) - 1):
            collision, _ = Line(self.points[a], self.points[a + 1]).intersection(lineB)
            if collision:
                return True

        return False

    def point_inside(self, lineA, lineB, bodyB):
        if math.copysign(1, lineB.isLeft(lineA.p1)) == math.copysign(1, lineB.isLeft(bodyB.position)):
            return True, False, lineA.p1

        if math.copysign(1, lineB.isLeft(lineA.p2)) == math.copysign(1, lineB.isLeft(bodyB.position)):
            return True, False, lineA.p2

        if math.copysign(1, lineA.isLeft(lineB.p1)) == math.copysign(1, lineA.isLeft(self.position)):
            return True, True, lineB.p1

        if math.copysign(1, lineA.isLeft(lineB.p2)) == math.copysign(1, lineA.isLeft(self.position)):
            return True, True, lineB.p2

        return False, False, Vector()

    def touches(self, bodyB):
        poc = None
        normal = Vector()
        for a in range(-1, len(self.points) - 1):
            lineA = Line(self.points[a], self.points[a + 1])
            for b in range(-1, len(bodyB.points) - 1):
                lineB = Line(bodyB.points[b], bodyB.points[b + 1])
                collision, point = lineA.intersection(lineB)
                if collision:
                    hasPoint, is_b, p_inside = self.point_inside(lineA, lineB, bodyB)
                    if hasPoint:
                        if is_b:
                            normA = (lineA.p2 - lineA.p1).normal()
                            contact, pocA = lineA.intersection(Line(p_inside - normA, p_inside + normA))
                            if contact:
                                depth = p_inside.distance(pocA)
                                self.position += normA.unit() * depth
                                print(depth, contact)
                                self.update_points()
                                poc = pocA
                                normal = normA.unit()
                        else:
                            normB = (lineB.p2 - lineB.p1).normal()
                            contact, pocB = lineB.intersection(Line(p_inside - normB, p_inside + normB))
                            if contact:
                                depth = p_inside.distance(pocB)
                                self.position += normB.unit() * depth
                                self.update_points()
                                poc = pocB
                                normal = normB.unit()

        if poc is None:
            return False, Vector(), Vector()
        else:
            return True, poc, normal

    def calc_accelerations(self, net_force, poc, normal):
        if not self.dynamic:
            return

        self.acceleration += Vector(net_force.x / self.mass, net_force.y / self.mass)

        norm = Line(self.position + normal, self.position - normal)
        torque = abs((self.position - poc).cross(net_force)) * math.copysign(1, norm.isLeft(poc))
        moi = self.moment_of_inertia(poc)

        if moi > 1:
            self.angular_acceleration -= torque / (moi * self.mass)
