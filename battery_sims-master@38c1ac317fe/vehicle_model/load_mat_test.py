from vehicle_model.point_mass_model import GGV

if __name__ == '__main__':

    ggv = GGV()

    ggv.read_from_mat('../matlab_files/18e_fsi_endurance_raw.mat')

