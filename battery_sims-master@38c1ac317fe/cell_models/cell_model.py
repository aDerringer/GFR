import matlab.engine as matlab_eng
from scipy.interpolate import interp1d
import math
import numpy as np


class CellModel:

    s_in_hr = 3600.0

    def __init__(self):
        self.matlab = matlab_eng.start_matlab()

        self._state_of_charge_for_voltage_raw = None
        self._voltage_open_circuit_raw = None

        self._state_of_charge_for_resistance_raw = None
        self._internal_resistance_raw = None

        self._interp_volts = None
        self._interp_resistance = None

        self._soc = 1.0

        self._bol_capacity_amp_seconds = 1.0

        self._charge_power = 0.0
        self._term_power = 0.0
        self._heat_watts = 0.0

        self._efficiency = 1.0

    def __repr__(self):
        return str(self.capacity_ah) + ' Ah cell, '\
               + str(int(self.soc*100)) + '%, '\
               + str(int(self.voltage_no_load*100)/100.0) + ' VNL, '\
               + str(int(self._charge_power*100)/100.0) + ' W Charge, '\
               + str(int(self._term_power*100)/100.0) + ' W Term, '\
               + str(int(self._heat_watts*100)/100.0) + ' W Heat, '\
               + str(int(self._efficiency*100)) + '% Eff'

    @property
    def soc(self):
        return self._soc

    @soc.setter
    def soc(self, val):
        if 0.0 <= val <= 1.0:
            self._soc = val
        else:
            pass

    @property
    def resistance(self):
        try:
            res = self._interp_resistance(self._soc)
        except ValueError:
            return 999999.9
        else:
            return res

    @property
    def capacity_ah(self):
        return self._bol_capacity_amp_seconds / self.s_in_hr

    def set_capacity_ah(self, cap_ah):
        self._bol_capacity_amp_seconds = cap_ah * self.s_in_hr

    @property
    def voltage_no_load(self):
        return self._interp_volts(self._soc)

    def voltage_terminal(self, current_amps):
        return self.voltage_no_load - (current_amps * self.resistance)

    def apply_power_for_time(self, power, time_s):

        if power > 0:
            charging = True
        else:
            charging = False

        a = self.resistance
        if charging:   # charging
            b = self.voltage_no_load
            c = - math.fabs(power)
        else:   # discharging
            b = - self.voltage_no_load
            c = math.fabs(power)

        discriminant = (b**2) - (4*a*c)

        if discriminant < 0:
            discriminant = 0

        if charging:
            current = (-b + math.sqrt(discriminant)) / (2*a)
            current = math.fabs(current)
        else:
            current = (-b - math.sqrt(discriminant)) / (2*a)
            current = - math.fabs(current)

        if current == 0.0:
            voltage_terminal = self.voltage_no_load
        else:
            voltage_terminal = power / current

        print('Applying', str(int(voltage_terminal*100.0)/100.0), 'V')

        self.apply_voltage_for_time(voltage_terminal, time_s)

    def apply_voltage_for_time(self, voltage, time_s):
        current = (voltage - self.voltage_no_load) / self.resistance
        return self.apply_current_for_time(current, time_s)

    def apply_current_for_time(self, current_amps, time_s):

        new_soc = self.soc + (current_amps/time_s)/self._bol_capacity_amp_seconds

        if 0.0 <= new_soc <= 1.0:

            i2r_loss = current_amps*current_amps*self.resistance

            self._soc = new_soc
        else:

            i2r_loss = 0

            print('Invalid time step: SOC at', str(int(self.soc*100)), '%')

        charge_power = current_amps*self.voltage_terminal(current_amps)

        self._charge_power = charge_power

        self._heat_watts = i2r_loss
        if charge_power > 0:
            self._term_power = charge_power + i2r_loss
            self._efficiency = charge_power / self._term_power
        else:
            self._term_power = charge_power + i2r_loss
            self._efficiency = self._term_power / charge_power

        return i2r_loss * time_s

    def reload_interpolations(self):

        self._interp_volts = interp1d(
            self._state_of_charge_for_voltage_raw,
            self._voltage_open_circuit_raw,
            kind='cubic'
        )

        self._interp_resistance = interp1d(
            self._state_of_charge_for_resistance_raw,
            self._internal_resistance_raw,
            kind='cubic'
        )

    def load_from_filename(self, filename):
        raise NotImplementedError

    def load_from_lists(
            self,
            state_of_charge_for_voltage_raw,
            voltage_open_circuit_raw,
            state_of_charge_for_resistance_raw,
            internal_resistance_raw,
    ):

        self._state_of_charge_for_voltage_raw = state_of_charge_for_voltage_raw
        self._voltage_open_circuit_raw = voltage_open_circuit_raw

        self._state_of_charge_for_resistance_raw = state_of_charge_for_resistance_raw
        self._internal_resistance_raw = internal_resistance_raw

        self.reload_interpolations()

    def soc_to_v_r(self, soc):

        return self._interp_volts(soc), self._interp_resistance(soc)
