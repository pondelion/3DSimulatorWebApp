import numpy as np


def sampling(distribution, num=1):
    dim = len(distribution.shape)
    if dim <= 0 or dim >= 3:
        raise ValueError('only 1/2 dimention is supported for now')

    cs = np.cumsum(distribution.flatten())
    cs = cs / cs[-1]

    rds = np.random.rand(num)

    indices = [np.sum(cs <= rd)-1 for rd in rds]

    if dim == 1:
        return indices
    if dim == 2:
        return [[int(idx/distribution.shape[1]), idx % distribution.shape[1]] for idx in indices]
