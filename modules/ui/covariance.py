import numpy as np
import pandas as pd
import streamlit as st


def render_covariance_section(p, empirical, theoretical, error):

    st.subheader("Covariance matrix")

    max_err = np.max(error)
    mean_err = np.mean(error)

    c1, c2 = st.columns(2)

    c1.metric("max error", f"{max_err:.6f}")
    c2.metric("mean error", f"{mean_err:.6f}")

    labels = [f"X{i+1}" for i in range(len(p))]

    with st.expander("sample covariance"):
        st.dataframe(
            pd.DataFrame(empirical, index=labels, columns=labels)
        )

    with st.expander("theoretical covariance"):
        st.dataframe(
            pd.DataFrame(theoretical, index=labels, columns=labels)
        )

    with st.expander("absolute error"):
        st.dataframe(
            pd.DataFrame(error, index=labels, columns=labels)
        )

    st.divider()