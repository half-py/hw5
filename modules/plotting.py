# 匯入 matplotlib 的 pyplot 模組
# 常用來畫圖
import matplotlib.pyplot as plt

# 從 modules/theory.py 匯入 binomial_pmf 函式
# 用來取得二項分配的理論機率
from modules.theory import binomial_pmf


# =====================================================
# 全域字型設定
# =====================================================

# 設定中文字型為 微軟正黑體
# 避免圖表中文亂碼
plt.rcParams["font.family"] = "Microsoft JhengHei"

# 避免負號顯示成方塊
plt.rcParams["axes.unicode_minus"] = False


# =====================================================
# 畫單一 Xi 的分布圖
# =====================================================
def plot_single_x(samples, n, probabilities, selected_index):
    """
    功能：
        畫出某一個 Xi 的：

        1. 模擬直方圖
        2. 理論 Binomial 分布線圖

    參數：

    samples:
        模擬資料矩陣

        假設 shape = (模擬次數, 類別數)

    n:
        試驗總次數

    probabilities:
        各類別機率
        例如 [0.2,0.5,0.3]

    selected_index:
        要畫哪一欄

        0 表 X1
        1 表 X2
        2 表 X3
    """

    # -------------------------------------------------
    # 取出第 selected_index 欄資料
    #
    # samples[:, j]
    #
    # : 表所有列
    # j 表第 j 欄
    # -------------------------------------------------
    xi_samples = samples[:, selected_index]

    # 該 Xi 對應的機率 pi
    pi = probabilities[selected_index]

    # 建立圖形與座標軸
    fig, ax = plt.subplots(figsize=(9, 5))

    # =================================================
    # 深色背景
    # =================================================
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    # -------------------------------------------------
    # 建立 histogram 的箱子區間
    #
    # 若 n=5
    #
    # range(0,n+2)
    # -> 0,1,2,3,4,5,6
    #
    # 再每個減0.5
    #
    # -> -0.5,0.5,1.5,...,5.5
    #
    # 這樣整數值會剛好落在箱子中央
    # -------------------------------------------------
    bins = list(range(0, n + 2))
    bins = [b - 0.5 for b in bins]

    # =================================================
    # 畫模擬直方圖
    # =================================================
    ax.hist(
        xi_samples,

        # 分箱範圍
        bins=bins,

        # 正規化成機率比例
        density=True,

        # 透明度
        alpha=0.5,

        # 顏色
        color="#4FC3F7",

        edgecolor="#4FC3F7",

        # 圖例名稱
        label=f"模擬分布 X{selected_index + 1}"
    )

    # =================================================
    # 取得理論 Binomial PMF
    # =================================================
    x_values, pmf_values = binomial_pmf(n, pi)

    # x_values = 0~n
    # pmf_values = 對應機率

    # =================================================
    # 畫理論折線圖
    # =================================================
    ax.plot(
        x_values,
        pmf_values,

        marker="o",      # 點樣式
        markersize=3,    # 點大小
        linewidth=2,     # 線寬

        color="#00E5FF",

        label=f"理論 Binomial({n}, {pi})"
    )

    # =================================================
    # 標題
    # =================================================
    ax.set_title(
        f"X{selected_index + 1} 的模擬分布 vs 理論二項分布",
        color="white"
    )

    # x軸名稱
    ax.set_xlabel("x", color="white")

    # y軸名稱
    ax.set_ylabel("機率 / 密度", color="white")

    # =================================================
    # 座標軸刻度顏色
    # =================================================
    ax.tick_params(colors="white")

    # =================================================
    # 邊框顏色
    # =================================================
    for spine in ax.spines.values():

        # spine 就是上下左右邊框線
        spine.set_color("#888888")

    # =================================================
    # 網格線
    # =================================================
    ax.grid(alpha=0.2, color="white")

    # =================================================
    # 圖例
    # =================================================
    legend = ax.legend()

    # 圖例文字白色
    for text in legend.get_texts():
        text.set_color("white")

    # 圖例背景
    legend.get_frame().set_facecolor("#0E1117")

    # 圖例邊框
    legend.get_frame().set_edgecolor("#444")

    # 回傳圖物件
    return fig