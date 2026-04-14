import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def mixture_sample(n, rng):

    samples = []

    for _ in range(n):

        z = rng.random() < 0.55

        if z:
            x = rng.choice([5,7,9,11,13])
        else:
            x = rng.choice([6,8,10,12,14])

        samples.append(x)

    return np.array(samples)


def render_mixture_page():

    st.title("Mixture Method 模擬 X")

    st.latex(
    r"""
    P(X=j)=
    \begin{cases}
    0.11 & j=5,7,9,11,13 \\
    0.09 & j=6,8,10,12,14
    \end{cases}
    """
    )

    sample_size = st.slider(
        "樣本數",
        500,
        20000,
        5000
    )

    rng = np.random.default_rng(42)
    samples = mixture_sample(sample_size, rng)

    # 左右排版
    left, right = st.columns([2,1])

    with left:

        fig, ax = plt.subplots(figsize=(7,4))

        # 深色背景
        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        values = np.arange(5,15)

        probs = [
            0.11 if v%2==1 else 0.09
            for v in values
        ]

        ax.hist(
            samples,
            bins=np.arange(4.5,15.5,1),
            density=True,
            alpha=0.5,
            color="#4FC3F7",
            edgecolor="#4FC3F7",
            label="simulation"
        )

        ax.plot(
            values,
            probs,
            marker="o",
            linewidth=2,
            color="#00E5FF",
            label="theoretical"
        )

        ax.set_title("Mixture 模擬分布", color="white")

        ax.tick_params(colors="white")

        for spine in ax.spines.values():
            spine.set_color("#888")

        ax.grid(alpha=0.2, color="white")

        legend = ax.legend()

        for text in legend.get_texts():
            text.set_color("white")

        legend.get_frame().set_facecolor("#0E1117")

        st.pyplot(fig)

    with right:

        st.subheader("統計資訊")

        st.metric(
            "樣本平均",
            f"{samples.mean():.4f}"
        )

        st.metric(
            "樣本變異數",
            f"{samples.var():.4f}"
        )

        st.metric(
            "最小值",
            int(samples.min())
        )

        st.metric(
            "最大值",
            int(samples.max())
        )

    st.divider()

    st.subheader("樣本預覽")

    preview_n = st.slider(
        "顯示筆數",
        min_value=5,
        max_value=30,
        value=10
    )

    preview = samples[:preview_n]

    import pandas as pd

    df = pd.DataFrame({
        "編號": range(1, preview_n + 1),
        "X": preview,
        "類型": ["奇數" if v % 2 else "偶數" for v in preview],
        "機率": [0.11 if v % 2 else 0.09 for v in preview]
    })

    st.dataframe(
        df.style
        .format({"機率": "{:.2f}"})
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]},
            {"selector": "td", "props": [("text-align", "center")]}
        ]),
        use_container_width=True,
        hide_index=True
    )
    st.subheader("抽樣方法 (Mixture Method)")

    st.markdown("先抽 mixture indicator：")

    st.latex(
    r"Z \sim \mathrm{Bernoulli}(0.55)"
    )

    st.markdown("若 Z = 1 (選擇奇數)：")

    st.latex(
    r"X \sim \mathrm{Uniform}\{5,7,9,11,13\}"
    )

    st.markdown("若 Z = 0 (選擇偶數)：")

    st.latex(
    r"X \sim \mathrm{Uniform}\{6,8,10,12,14\}"
    )

    st.markdown("因此整體分布為 mixture：")

    st.latex(
    r"""
    X =
    \begin{cases}
    \mathrm{Uniform}\{5,7,9,11,13\} & 0.55 \\
    \mathrm{Uniform}\{6,8,10,12,14\} & 0.45
    \end{cases}
    """
    )

    st.markdown("驗證：")

    st.latex(
    r"P(X=5)=0.55 \times \frac{1}{5} = 0.11"
    )

    st.latex(
    r"P(X=6)=0.45 \times \frac{1}{5} = 0.09"
    )