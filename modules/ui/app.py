# 匯入 NumPy
# 用來建立亂數產生器
import numpy as np

# 匯入 Streamlit
# 用來建立互動網頁介面
import streamlit as st


# =====================================================
# 匯入自己專案中的模組
# =====================================================

# 條件式 Multinomial 抽樣器類別
from modules.sampler import ConditionalMultinomialSampler

# 匯入 stats_utils.py 所有函式
# （期望值表、變異數表、共變異數等）
from modules.stats_utils import *

# 左側欄設定
from .sidebar import render_sidebar

# 摘要區塊
from .summary import render_summary

# 單一 Xi 分布區塊
from .single_x import render_single_x_section

# 表格區塊全部匯入
from .tables import *

# 共變異數區塊
from .covariance import render_covariance_section

# 樣本預覽區塊
from .preview import render_sample_preview

# 理論公式區塊
from .formulas import render_formula_section

# Mixture Method 頁面
from .page_mixture import render_mixture_page


# =====================================================
# Multinomial 主頁面
# =====================================================
def render_multinomial():
    """
    顯示 Multinomial 模擬頁面
    """

    # 頁面標題
    st.title("Conditional Multinomial Sampler")

    # -------------------------------------------------
    # 從 sidebar 取得使用者設定參數
    #
    # n            = 試驗次數
    # sample_size  = 模擬樣本數
    # probabilities= 機率向量
    # seed         = 亂數種子
    # -------------------------------------------------
    n, sample_size, probabilities, seed = render_sidebar()

    # 建立亂數產生器
    rng = np.random.default_rng(seed)

    # 建立抽樣器物件
    sampler = ConditionalMultinomialSampler(probabilities, rng)

    # -------------------------------------------------
    # 產生很多筆樣本
    #
    # shape 可能是：
    # (sample_size, 類別數)
    # -------------------------------------------------
    samples = sampler.sample_many(n, sample_size)

    # =================================================
    # 建立統計表格資料
    # =================================================

    # 期望值比較表
    expectation_df = build_expectation_table(
        samples,
        n,
        probabilities
    )

    # 變異數比較表
    variance_df = build_variance_table(
        samples,
        n,
        probabilities
    )

    # -------------------------------------------------
    # 共變異數結果
    #
    # empirical_cov   = 樣本共變異數
    # theoretical_cov = 理論共變異數
    # abs_cov_error   = 誤差矩陣
    # -------------------------------------------------
    empirical_cov, theoretical_cov, abs_cov_error = (
        build_covariance_results(
            samples,
            n,
            probabilities
        )
    )

    # =================================================
    # 開始渲染畫面區塊
    # =================================================

    # 基本摘要資訊
    render_summary(
        n,
        sample_size,
        probabilities
    )

    # 單一 Xi 分布圖
    render_single_x_section(
        samples,
        n,
        probabilities
    )

    # 期望值表格
    render_expectation_table(
        expectation_df
    )

    # 變異數表格
    render_variance_table(
        variance_df
    )

    # 共變異數區塊
    render_covariance_section(
        probabilities,
        empirical_cov,
        theoretical_cov,
        abs_cov_error
    )

    # 樣本預覽表格
    render_sample_preview(
        samples,
        probabilities
    )

    # 理論公式說明
    render_formula_section()


# =====================================================
# App 主入口
# =====================================================
def run_app():
    """
    整個 Streamlit App 的入口函式
    """

    # -------------------------------------------------
    # 頁面設定
    #
    # page_title = 瀏覽器標題
    # layout="wide" = 寬版畫面
    # -------------------------------------------------
    st.set_page_config(
        page_title="Simulation Methods",
        layout="wide"
    )

    # -------------------------------------------------
    # 側邊欄選單
    #
    # radio = 單選按鈕
    # -------------------------------------------------
    page = st.sidebar.radio(
        "選擇頁面",
        [
            "Multinomial",
            "Mixture Method"
        ]
    )

    # =================================================
    # 根據選項切換頁面
    # =================================================

    if page == "Multinomial":

        # 顯示 multinomial 頁面
        render_multinomial()

    else:

        # 顯示 mixture 頁面
        render_mixture_page()