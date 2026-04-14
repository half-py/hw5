import numpy as np
from math import comb


def binomial_pmf(n, p):
    """
    回傳 Binomial(n, p) 在 x=0,1,...,n 的 pmf
    """
    x_values = np.arange(n + 1)
    pmf_values = np.array([
        comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
        for x in x_values
    ])
    return x_values, pmf_values


def theoretical_covariance_matrix(n, probabilities):
    """
    multinomial 的理論 covariance matrix
    """
    probabilities = np.asarray(probabilities, dtype=float)
    k = len(probabilities)

    cov_matrix = np.zeros((k, k))
    for i in range(k):
        for j in range(k):
            if i == j:
                cov_matrix[i, j] = n * probabilities[i] * (1 - probabilities[i])
            else:
                cov_matrix[i, j] = -n * probabilities[i] * probabilities[j]

    return cov_matrix