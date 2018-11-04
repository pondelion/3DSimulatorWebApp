import numpy as np
import sympy
from .._base_simulator import BaseSimulator
from ...solver.solver import euler


class FlowParticles(BaseSimulator):

    def __init__(self, simulator_name):
        super().__init__(simulator_name)

    def init(self):
        self._RANGE = 15
        self._time_history = []
        self._positions_history = []
        self._init_particles()
        self._parse_flow_field()

    def update(self, dt):
        if self._is_running is False:
            return
        self._time += dt
        for i in range(self._positions.shape[0]):
            self._velocities[i] = euler(self._velocities[i], 
                    self._force(self._positions[i])/self._params['mass'], dt)
            self._positions[i] += self._velocities[i] * dt
            if self._positions[i][0] > self._RANGE:
                self._positions[i][0] = self._RANGE
            if self._positions[i][1] > self._RANGE:
                self._positions[i][1] = self._RANGE
            if self._positions[i][2] > self._RANGE:
                self._positions[i][2] = self._RANGE
            if self._positions[i][0] < -self._RANGE:
                self._positions[i][0] = -self._RANGE
            if self._positions[i][1] < -self._RANGE:
                self._positions[i][1] = -self._RANGE
            if self._positions[i][2] < -self._RANGE:
                self._positions[i][2] = -self._RANGE
        print('1cycle')
        self._positions_history.append(self._positions.reshape([-1, 3]).copy().tolist())
        self._positions_history = self._positions_history[-self._MAX_HISTORY:]
        self._time_history.append(self._time)
        self._time_history = self._time_history[-self._MAX_HISTORY:]

    def get_states(self, n=1):
        """最新状態(位置など)をn個返す
        """
        states = {
            'positions': self._positions_history[-n:],
            'time': self._time_history[-n:]
        }
        return states

    def _force(self, pos):
        #return np.array([-0.5*pos[2], 0.0, 0.5*pos[0]])*(pos[1]+self._RANGE)*0.1
        return self._eval_flow_field(pos[0], pos[1], pos[2])*0.1

    def _init_particles(self, scale=10):
        self._positions = np.random.rand(
            int(self._params['particle_num']), 3
        )
        self._positions = 2. * (self._positions - 0.5) * self._RANGE
        self._velocities = np.zeros([int(self._params['particle_num']), 3])
        self._positions_history.append(self._positions.reshape([-1, 3]).copy().tolist())

    def _parse_flow_field(self):
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        z = sympy.Symbol('z')
        self._x = x
        self._y = y 
        self._z = z
        try:
            self._flow_field_x = eval(str(self._params['flow_field_x']) + " + 0*x + 0*y + 0*z")
            print(type(self._flow_field_x))
            print(self._flow_field_x)
            print(self._flow_field_x.subs({x: 1., y: 1., z: 1.}))
        except Exception as e:
            print(e)
            pass
        try:
            self._flow_field_y = eval(str(self._params['flow_field_y']) + " + 0*x + 0*y + 0*z")
        except Exception as e:
            print(e)
            pass
        try:
            self._flow_field_z = eval(str(self._params['flow_field_x']) + " + 0*x + 0*y + 0*z")
        except Exception as e:
            print(e)
            pass

    def _eval_flow_field(self, val_x, val_y, val_z):
        flow_filed = np.array([
            float(self._flow_field_x.subs({self._x: val_x, self._y: val_x, self._z: val_z})),
            float(self._flow_field_y.subs({self._x: val_x, self._y: val_x, self._z: val_z})),
            float(self._flow_field_z.subs({self._x: val_x, self._y: val_x, self._z: val_z})),
        ])
        return flow_filed

    def set_params(self, params):
        super().set_params(params)
        self._parse_flow_field()
