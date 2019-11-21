from scipy import signal
import numpy as np

from track_to_spline.geometry_elements import SplineXY, LoopClosure, Track
from track_to_spline.geometry_elements import GPSDecoder


class TrackGeometryProcessor:

    def __init__(self):

        self._track_geometry = None

    @property
    def track_geometry(self):
        return self._track_geometry

    @property
    def lap_x(self):
        return self.track_geometry.x

    @property
    def lap_y(self):
        return self.track_geometry.y

    @property
    def curvature(self):
        return self.track_geometry.k

    def smoothed_curvature(self, smoothing=0.5):

        num = len(self.curvature)

        curves = np.concatenate((self.curvature, self.curvature))

        b, a = signal.butter(5, smoothing, 'low')

        smoothed = signal.filtfilt(b, a, curves)

        midway = int(num/2)
        midway_2 = num+midway

        wrapped = smoothed[midway:midway_2]

        upwrapped = np.concatenate((wrapped[midway:-1], wrapped[0:midway+1]))

        return upwrapped

    def find_turns(self, smoothing):

        absolute_curvature = np.fabs(self.smoothed_curvature(smoothing=smoothing))

        peaks = []

        for i in range(1, len(absolute_curvature)-1):

            diff_back = absolute_curvature[i] - absolute_curvature[i-1]
            diff_fwrd = absolute_curvature[i+1] - absolute_curvature[i]

            if diff_back > 0 > diff_fwrd:

                peaks.append(i)

            # elif diff_fwrd > 0 > diff_back:
            #
            #     peaks.append(i)

        return peaks

    def load_from_arrays(self, longitude_deg, latitude_deg):

        self._track_geometry = self.gps_to_track(longitude_deg, latitude_deg)

    @staticmethod
    def gps_to_track(longitude_deg, latitude_deg):

        x_m, y_m = GPSDecoder.gps_coord_to_meters(
            longitude_deg, latitude_deg
        )

        spline_xy = SplineXY(x_m, y_m)

        open_track = Track(spline_xy=spline_xy)

        closed_track = LoopClosure.get_closed_track(open_track)

        return closed_track
