import numpy as np

methods = ('holm', 'bonferroni', 'hochberg', 'hommel', 'BH', 'BY', 'none')


def p_adjust(p, method:str='holm', n=None):
    """Given a set of p values, returns p values adjusted using one of the methods.

    **Arguments:**

    p {array} -- Array of p values to adjust.

    method {string} -- Method that is used in correction for multiple comparisons.
        Avaliable options: 'holm', 'bonferroni', 'hochberg', 'hommel', 'BH', 'BY', 'none'

    n {integer} -- Number of comparisons, must be at least length(p); only set this (to non-default) when you know what you are doing!

    **Returns**

    Numpy array of corrected p values (of the same length as p).

    **Details**

    The adjustment methods include the Bonferroni correction ("*bonferroni*") in which the p-values are multiplied by
    the number of comparisons. Less conservative corrections are also included by Holm (1979) ("*holm*"),
    Hochberg (1988) ("*hochberg*"),
    Hommel (1988) ("*hommel*"),
    Benjamini & Hochberg (1995) ("*BH*"),
    and Benjamini & Yekutieli (2001) ("*BY*"), respectively.
    A pass-through option ("*none*") is also included.
    The set of methods are contained in the multi_comparison.methods array for the benefit of methods that need to
    have the method as an option and pass it on to p_adjust.

    The first four methods are designed to give strong control of the family-wise error rate. There seems no reason to use the unmodified Bonferroni correction because it is dominated by Holm's method, which is also valid under arbitrary assumptions.

    Hochberg's and Hommel's methods are valid when the hypothesis tests are independent or when they are non-negatively associated (Sarkar, 1998; Sarkar and Chang, 1997). Hommel's method is more powerful than Hochberg's, but the difference is usually small and the Hochberg p-values are faster to compute.

    The "BH" and "BY" methods of Benjamini, Hochberg, and Yekutieli control the false discovery rate, the expected proportion of false discoveries amongst the rejected hypotheses. The false discovery rate is a less stringent condition than the family-wise error rate, so these methods are more powerful than the others.

    Note that you can set n larger than length(p) which means the unobserved p-values are assumed to be greater than all the observed p for "bonferroni" and "holm" methods and equal to 1 for the other methods.


    **References**

    Benjamini, Y., and Hochberg, Y. (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society Series B, 57, 289–300. http://www.jstor.org/stable/2346101.

    Benjamini, Y., and Yekutieli, D. (2001). The control of the false discovery rate in multiple testing under dependency. Annals of Statistics, 29, 1165–1188. doi: 10.1214/aos/1013699998.

    Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics, 6, 65–70. http://www.jstor.org/stable/4615733.

    Hommel, G. (1988). A stagewise rejective multiple test procedure based on a modified Bonferroni test. Biometrika, 75, 383–386. doi: 10.2307/2336190.

    Hochberg, Y. (1988). A sharper Bonferroni procedure for multiple tests of significance. Biometrika, 75, 800–803. doi: 10.2307/2336325.

    Shaffer, J. P. (1995). Multiple hypothesis testing. Annual Review of Psychology, 46, 561–584. doi: 10.1146/annurev.ps.46.020195.003021. (An excellent review of the area.)

    Sarkar, S. (1998). Some probability inequalities for ordered MTP2 random variables: a proof of Simes conjecture. Annals of Statistics, 26, 494–504. doi: 10.1214/aos/1028144846.

    Sarkar, S., and Chang, C. K. (1997). The Simes method for multiple hypothesis testing with positively dependent test statistics. Journal of the American Statistical Association, 92, 1601–1608. doi: 10.2307/2965431.

    Wright, S. P. (1992). Adjusted P-values for simultaneous inference. Biometrics, 48, 1005–1013. doi: 10.2307/2532694. (Explains the adjusted P-value approach.)
    """

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
