import math


class BicycleModel:

    def __init__(self, track, base, mass, cg_proportion_forward=0.5):

        self._track = track

        self._base = base

        self._mass = mass

        self._cg = cg_proportion_forward * self._base

        self._heading = 0

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, val):
        self._mass = val

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, val):
        self._heading = val

    @property
    def heading_d(self):
        return self._heading * 180.0 / math.pi

    @heading_d.setter
    def heading_d(self, val):
        self._heading = val * math.pi / 180.0

    @property
    def curvature(self):
        return math.cos(self.heading)/self._cg

    @curvature.setter
    def curvature(self, val):
        self._heading = math.acos(self._cg * val)


