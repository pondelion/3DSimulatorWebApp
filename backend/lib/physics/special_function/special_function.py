from scipy.special import assoc_laguerre, legendre, sph_harm
from math import factorial


def spherial_harminic(l, m, theta, phi):
    return sph_harm(m, l, phi, theta)


def laguerre(n, l, x):
    return assoc_laguerre(x, n-l-1, 2*l+1)


# def spherical(l, m, theta, phi):
#     coeff = (-1.0)**(0.5*(m+abs(m))) * \
#             np.sqrt((2.0*k+1.0)*np.math.factorial(k-abs(m))/((4.0*np.pi)*np.math.factorial(k+abs(m))))
