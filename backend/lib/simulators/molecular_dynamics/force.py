import numpy as np


def lennard_jones(p1: np.array, p2: np.array, eps, sigma):
    """Force acting on particle p1
    """
    r = p2 - p1
    r2 = max(sum(r*r), 0.0000001)
    coeff = 24. * eps * (1. / r2)**4 * sigma**6 * (1. - 2. * sigma**6 / r2**3)
    return coeff * r


def gravity(m, g=9.8):
    return -m * np.array([0.0, g, 0.0])
