from abc import *
import json
from time import sleep
from ..utils.common import load_params


class BaseSimulator:

    def __init__(self, simulator_name):
        """Init function

        Args:
            simulator_name (str): Simulator name.
        """
        self._MAX_HISTORY = 10000
        self._time = 0.
        self._simulator_name = simulator_name
        self._is_running = False
        self._params = {}
        self._minimal_dt = 0.01
        self._is_finished = False
        self._params = load_params(self._simulator_name)
        self.init()

    def run(self):
        """Run simulation.
        """
        self._is_running = True

    def stop(self):
        """Stop simulation.
        """
        self._is_running = False

    def finish(self):
        """Finish simulation.
        """
        self._is_running = False
        self.init()

    def set_params(self, params):
        """Set parameters

        Args:
            params (json): The json data of parameters to set.
        """
        for key, val in params.items():
            self._params[key] = val
        self._on_update_params()

    @property
    def is_running(self):
        """Return whether simulator is running.

        Returns:
            True if simulator is runnning, False otherwise.
        """
        return self._is_running

    @property
    def minimal_dt(self):
        """Return minimal update time.

        Returns:
            float: Minimal time of updation.
        """
        return self._minimal_dt

    @abstractclassmethod
    def init(self):
        """Init function.
        Subclass must override this method.
        """
        raise NotImplementedError()

    @abstractclassmethod
    def update(self, dt):
        """Update system by dt.
        Subclass must override this method.

        Args:
            dt (float): The time to update.
        """
        raise NotImplementedError()

    @abstractclassmethod
    def get_states(self, n=1):
        """Get last n states of simulation.
        The states depends on each simulator and must be same as
        configurations defined in conf.yaml.
        Subclass must override this method.

        Args:
            n (int): The number of states.

        Returns:
            states (json): The json data of latest n states.
                The data must be serializable.
        """
        raise NotImplementedError()

    def get_states_streaming(self):
        """Keep returning latest state of simulation.

        Yields:
            json: Json data of latest state.
        """
        while True:
            yield json.dumps(self.get_states())
            sleep(0.01)

    def _on_update_params(self):
        """Additional updation when parameters is updated.
        Subclass may override this method if needed.
        """
        pass
