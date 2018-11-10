import numpy as np


def gravity(m, g=-9.8):
    """Calculate graviational force.

    Args:
        m (float): The mass of particle/material.
        g (gloat): The gravitational acceleration constant. Defaults to -9.8.

    Returns:
        numpy.ndarray: The graviational force.
    """
    return m * np.array([0.0, g, 0.0])
