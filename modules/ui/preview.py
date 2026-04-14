import pandas as pd
import streamlit as st


def render_sample_preview(samples, probabilities):
    st.subheader("樣本預覽")

    preview_count = st.slider(
        "顯示前幾筆樣本",
        min_value=5,
        max_value=min(50, len(samples)),
        value=min(10, len(samples)),
        step=1
    )

    labels = [f"X{i+1}" for i in range(len(probabilities))]

    preview_df = pd.DataFrame(
        samples[:preview_count],
        columns=labels
    )
    preview_df["sum"] = preview_df.sum(axis=1)

    st.dataframe(preview_df, use_container_width=True)

    st.divider()