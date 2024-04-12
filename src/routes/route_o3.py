from _route import OffenseRoute


class O3Route(OffenseRoute):
    """ An offensive route, rushing
    """
    @staticmethod
    def name():
        return "Offense 3"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(225)
