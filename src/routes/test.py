from _route import TestRoute as TestRouteCategory
from vex import wait


class TestRoute(TestRouteCategory):
    @staticmethod
    def name():
        return "Test route"

    @staticmethod
    def run(p, d):
        while True:
            d.turn(90)
            wait(500)
