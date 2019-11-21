import scipy.io as sio


class GGV:

    def __init__(self):

        self.model = None

    def read_from_arrays(self, g_lat, g_long, air_speed):

        raise NotImplementedError

    def read_from_mat(self, filename: str):

        mat = sio.loadmat(filename)

        speed = mat.get('GPS_Speed')
        g_lat = mat.get('GPS')

        print(mat)

        raise NotImplementedError
