from .._base_simulator import BaseSimulator
from ...solver.solver import euler


class BouncingBall(BaseSimulator):
    GRAVITY_ACCEL = -9.8
    SIMULATOR_NAME = 'bouncing_ball'

    def __init__(self, simulator_name):
        super().__init__(simulator_name)

    def init(self):
        #self._params = load_params(BouncingBall.SIMULATOR_NAME)
        self._height = self._params['initial_height']
        self._vel_y = self._params['initial_vel_y']
        self._height_history = []
        self._vel_y_history = []
        self._time_history = []

    def update(self, dt):
        if self._is_running is False:
            return
        self._time += dt
        self._vel_y = euler(self._vel_y, self._force()/self._params['ball_mass'], dt)
        self._height += self._vel_y * dt
        if (self._height - self._params['ground_height']) < self._params['ball_radius']:
            self._height = self._params['ground_height'] + self._params['ball_radius']
            self._vel_y *= - self._params['restitution_coef']
        self._height_history.append(self._height)
        self._vel_y_history.append(self._vel_y)
        self._time_history.append(self._time)
        #print('t : {}\nvel_y : {}\nheight : {}'.format(self._time, self._vel_y, self._height))

    def get_states(self, n=1):
        """最新状態(位置など)をn個返す
        """
        states = {
            'obj_name': 'ball1',
            'property_name': 'pos_y',
            'height': self._height_history[-n:],
            'vel_y': self._vel_y_history[-n:],
            'time': self._time_history[-n:]
        }
        return states

    def _force(self):
        return self._params['ball_mass'] * BouncingBall.GRAVITY_ACCEL \
                - self._params['resistance_coef'] * self._vel_y
