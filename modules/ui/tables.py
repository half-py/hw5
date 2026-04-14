import streamlit as st


def render_expectation_table(df):
    st.subheader("Expectation comparison")

    st.dataframe(
        df.style.format({
            "樣本平均": "{:.4f}",
            "理論期望值": "{:.4f}",
            "絕對誤差": "{:.4f}",
        }),
        use_container_width=True
    )


def render_variance_table(df):
    st.subheader("Variance comparison")

    st.dataframe(
        df.style.format({
            "樣本變異數": "{:.4f}",
            "理論變異數": "{:.4f}",
            "絕對誤差": "{:.4f}",
        }),
        use_container_width=True
    )