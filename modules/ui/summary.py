import numpy as np
import streamlit as st


def render_summary(n, sample_size, probabilities):
    st.subheader("Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("n", int(n))
    c2.metric("sample size", int(sample_size))
    c3.metric("k", len(probabilities))
    c4.metric("p", str(np.round(probabilities, 4).tolist()))

    st.divider()