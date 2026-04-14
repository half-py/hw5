import numpy as np
import streamlit as st

from modules.plotting import plot_single_x


def render_single_x_section(samples, n, probabilities):
    st.subheader("單一 Xi 分布")

    labels = [f"X{i+1}" for i in range(len(probabilities))]

    selected = st.selectbox("選擇 Xi", labels)

    index = labels.index(selected)

    left, right = st.columns([2, 1])

    with left:
        fig = plot_single_x(samples, n, probabilities, index)
        st.pyplot(fig)

    with right:
        mean = samples[:, index].mean()
        var = np.var(samples[:, index], ddof=1)

        theo_mean = n * probabilities[index]
        theo_var = n * probabilities[index] * (1 - probabilities[index])

        st.metric("樣本平均", f"{mean:.4f}")
        st.metric("理論期望值", f"{theo_mean:.4f}")
        st.metric("樣本變異數", f"{var:.4f}")
        st.metric("理論變異數", f"{theo_var:.4f}")
        st.metric("平均誤差", f"{abs(mean - theo_mean):.4f}")
        st.metric("變異誤差", f"{abs(var - theo_var):.4f}")

    st.divider()