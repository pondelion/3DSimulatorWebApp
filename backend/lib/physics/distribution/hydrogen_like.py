import numpy as np
from ..special_function.special_function import spherial_harminic, laguerre


def R(n, l, r, Z=1):
    """Radial wave function of hydrogen electron.
    """

    rho = 2.0*r*Z/n
    norm = Z**1.5 * (2.0/n)**1.5 * np.sqrt(np.math.factorial(n-l-1) / 2.*n*np.math.factorial(n+l))
    return norm * rho**l * np.exp(-0.5*rho) * laguerre(n, l, rho)


def Y(l, m, theta, phi):
    """Azimuthal wave function of hydrogen electron.
    """
    theta_mesh, phi_mesh = np.meshgrid(theta, phi)
    return spherial_harminic(l, m, theta_mesh, phi_mesh)


def R_dist(n, l, r, Z=1):
    """Radial distribution function of hydrogen electron.
    """

    return np.abs(R(n, l, r, Z))**2


def Y_dist(l, m, theta, phi):
    """Azimuthal distribution function of hydrogen electron.
    """

    return np.abs(Y(l, m, theta, phi))**2


def R_dist_cumsum(n, l, r, Z=1):
    """Cumultive sum of radial distribution function of hydrogen electron.
    """

    return np.cumsum(R_dist(n, l, r, Z))


def Y_dist_cumsum(l, m, theta, phi):
    """Cumultive sum of azimuthal distribution function of hydrogen electron.
    """

    return np.cumsum(Y_dist(l, m, theta, phi))


def hydrogen_electron_dist(r, theta, phi, n, l, m, Z=1):
    """Radial and azimuthal distribution function of hydrogen electron.
    """
    return R_dist(n, l, r, Z), Y_dist(l, m, theta, phi)


def hydrogen_electron_dist_cumsum(r, theta, phi, n, l, m, Z=1):
    """Cumultive sum of radial and azimuthal distribution function of hydrogen electron.
    """
    return R_dist_cumsum(n, l, r, Z), Y_dist_cumsum(l, m, theta, phi)
