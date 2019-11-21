import numpy as np

from cell_models import generic_cell
from cell_models.cell_model import CellModel


if __name__ == '__main__':

    cell = CellModel()

    cell.load_from_lists(
        generic_cell.state_of_charge_for_voltage_raw,
        generic_cell.voltage_open_circuit_raw,
        generic_cell.state_of_charge_for_resistance_raw,
        generic_cell.internal_resistance_raw
    )

    cell.load_from_lists(
        np.array([0, 109]),
    )

    cell.soc = 0.2
    cell.set_capacity_ah(2.0)

    print(cell)

    for step in range(100):

        time_step = 0.5

        cell.apply_power_for_time(100, time_step)

        cell.resistance

        print(cell)

