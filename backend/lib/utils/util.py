import yaml
import os


def load_params(simulator):
    conf = yaml.load(open('conf/conf.yaml'))
    params = {}
    for param_name, val in conf['SIMULATORS'][simulator]['PARAM_NAMES'].items():
        params[param_name] = val['default']
    return params
