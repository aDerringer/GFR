import math
import numpy as np

from track_to_spline.splines import SplineXY

DIV_ZERO_NOISE = 0.000000001
CURVATURE_CORRECTION_SCALE = 1#20000


class Point:

    def __init__(self, x=0, y=0, z=0):

        self.x, self.y, self.z = x, y, z


class Track:

    def __init__(self, **kwargs):

        x, y = kwargs.get('x', None), kwargs.get('y', None)

        spline_xy = kwargs.get('spline_xy', None)

        if x is not None and y is not None and len(x) == len(x):

            self._spline = SplineXY(x, y)

        elif spline_xy is not None and isinstance(spline_xy, SplineXY):

            self._spline = spline_xy

        self._spots = 1000

        self._x, self._y = self._spline.eval()

        self._k = None

        self._compute_curvature()

    def at(self, idx):
        if idx >= self._spots:
            idx = -1
        return self._x[idx], self._y[idx]

    @property
    def start(self):
        return self.at(0)

    @property
    def end(self):
        return self.at(-1)

    @property
    def num(self):
        return self._spots

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def vel(self):
        return self._compute_vel()

    @property
    def heading(self):

        dir_x, dir_y = self.vel

        return np.arctan2(dir_y, dir_x)

    @property
    def turn_radius(self):

        non_zero_curvature = self._add_noise_until_no_zeros(self.k)

        raw_radii = 1.0 / non_zero_curvature

        max_radius = 50

        raw_radii[raw_radii > max_radius] = max_radius

        raw_radii[raw_radii < -max_radius] = -max_radius

        return raw_radii

    @property
    def k(self):
        return self._k

    def _compute_vel(self):
        return self._eval_spline(der=1)

    def _compute_curvature(self):

        k_x, k_y = self._spline.eval(der=2)

        mag = np.sqrt(np.square(k_x) + np.square(k_y)) / CURVATURE_CORRECTION_SCALE

        ang = np.arctan2(k_y, k_x)

        self._k = mag * np.sin(ang - self.heading)

    def _eval_spline(self, der=0, steps=1000):

        return self._spline.eval(der=der, steps=steps)

    @staticmethod
    def _add_noise_until_no_zeros(numbers):

        array = np.array(numbers)

        while np.any(array == 0):
            noise = np.random.rand(array.shape) * DIV_ZERO_NOISE

            array += noise

        return array

    def __iter__(self):
        return TrackIterator(self)


class TrackIterator:

    def __init__(self, track):

        self._track = track

        self._index = 0

    def __next__(self):
        """Returns the next item in the track"""
        if self._index < self._track.num:
            spot = self._track.at(self._index)
            self._index += 1
            return spot
        raise StopIteration


class LoopClosure:

    @staticmethod
    def get_final_error(track):

        start_point = track.start
        end_point = track.end

        del_x = end_point[0] - start_point[0]
        del_y = end_point[1] - start_point[1]

        return del_x, del_y

    @staticmethod
    def get_closed_track(track: Track):
        err_x, err_y = LoopClosure.get_final_error(track)

        error_fractions = np.arange(0, 1.0, 1.0 / track.num)

        correction_x = error_fractions * err_x
        correction_y = error_fractions * err_y

        return Track(
            x=(np.array(track.x) - correction_x),
            y=(np.array(track.y) - correction_y),
        )


class GPSDecoder:

    @staticmethod
    def gps_coord_to_meters(long, lat):

        long = np.array(long)
        lat = np.array(lat)

        x_new = np.zeros(long.size)
        y_new = np.zeros(lat.size)

        lat_0 = lat[0]
        long_0 = long[0]

        for i, (long_i, lat_i) in enumerate(zip(long, lat)):

            m_disp = GPSDecoder.m_between_gps_points(
                Point(lat_0, long_0, 0),
                Point(lat_i, long_i, 0)
            )

            x_new[i] = m_disp.x
            y_new[i] = m_disp.y

        return x_new, y_new

    @staticmethod
    def m_between_gps_points(gps_origin: Point, gps_point: Point):

        radius_earth_m = 6.371e6
        deg_to_rad = math.pi / 180.0

        longitude_diff_deg = gps_point.x - gps_origin.x
        latitude_diff_deg = gps_point.y - gps_origin.y

        distance_m = Point()
        distance_m.x = longitude_diff_deg * deg_to_rad * radius_earth_m
        distance_m.y = -latitude_diff_deg * deg_to_rad * radius_earth_m * math.cos(gps_origin.x * deg_to_rad)

        distance_m.z = (gps_point.z - gps_origin.z)

        return distance_m


