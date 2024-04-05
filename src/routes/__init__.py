from _route import EmptyRoute, Route

from route_test import TestRoute
from route_d1 import D1Route
from route_d2 import D2Route
from route_d3 import D3Route
from route_d4 import D4Route
from route_d5 import D5Route
from route_d6 import D6Route
from route_o1 import O1Route
from route_o2 import O2Route
from route_o3 import O3Route
from route_o4 import O4Route
from route_o5 import O5Route

routes: list[type[Route]] = [
    # D1Route,
    D2Route,
    D3Route,
    D4Route,
    D5Route,
    D6Route,

    O1Route,
    O2Route,
    O3Route,
    O4Route,
    O5Route,

    TestRoute,
    EmptyRoute
]

__all__ = ["Route", "routes"]
