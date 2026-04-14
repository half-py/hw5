import streamlit as st


def render_formula_section():
    st.subheader("理論公式說明")

    with st.expander("查看 multinomial 的理論公式"):

        st.markdown("若")

        st.latex(
            r"(X_1, X_2, \dots, X_k) \sim \mathrm{Multinomial}(n; p_1, p_2, \dots, p_k)"
        )

        st.markdown("且")

        st.latex(
            r"\sum_{i=1}^{k} p_i = 1"
        )

        st.markdown("則各分量滿足：")

        st.markdown("### 1. 期望值")

        st.latex(
            r"E[X_i] = n p_i"
        )

        st.markdown("### 2. 變異數")

        st.latex(
            r"\mathrm{Var}(X_i) = n p_i (1 - p_i)"
        )

        st.markdown("### 3. 協方差")

        st.latex(
         r"\mathrm{Cov}(X_i, X_j) = - n p_i p_j \qquad (i \ne j)"
        )

        st.markdown("### 4. 總和限制")

        st.latex(
            r"X_1 + X_2 + \cdots + X_k = n"
        )
        st.markdown("## 抽樣方法：條件二項分布分解")

        st.markdown("Multinomial 可以用條件二項分布依序抽樣：")

        st.latex(
        r"X_1 \sim \mathrm{Binomial}(n,p_1)"
        )

        st.latex(
        r"X_2 \mid X_1 \sim \mathrm{Binomial}\left(n-X_1,\frac{p_2}{1-p_1}\right)"
        )

        st.latex(
        r"X_3 \mid X_1,X_2 \sim \mathrm{Binomial}\left(n-X_1-X_2,\frac{p_3}{1-p_1-p_2}\right)"
        )

        st.markdown("一般形式：")

        st.latex(
        r"""
        X_i
        \sim
        \mathrm{Binomial}
        \left(
        n-\sum_{j=1}^{i-1}X_j,
        \frac{p_i}{1-\sum_{j=1}^{i-1}p_j}
        \right)
        """
        )

        st.markdown("最後一個分量為剩餘數量：")

        st.latex(
        r"X_k = n-\sum_{i=1}^{k-1}X_i"
        )


    st.divider()