

class BaseSimulatorRunner:

    def __init__(self):
        self._simulators = {}

    def stop(self, ip, simulator_name):
        if (ip, simulator_name) not in self._simulators:
            print(simulator_name + ' is not created.')
            return
        self._simulators[(ip, simulator_name)]['simulator'].stop()

    def finish(self, ip, simulator_name):
        if (ip, simulator_name) not in self._simulators:
            print(simulator_name + ' is not created.')
            return
        self._simulators[(ip, simulator_name)]['simulator'].finish()

    def init(self, ip, simulator_name):
        if (ip, simulator_name) not in self._simulators:
            print(simulator_name + ' is not created.')
            return
        self._simulators[(ip, simulator_name)]['simulator'].init()

    def exist(self, ip, simulator_name):
        return (ip, simulator_name) in self._simulators

    def create_simulator(self, ip, simulator_name, module_name, class_name):
        if self.exist(ip, simulator_name):
            return

        module = __import__(module_name, globals(), locals(), [class_name], 0)
        simulator_class = getattr(module, class_name)
        self._simulators[(ip, simulator_name)] = {
            'simulator': simulator_class(),
            'thread': None
        }
        print(self._simulators[(ip, simulator_name)]['simulator'])

    def get_states(self, ip, simulator_name, n):
        if not self.exist(ip, simulator_name):
            print(simulator_name + ' not exists.')
            return {}

        return self._simulators[(ip, simulator_name)]['simulator'].get_states(n)
