from body import Body
from line import Line
from vector import Vector
import math


class World:

    def __init__(self, g=9.81, ppm=1):
        self.g = g
        self.ppm = ppm
        self.bodies = []
        self.poc = Vector()

    def add_body(self, body):
        self.bodies.append(body)

    def update(self, dt):
        for body in self.bodies:
            if body.dynamic:
                self.integrate(body, dt)
            else:
                body.acceleration = Vector()
                body.angular_acceleration = 0
                body.velocity = Vector()
                body.angular_velocity = 0
            body.update_points()

        self.find_collisions(dt)

    def evaluate(self, body, dt, dw):
        w = body.angular_velocity + dw * dt

        return w, body.angular_acceleration

    def evaluate2D(self, body, dt, dv):
        v = body.velocity
        v = Vector(v.x + dv.x * dt, v.y + dv.y * dt)

        return v, body.acceleration

    def integrate(self, body, dt):
        body.acceleration.y -= self.g

        # linear
        a = self.evaluate2D(body, 0.0, Vector())
        b = self.evaluate2D(body, dt * 0.5, a[1])
        c = self.evaluate2D(body, dt * 0.5, b[1])
        d = self.evaluate2D(body, dt, c[1])

        dxdt = 1 / 6 * (a[0].x + 2 * (b[0].x + c[0].x) + d[0].x)
        dydt = 1 / 6 * (a[0].y + 2 * (b[0].y + c[0].y) + d[0].y)

        dvxdt = 1 / 6 * (a[1].x + 2 * (b[1].x + c[1].x) + d[1].x)
        dvydt = 1 / 6 * (a[1].y + 2 * (b[1].y + c[1].y) + d[1].y)

        body.position.x += dxdt * dt
        body.position.y += dydt * dt
        body.velocity.x += dvxdt * dt
        body.velocity.y += dvydt * dt
        body.acceleration = Vector()

        # angular
        a = self.evaluate(body, 0.0, 0)
        b = self.evaluate(body, dt * 0.5, a[1])
        c = self.evaluate(body, dt * 0.5, b[1])
        d = self.evaluate(body, dt, c[1])

        dadt = 1 / 6 * (a[0] + 2 * (b[0] + c[0]) + d[0])
        dwdt = 1 / 6 * (a[1] + 2 * (b[1] + c[1]) + d[1])

        body.angle += dadt * dt
        body.angular_velocity += dwdt * dt
        body.angular_acceleration = 0

    def find_collisions(self, dt):
        for bodyA in self.bodies:
            if not bodyA.dynamic:
                continue
            for bodyB in self.bodies:
                if bodyA == bodyB:
                    continue

                collision, poc, normal = bodyA.touches(bodyB)
                if collision:
                    self.poc = poc
                    self.resolve_collision(bodyA, bodyB, poc, normal, dt)

    def resolve_collision(self, bodyA, bodyB, poc, normal, dt):
        mult = 0.5
        if not bodyB.dynamic:
            mult = 1

        veloA = (bodyA.velocity + ((bodyA.position - poc).normal().unit() * bodyA.angular_velocity * bodyA.position.distance(poc))).dot(normal)
        impactA = Vector(veloA * normal.x * (bodyA.elasticity + mult), veloA * normal.y * (bodyA.elasticity + mult))

        veloB = (bodyB.velocity + ((bodyB.position - poc).normal().unit() * bodyB.angular_velocity * bodyB.position.distance(poc))).dot(Vector(-normal.x, -normal.y))
        impactB = Vector(veloB * normal.x * (bodyB.elasticity + 0.5), veloB * normal.y * (bodyB.elasticity + 0.5))

        net_force_x = bodyA.mass * (impactA.x / dt) + bodyB.mass * (impactB.x / dt)
        net_force_y = bodyA.mass * (impactA.y / dt) + bodyB.mass * (impactB.y / dt)

        bodyA.calc_accelerations(Vector(-net_force_x, -net_force_y), poc, normal)
        bodyB.calc_accelerations(Vector(net_force_x, net_force_y), poc, normal)
