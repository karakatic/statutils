import numpy as np

methods = ('holm', 'bonferroni', 'hochberg', 'hommel', 'BH', 'BY', 'none')


def p_adjust(p, method='holm', n=None):
    if n is None:
        n = len(p)

    p0 = np.array(p)
    p_a = p0[np.logical_not(np.isnan(p0))]

    lp = len(p_a)

    assert n >= lp

    if n <= 1:
        return p0
    if n == 2 and method == 'hommel':
        method = 'hochberg'

    results = None

    if method == 'holm':
        i = np.arange(lp)
        o = p_a.argsort()
        ro = np.argsort(o)
        results = np.minimum(1, np.maximum.accumulate((n - i) * p_a[o]))[ro]
    elif method == 'bonferroni':
        results = np.minimum(p_a * n, 1)
    elif method == 'hochberg':
        i = np.arange(lp - 1, -1, -1)
        o = (-p_a).argsort()
        ro = np.argsort(o)
        results = np.minimum(1, np.minimum.accumulate((n - i) * p_a[o]))[ro]
    elif method == 'hommel':
        if n > lp:
            p_a = np.concatenate((p_a, np.repeat(1, n - lp)))

        i = np.arange(n) + 1
        o = p_a.argsort()
        p_sorted = p_a[o]
        ro = np.argsort(o)

        q = np.repeat(np.min(n * p_sorted / i), n)
        pa = np.repeat(np.min(n * p_sorted / i), n)

        for j in range(n - 1, 1, -1):
            ij = np.arange(n - j + 1)
            i2 = np.arange(n - j + 1, n)
            q1 = np.min(j * p_sorted[i2] / np.arange(2, j + 1))
            q[ij] = np.minimum(j * p_sorted[ij], q1)
            q[i2] = q[n - j]
            pa = np.maximum(pa, q)

        results = np.maximum(pa, q)[ro[np.arange(lp)] if lp < n else ro]
    elif method == 'BH':
        i = np.arange(lp - 1, -1, -1)
        o = (-p_a).argsort()
        ro = np.argsort(o)
        results = np.minimum(1, np.minimum.accumulate((n / (i + 1)) * p_a[o]))[ro]
    elif method == 'BY':
        i = np.arange(lp - 1, -1, -1)
        o = (-p_a).argsort()
        ro = np.argsort(o)
        q = np.sum(1 / np.arange(1, n + 1))
        results = np.minimum(1, np.minimum.accumulate((q * n / (i + 1)) * p_a[o]))[ro]
    elif method == 'none':
        results = p_a

    p0[np.logical_not(np.isnan(p0))] = results

    return p0
