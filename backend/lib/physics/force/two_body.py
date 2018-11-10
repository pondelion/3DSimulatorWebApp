import numpy as np


def lennard_jones(p1: np.array, p2: np.array, eps, sigma):
    """Calculate force acting on particle p1 from p2

    Args:
        p1 (numpy.ndarray): Position vector of particle 1.
        p2 (numpy.ndarray): Position vector of particle 2.

    Returns:
        force (numpy.ndarray): Lennard-Jones force acting on p1 from p2.
    """
    r = p2 - p1
    r2 = max(sum(r*r), 0.0000001)
    coeff = 24. * eps * (1. / r2)**4 * sigma**6 * (1. - 2. * sigma**6 / r2**3)
    return coeff * r
