import numpy as np
import datetime
from time import sleep
from ...._base_simulator import BaseSimulator


class IsingSpin3D(BaseSimulator):

    def __init__(self, simulator_name):
        super().__init__(simulator_name)
        self._MAX_HISTORY = 10000

    def init(self):
        self._temperature = float(self._params['initial_temperature'])
        self._sweep_rate = float(self._params['sweep_rate_sec'])
        self._dimension_x = self._params['dimension_x']
        self._dimension_y = self._params['dimension_y']
        self._dimension_z = self._params['dimension_z']
        self._exchange_interaction = float(self._params['exchange_interaction'])
        self._spins = np.ones([self._params['dimension_x'], self._params['dimension_y'], self._params['dimension_z']])
        self._time_history = []
        self._magnetization_history = []
        self._spins_history = []
        self._spins_history.append(self._spins.flatten().copy().tolist())
        self._colors_history = []
        self._colors_history.append([0xff0000 if dir == 1 else 0x0000ff for dir in self._spins.flatten()])
        self._init_positions()
        self._temperature_hist = []
        self._temperature_hist.append(self._temperature)

    def update(self, dt):
        if self._is_running is False:
            return
        self._time += dt
        sweep_dir = 1 if int(self._params['final_temperature']) > int(self._params['initial_temperature']) else -1
        sweep_rate = sweep_dir * abs(float(self._params['sweep_rate_sec']))
        self._temperature += sweep_rate * dt
        if (int(self._params['initial_temperature']) - int(self._params['final_temperature'])) * \
            (self._temperature - int(self._params['final_temperature'])) < 0:
            self._temperature = int(self._params['final_temperature'])
        self._temperature_hist.append(self._temperature)
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).total_seconds() < dt:
            idx = np.random.randint(0, self._dimension_x)
            idy = np.random.randint(0, self._dimension_y)
            idz = np.random.randint(0, self._dimension_z)
            cur_energy = 0.
            j = float(self._params['exchange_interaction'])
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    for dz in range(-1, 2):
                        if dx == 0 and dy == 0 and dz == 0:
                            continue
                        try:
                            cur_energy += self._spins[idx+dx, idy+dy, idz+dz]
                        except IndexError:
                            pass
            cur_energy *= (-j * self._spins[idx, idy, idz])
            flip_energy = -cur_energy
            if np.random.rand() < 0.000001:
                self._spins[idx, idy, idz] *= -1
            elif np.random.rand() < min(np.exp(-(flip_energy-cur_energy)/self._temperature), 1.):
                self._spins[idx, idy, idz] *= -1
        self._spins_history.append(((self._spins + 1) * np.pi * 0.5).flatten().copy().tolist())
        self._spins_history = self._spins_history[-self._MAX_HISTORY:]
        self._magnetization_history.append(self._get_normalized_magnetizastion())
        self._magnetization_history = self._magnetization_history[-self._MAX_HISTORY:]
        self._time_history.append(self._time)
        self._time_history = self._time_history[-self._MAX_HISTORY:]
        self._colors_history.append([0xff0000 if dir == 1 else 0x0000ff for dir in self._spins.flatten()])
        self._colors_history = self._colors_history[-self._MAX_HISTORY:]

    def get_states(self, n=1):
        """Return last n states of simulation.

        Args:
            n (int): The number of states.

        Returns:
            states (json): The json data of latest n states.
        """
        states = {
            'directions': self._spins_history[-n:],
            'positions': self._positions_history[-n:],
            'colors': self._colors_history[-n:],
            'magnetization': self._magnetization_history[-n:],
            'time': self._time_history[-n:],
            'temperature': self._temperature_hist[-n:]
        }
        return states

    def _get_normalized_magnetizastion(self):
        return abs(sum(self._spins.flatten())/len(self._spins.flatten()))

    def _init_positions(self, dx=1, dy=1, dz=1):
        dim_x = int(self._params['dimension_x'])
        dim_y = int(self._params['dimension_y'])
        dim_z = int(self._params['dimension_z'])
        self._positions = np.zeros((dim_x, dim_y, dim_z, 3))
        for x in range(dim_x):
            for y in range(dim_y):
                for z in range(dim_z):
                    self._positions[x, y, z] = np.array([x*dx - 0.5*dx*dim_x, z*dz - 0.5*dz*dim_z, y*dy - 0.5*dy*dim_y])
        self._positions_history = [self._positions.reshape([-1, 3]).copy().tolist()]
