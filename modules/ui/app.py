import numpy as np
import streamlit as st

from modules.sampler import ConditionalMultinomialSampler
from modules.stats_utils import *
from .sidebar import render_sidebar
from .summary import render_summary
from .single_x import render_single_x_section
from .tables import *
from .covariance import render_covariance_section
from .preview import render_sample_preview
from .formulas import render_formula_section

# 新增這行
from .page_mixture import render_mixture_page


def render_multinomial():

    st.title("Conditional Multinomial Sampler")

    n, sample_size, probabilities, seed = render_sidebar()

    rng = np.random.default_rng(seed)
    sampler = ConditionalMultinomialSampler(probabilities, rng)

    samples = sampler.sample_many(n, sample_size)

    expectation_df = build_expectation_table(samples, n, probabilities)
    variance_df = build_variance_table(samples, n, probabilities)

    empirical_cov, theoretical_cov, abs_cov_error = build_covariance_results(
        samples, n, probabilities
    )

    render_summary(n, sample_size, probabilities)

    render_single_x_section(samples, n, probabilities)

    render_expectation_table(expectation_df)

    render_variance_table(variance_df)

    render_covariance_section(
        probabilities,
        empirical_cov,
        theoretical_cov,
        abs_cov_error
    )

    render_sample_preview(samples, probabilities)

    render_formula_section()


def run_app():

    st.set_page_config(
        page_title="Simulation Methods",
        layout="wide"
    )

    page = st.sidebar.radio(
        "選擇頁面",
        [
            "Multinomial",
            "Mixture Method"
        ]
    )

    if page == "Multinomial":
        render_multinomial()
    else:
        render_mixture_page()