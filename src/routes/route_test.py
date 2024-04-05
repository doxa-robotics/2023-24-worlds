from math import cos, pi, sin
from _route import TestRoute as TestRouteCategory


class TestRoute(TestRouteCategory):
    @staticmethod
    def name():
        return "Test route"

    @staticmethod
    def run(p, d):
        p.brain.screen.draw_circle(100, 100, 30, 0xaaaaaa)
        p.brain.screen.set_pen_color(0xff0000)
        p.brain.screen.draw_line(100, 100, cos(
            p.inertial.heading() / 180 * pi)*30+100, sin(p.inertial.heading() / 180 * pi)*30+100)
        p.brain.screen.render()

        d.drive(1000)
        p.brain.screen.set_fill_color(0xff0000)
        p.brain.screen.draw_rectangle(0, 0, 50, 50)
        p.brain.screen.set_pen_color(0x00ff00)
        p.brain.screen.draw_line(100, 100, cos(
            p.inertial.heading() / 180 * pi)*30+100, sin(p.inertial.heading() / 180 * pi)*30+100)
        p.brain.screen.render()

        d.turn(180)
        p.brain.screen.set_fill_color(0x00ff00)
        p.brain.screen.draw_rectangle(0, 50, 50, 50)

        p.brain.screen.set_pen_color(0x0000ff)
        p.brain.screen.draw_line(100, 100, cos(
            p.inertial.heading() / 180 * pi)*30+100, sin(p.inertial.heading() / 180 * pi)*30+100)
        p.brain.screen.render()
