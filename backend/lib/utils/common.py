import yaml
import os
from logging import basicConfig, getLogger, DEBUG


basicConfig(level=DEBUG)


def load_params(simulator, file_path='conf/conf.yaml'):
    """Load parameters form conf file.

    Args:
        simulator (str): The simulator name.
        file_path (str): The path of conf file. Defaults to 'conf/conf.yaml'.

    Returns:
        params (json): The json data of conf.
            The key is parameter name and the value if default value. 
    """
    conf = yaml.load(open(file_path))
    params = {}
    for param_name, val in conf['SIMULATORS'][simulator]['PARAM_NAMES'].items():
        params[param_name] = val['default']
    return params


def get_logger(name):
    return gettLogger(name)


def density2color(densitiy: float):
    """Convert density to hex color

    Args:
        density (float): Density

    Returns:
        hex
    """