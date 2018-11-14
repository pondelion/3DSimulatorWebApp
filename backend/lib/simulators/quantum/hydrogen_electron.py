import numpy as np
from .._base_simulator import BaseSimulator
from ...utils.data_util import sampling
from ...physics.distribution.hydrogen_like import hydrogen_electron_dist


class HydrogenElectronDistribution(BaseSimulator):

    def __init__(self, simulator_name):
        super().__init__(simulator_name)

    def init(self):
        self._time = 0.
        self._time_history = []
        self._positions_history = []
        self._colors_history = []
        self._r = np.arange(0, 10, 0.02)
        self._theta = np.arange(0, np.pi, 0.01)
        self._phi = np.arange(0, 2.0*np.pi, 0.01)
        self._colors_history.append(self._colors.copy())
        self._positions_history.append(self._positions.reshape([-1, 3]).copy().tolist())
        self._time_history.append(self._time)

    def update(self, dt):
        """Keep generating electron according to hydrogen electron distribution for nlm.
        """
        if self._is_running is False:
            return

        if not self._nlm_check(self._n, self._l, self._m):
            return

        dt = min(dt, 0.01)
        self._time += dt

        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).total_seconds() < dt:
            r_idxs = sampling(self._R_dist, num=100)
            theta_idxs, phi_idxs = sampling(self._Y_dist, num=100)
            xyz = [
                [sefl._r[r_idx]*np.sin(self._theta[theta.idx])*np.cos(self._phi[phi_idx]), sefl._r[r_idx]*np.sin(self._theta[theta.idx])*np.sin(self._phi[phi_idx]), sefl._r[r_idx]*np.cos(self._theta[theta.idx])] /
                    for r_idx, theta_idx, phi_idx in zip(r_idxs, theta_idxs, phi_idxs)
            ]
            self._positions_history += xyz
            self._positions_history = self._positions_history[-self._MAX_HISTORY:]

        self._time_history.append(self._time)
        self._time_history = self._time_history[-self._MAX_HISTORY:]

    def get_states(self, n=1):
        """Return last n states of simulation.

        Args:
            n (int): The number of states.

        Returns:
            states (json): The json data of latest n states.
        """
        states = {
            'electron_positions': self._positions_history[-n:],
            'time': self._time_history[-n:],
            'colors': self._colors_history[-n:]
        }
        return states

    def _on_update_params(self):
        self._n = int(self._params['n'])
        self._l = int(self._params['l'])
        self._m = int(self._params['m'])
        self._R_dist, self._Y_dist = hydrogen_electron_dist(
                                        self._r, self._theta, self._phi, n=self._n, l=self._l, m=self._m, Z=1
                                    )

    def _nlm_check(n, l, m):
        if n <= l:
            return False
        if l < abs(m):
            return False
        return True
