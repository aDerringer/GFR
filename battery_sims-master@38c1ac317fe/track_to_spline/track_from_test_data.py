import math
import time

import numpy as np
from track_to_spline.geometry_elements import GPSDecoder

from track_to_spline import assem_oval_gps
from track_to_spline.geometry_processor import TrackGeometryProcessor
import matplotlib.pyplot as plt


def scale_raw_gps(time, longitude, latitude):

    time = np.array(time) - time[0]

    longitude, latitude = GPSDecoder.gps_coord_to_meters(
        longitude, latitude
    )

    return time, longitude, latitude


if __name__ == '__main__':

    track_geometry = TrackGeometryProcessor()

    track_geometry.load_from_arrays(
        assem_oval_gps.longitude,
        assem_oval_gps.latitude,
    )

    plt.figure()

    curves = track_geometry.smoothed_curvature(smoothing=0.03)

    peaks = track_geometry.find_turns(smoothing=0.03)

    plt.plot(curves)

    for peak in peaks:

        plt.plot([peak, peak], [0, curves[peak]])

    plt.grid()
    plt.show()
