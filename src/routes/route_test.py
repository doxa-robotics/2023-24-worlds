from _route import TestRoute as TestRouteCategory
from vex import wait


class TestRoute(TestRouteCategory):
    @staticmethod
    def name():
        return "Test route"

    @staticmethod
    def run(p, d):
        d.drive(1000)
        p.brain.screen.set_fill_color(0xff0000)
        p.brain.screen.draw_rectangle(0, 0, 500, 500)
        p.brain.screen.render()
