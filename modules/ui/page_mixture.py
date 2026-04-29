# 匯入 NumPy
# 用來做亂數、陣列、平均值等數值運算
import numpy as np

# 匯入 Streamlit
# 用來建立網頁互動介面
import streamlit as st

# 匯入 matplotlib
# 用來畫圖
import matplotlib.pyplot as plt


# =====================================================
# Mixture 抽樣函式
# =====================================================
def mixture_sample(n, rng):
    """
    功能：
        產生 n 筆混合分布樣本

    分布規則：

    先抽 Z ~ Bernoulli(0.55)

    若 Z=1：
        從奇數集合 {5,7,9,11,13} 等機率抽一個

    若 Z=0：
        從偶數集合 {6,8,10,12,14} 等機率抽一個
    """

    # 建立空 list 存樣本
    samples = []

    # 重複抽樣 n 次
    for _ in range(n):

        # -------------------------------------------------
        # rng.random() 產生 0~1 均勻亂數
        #
        # 若 < 0.55 回傳 True
        # 否則 False
        #
        # True 表示抽到奇數組
        # False 表示抽到偶數組
        # -------------------------------------------------
        z = rng.random() < 0.55

        # 若 z=True
        if z:

            # 從奇數集合隨機選一個
            x = rng.choice([5, 7, 9, 11, 13])

        else:
            # 從偶數集合隨機選一個
            x = rng.choice([6, 8, 10, 12, 14])

        # 放入樣本清單
        samples.append(x)

    # list 轉 numpy array
    return np.array(samples)


# =====================================================
# Streamlit 頁面函式
# =====================================================
def render_mixture_page():

    # 網頁標題
    st.title("Mixture Method 模擬 X")

    # 顯示數學公式
    st.latex(
    r"""
    P(X=j)=
    \begin{cases}
    0.11 & j=5,7,9,11,13 \\
    0.09 & j=6,8,10,12,14
    \end{cases}
    """
    )

    # -------------------------------------------------
    # 滑桿設定樣本數
    #
    # 最小500
    # 最大20000
    # 預設5000
    # -------------------------------------------------
    sample_size = st.slider(
        "樣本數",
        500,
        20000,
        5000
    )

    # 固定亂數種子，結果可重現
    rng = np.random.default_rng(42)

    # 產生樣本
    samples = mixture_sample(sample_size, rng)

    # -------------------------------------------------
    # 左右分欄
    # 左欄寬2
    # 右欄寬1
    # -------------------------------------------------
    left, right = st.columns([2, 1])

    # =================================================
    # 左邊：圖表區
    # =================================================
    with left:

        # 建立圖與座標軸
        fig, ax = plt.subplots(figsize=(7,4))

        # 設深色背景
        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        # x 軸可能值：5~14
        values = np.arange(5,15)

        # -------------------------------------------------
        # 理論機率
        #
        # 奇數 -> 0.11
        # 偶數 -> 0.09
        #
        # v % 2 == 1 表奇數
        # -------------------------------------------------
        probs = [
            0.11 if v % 2 == 1 else 0.09
            for v in values
        ]

        # -------------------------------------------------
        # 畫直方圖
        #
        # density=True 表示轉成機率密度比例
        # -------------------------------------------------
        ax.hist(
            samples,
            bins=np.arange(4.5,15.5,1),
            density=True,
            alpha=0.5,
            color="#4FC3F7",
            edgecolor="#4FC3F7",
            label="simulation"
        )

        # -------------------------------------------------
        # 畫理論折線圖
        # -------------------------------------------------
        ax.plot(
            values,
            probs,
            marker="o",
            linewidth=2,
            color="#00E5FF",
            label="theoretical"
        )

        # 標題
        ax.set_title("Mixture 模擬分布", color="white")

        # 座標字顏色
        ax.tick_params(colors="white")

        # 邊框顏色
        for spine in ax.spines.values():
            spine.set_color("#888")

        # 格線
        ax.grid(alpha=0.2, color="white")

        # 圖例
        legend = ax.legend()

        for text in legend.get_texts():
            text.set_color("white")

        legend.get_frame().set_facecolor("#0E1117")

        # 顯示圖
        st.pyplot(fig)

    # =================================================
    # 右邊：統計資訊
    # =================================================
    with right:

        st.subheader("統計資訊")

        # 平均數
        st.metric(
            "樣本平均",
            f"{samples.mean():.4f}"
        )

        # 變異數
        st.metric(
            "樣本變異數",
            f"{samples.var():.4f}"
        )

        # 最小值
        st.metric(
            "最小值",
            int(samples.min())
        )

        # 最大值
        st.metric(
            "最大值",
            int(samples.max())
        )

    # 分隔線
    st.divider()

    # =================================================
    # 樣本預覽區
    # =================================================
    st.subheader("樣本預覽")

    # 顯示前幾筆資料滑桿
    preview_n = st.slider(
        "顯示筆數",
        min_value=5,
        max_value=30,
        value=10
    )

    # 取前 preview_n 筆
    preview = samples[:preview_n]

    # 這裡才匯入 pandas 也可以
    import pandas as pd

    # 建立表格
    df = pd.DataFrame({
        "編號": range(1, preview_n + 1),
        "X": preview,

        # 若 v % 2 !=0 為奇數
        "類型": ["奇數" if v % 2 else "偶數" for v in preview],

        # 對應機率
        "機率": [0.11 if v % 2 else 0.09 for v in preview]
    })

    # 顯示資料表
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

    # =================================================
    # 理論說明區
    # =================================================
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
    r"P(X=5)=0.55 \times \frac{1}{5}=0.11"
    )

    st.latex(
    r"P(X=6)=0.45 \times \frac{1}{5}=0.09"
    )