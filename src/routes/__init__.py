from _route import Route, EmptyRoute
from o1 import O1Route
from test import TestRoute

routes: list[type[Route]] = [O1Route, TestRoute, EmptyRoute]

__all__ = ["Route", "routes"]
