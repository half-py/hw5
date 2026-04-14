import numpy as np
import pandas as pd

from modules.theory import theoretical_covariance_matrix


def build_expectation_table(samples, n, probabilities):
    empirical_mean = samples.mean(axis=0)
    theoretical_mean = n * probabilities
    abs_error = np.abs(empirical_mean - theoretical_mean)

    labels = [f"X{i+1}" for i in range(len(probabilities))]

    df = pd.DataFrame({
        "類別": labels,
        "樣本平均": empirical_mean,
        "理論期望值": theoretical_mean,
        "絕對誤差": abs_error
    })
    return df


def build_variance_table(samples, n, probabilities):
    empirical_var = np.var(samples, axis=0, ddof=1)
    theoretical_var = n * probabilities * (1 - probabilities)
    abs_error = np.abs(empirical_var - theoretical_var)

    labels = [f"X{i+1}" for i in range(len(probabilities))]

    df = pd.DataFrame({
        "類別": labels,
        "樣本變異數": empirical_var,
        "理論變異數": theoretical_var,
        "絕對誤差": abs_error
    })
    return df


def build_covariance_results(samples, n, probabilities):
    empirical_cov = np.cov(samples, rowvar=False, ddof=1)
    theoretical_cov = theoretical_covariance_matrix(n, probabilities)
    abs_error = np.abs(empirical_cov - theoretical_cov)
    return empirical_cov, theoretical_cov, abs_error