from _route import EmptyRoute, Route
from route_disrupt_d import DisruptDRoute
from route_five_ball import FiveBallRoute
from route_rush_o import RushORoute
from route_safe_d import SafeDRoute
from route_safe_o import SafeORoute
from route_six_ball import SixBallRoute
from route_test import TestRoute

routes: list[type[Route]] = [
    SafeDRoute,
    DisruptDRoute,

    SafeORoute,
    RushORoute,
    FiveBallRoute,
    SixBallRoute,

    TestRoute,
    EmptyRoute
]

__all__ = ["Route", "routes"]
