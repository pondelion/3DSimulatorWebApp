from .._base_simulator import BaseSimulator
from ...utils.util import load_params


class BouncingBall(BaseSimulator):
    GRAVITY_ACCEL = -9.8
    SIMULATOR_NAME = 'bouncing_ball'

    def __init__(self):
        super().__init__(self)

    def init(self):
        self._height = self._params['initial_height']
        self._vel_y = self._params['initial_vel_y']
        self._height_history = []
        self._vel_y_history = []
        self._time_history = []
        self._params = load_params(BouncingBall.SIMULATOR_NAME)

    def update(self, dt):
        self._time += dt
        self._vel_y += BouncingBall.GRAVITY_ACCEL * dt / self._params['ball_mass']
        self._height += self._vel_y * dt
        if (self._height - self._params['ground_height']) < self._params['ball_radius']:
            self._height = self._params['ground_height'] + self._params['ball_radius']
            self._vel_y *= -1.
        self._height_history.append(self._height)
        self._vel_y_history.append(self._vel_y)
        self._time_history.append(self._time)

    def get_states(n=1):
        """最新状態(位置など)をn個返す
        """
        states = {
            'height': self._height_history[-n:],
            'vel_y': self._vel_y_history[-n:],
            'time': self._time_history[-n:]
        }
        return states
