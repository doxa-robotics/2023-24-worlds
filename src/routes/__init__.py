from _route import EmptyRoute, Route
from route_d3 import D3Route
from route_d5 import D5Route
from route_o2 import O2Route
from route_o3 import O3Route
from route_o5 import O5Route
from route_o6 import O6Route
from route_test import TestRoute

routes: list[type[Route]] = [
    D3Route,
    D5Route,

    O2Route,
    O3Route,
    O5Route,
    O6Route,

    TestRoute,
    EmptyRoute
]

__all__ = ["Route", "routes"]
