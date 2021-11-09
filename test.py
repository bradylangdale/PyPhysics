from world import World
from body import Body
from vector import Vector
import pyglet
from pyglet import shapes
import math

world = World()
world.g = 4

points1 = [Vector(), Vector(60, 0), Vector(60, 10), Vector(0, 10)]
points2 = [Vector(), Vector(8, 0), Vector(8, 12), Vector(0, 12)]
points3 = [Vector(), Vector(10, 0), Vector(10, 1000), Vector(0, 1000)]
body = Body(points=points1, position=Vector(15, 0), dynamic=False)
body2 = Body(points=points2, position=Vector(2, 15), velocity=Vector(0, 4), angle=0.1, mass=1, elasticity=0.1)
body3 = Body(points=points2, position=Vector(17, 30), velocity=Vector(-0.5, 0), angle=0.1, mass=1, elasticity=0.1)
body4 = Body(points=points2, position=Vector(17, 50), velocity=Vector(0, 4), angle=0.1, mass=1, elasticity=0.1)
body5 = Body(points=points2, position=Vector(2, 40), velocity=Vector(0, 0), angle=0.1, mass=1, elasticity=0.1)
body6 = Body(points=points3, position=Vector(-25, 0), dynamic=False)
body7 = Body(points=points3, position=Vector(35, 0), dynamic=False)

world.add_body(body)
world.add_body(body2)
world.add_body(body3)
world.add_body(body4)
world.add_body(body5)
world.add_body(body6)
world.add_body(body7)

window = pyglet.window.Window()
batch = pyglet.graphics.Batch()

box1 = shapes.Rectangle(0, 0, 300, 50, color=(255, 0, 0), batch=batch)
box1.anchor_position = (150, 25)
box2 = shapes.Rectangle(40, 500, 40, 60, color=(0, 255, 0), batch=batch)
box2.anchor_position = (20, 30)
box3 = shapes.Rectangle(40, 500, 40, 60, color=(0, 255, 0), batch=batch)
box3.anchor_position = (20, 30)
box4 = shapes.Rectangle(40, 500, 40, 60, color=(0, 255, 0), batch=batch)
box4.anchor_position = (20, 30)
box5 = shapes.Rectangle(40, 500, 40, 60, color=(0, 255, 0), batch=batch)
box5.anchor_position = (20, 30)

circle = shapes.Circle(0, 0, 3, batch=batch)
circle1 = shapes.Circle(0, 0, 2, batch=batch)
circle2 = shapes.Circle(0, 0, 2, batch=batch)
circle3 = shapes.Circle(0, 0, 2, batch=batch)
circle4 = shapes.Circle(0, 0, 2, batch=batch)


@window.event
def on_draw():
    window.clear()
    batch.draw()


def update(dt):
    world.update(0.02)

    circle.position = (world.poc.x * 5 + 100, world.poc.y * 5 + 20)

    circle1.position = (world.bodies[2].points[0].x * 5 + 100, world.bodies[2].points[0].y * 5 + 20)
    circle2.position = (world.bodies[2].points[1].x * 5 + 100, world.bodies[2].points[1].y * 5 + 20)
    circle3.position = (world.bodies[2].points[2].x * 5 + 100, world.bodies[2].points[2].y * 5 + 20)
    circle4.position = (world.bodies[2].points[3].x * 5 + 100, world.bodies[2].points[3].y * 5 + 20)

    box1.position = (world.bodies[0].position.x * 5 + 100,
                     world.bodies[0].position.y * 5 + 20)
    box1.rotation = math.degrees(-world.bodies[0].angle)

    box2.position = (world.bodies[1].position.x * 5 + 100,
                     world.bodies[1].position.y * 5 + 20)
    box2.rotation = math.degrees(-world.bodies[1].angle)

    box3.position = (world.bodies[2].position.x * 5 + 100,
                     world.bodies[2].position.y * 5 + 20)
    box3.rotation = math.degrees(-world.bodies[2].angle)

    box4.position = (world.bodies[3].position.x * 5 + 100,
                     world.bodies[3].position.y * 5 + 20)
    box4.rotation = math.degrees(-world.bodies[3].angle)

    box5.position = (world.bodies[4].position.x * 5 + 100,
                     world.bodies[4].position.y * 5 + 20)
    box5.rotation = math.degrees(-world.bodies[4].angle)


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
