import numpy as np
import streamlit as st


def render_sidebar():
    st.sidebar.header("參數設定")

    n = st.sidebar.number_input("n", min_value=1, value=100, step=1)
    sample_size = st.sidebar.number_input("sample size", min_value=100, value=10000, step=100)
    k = st.sidebar.number_input("變數個數 k", min_value=2, value=4, step=1)
    seed = st.sidebar.number_input("seed", min_value=0, value=42, step=1)

    st.sidebar.markdown("### 機率設定")
    st.sidebar.caption("請輸入前 k-1 個機率，最後一個會自動補成總和為 1。")

    probabilities = []

    # 平均分配當作預設值
    default_p = 1.0 / k

    for i in range(k - 1):
        remaining_mass = 1.0 - sum(probabilities)

        p_i = st.sidebar.number_input(
            f"p{i+1}",
            min_value=0.0,
            max_value=float(remaining_mass),
            value=float(min(default_p, remaining_mass)),
            step=0.01,
            format="%.4f",
            key=f"p_{i}"
        )
        probabilities.append(p_i)

    last_p = 1.0 - sum(probabilities)

    if last_p < 0:
        st.sidebar.error("前面的機率總和已超過 1，請調整。")
        st.stop()

    probabilities.append(last_p)
    probabilities = np.array(probabilities, dtype=float)

    st.sidebar.write(f"p{k} (自動補齊) = {last_p:.4f}")
    st.sidebar.write(f"機率總和 = {probabilities.sum():.4f}")

    return int(n), int(sample_size), probabilities, int(seed)