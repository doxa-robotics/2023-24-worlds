from _route import EmptyRoute, Route

from route_test import TestRoute
from route_d1 import D1Route
from route_d2 import D2Route
from route_d3 import D3Route
from route_o1 import O1Route
from route_o2 import O2Route
from route_o3 import O3Route

routes: list[type[Route]] = [
    O1Route,
    O2Route,
    O3Route,
    D1Route,
    D2Route,
    D3Route,
    TestRoute,
    EmptyRoute
]

__all__ = ["Route", "routes"]
