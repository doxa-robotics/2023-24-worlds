from _route import EmptyRoute, Route
from route_o1 import O1Route
from route_test import TestRoute
from route_d1 import D1Route

routes: list[type[Route]] = [O1Route, D1Route, TestRoute, EmptyRoute]

__all__ = ["Route", "routes"]
