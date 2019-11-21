import numpy as np
from scipy import interpolate

DEFAULT_NOISE = 0.0000001


def add_noise_to_array(orig_array: np.ndarray, amplitude: float = DEFAULT_NOISE):

    if not isinstance(orig_array, np.ndarray):
        orig_array = np.array(orig_array)

    shape = orig_array.shape

    noise_array = np.random.rand(*shape)*amplitude

    return orig_array + noise_array


def get_1d_spline(t, x):

    try:

        cubic_spline = interpolate.CubicSpline(t, x)

    except ValueError:

        cubic_spline = interpolate.CubicSpline(
            add_noise_to_array(t),
            add_noise_to_array(x),
        )

    return cubic_spline


class SplineXY:

    def __init__(self, x, y):

        assert len(x) == len(y)

        s = np.arange(0, 1.0, 1/len(x))

        self._cub_spline_x = get_1d_spline(s, x)
        self._cub_spline_y = get_1d_spline(s, y)

    def eval(self, der=0, steps=1000):

        s = np.arange(0, 1.0, 1 / steps)

        return self._cub_spline_x(s, der), self._cub_spline_y(s, der)
