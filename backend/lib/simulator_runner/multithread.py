import threading
import datetime
from time import sleep
from ._base_simulator_runner import BaseSimulatorRunner


def update_worker(simulator):
    print('update_worker started.')
    simulator.run()
    prev_time = datetime.datetime.now()
    dt_sec = 0.
    while True:
        time = datetime.datetime.now()
        dt_sec += (time - prev_time).total_seconds()
        if dt_sec > simulator.minimal_dt:
            if simulator.is_running:
                simulator.update(dt_sec)
            dt_sec -= simulator.minimal_dt
        prev_time = time
        sleep(0.001)


class SimulatorRunner(BaseSimulatorRunner):

    def __init__(self):
        super().__init__()

    def run(self, ip, simulator_name):
        if (ip, simulator_name) not in self._simulators:
            print(simulator_name + ' is not created.')
            return

        if self._simulators[(ip, simulator_name)]['thread'] is not None:
            self._simulators[(ip, simulator_name)]['simulator'].run()
            return

        thread = threading.Thread(
            target=update_worker,
            args=([self._simulators[(ip, simulator_name)]['simulator']])
        )
        self._simulators[(ip, simulator_name)]['thread'] = thread
        thread.start()
