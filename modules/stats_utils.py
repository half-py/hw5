# 匯入 NumPy 套件，主要用來做數值計算、矩陣運算、統計量計算
import numpy as np

# 匯入 pandas 套件，主要用來建立表格(DataFrame)
import pandas as pd

# 從 modules/theory.py 檔案中匯入 theoretical_covariance_matrix 函式
# 用來計算「理論上的共變異數矩陣」
from modules.theory import theoretical_covariance_matrix


# ======================================================
# 建立期望值比較表
# ======================================================
def build_expectation_table(samples, n, probabilities):
    """
    功能：
        比較樣本平均 與 理論期望值

    參數：
        samples:
            模擬產生的樣本資料（通常是矩陣）

            例如：
            [
              [2,1,0],
              [1,2,0],
              [0,3,0]
            ]

        n:
            每次試驗總次數（例如 multinomial 的 n）

        probabilities:
            各類別機率，例如：
            [0.2, 0.5, 0.3]

    回傳：
        pandas DataFrame 表格
    """

    # --------------------------------------------------
    # axis=0 表示「對每一欄取平均」
    # 也就是每個類別的樣本平均值
    # --------------------------------------------------
    empirical_mean = samples.mean(axis=0)

    # --------------------------------------------------
    # 理論期望值公式：
    # E(Xi) = n * pi
    # --------------------------------------------------
    theoretical_mean = n * probabilities

    # --------------------------------------------------
    # 絕對誤差 = |樣本平均 - 理論值|
    # np.abs() 取絕對值
    # --------------------------------------------------
    abs_error = np.abs(empirical_mean - theoretical_mean)

    # --------------------------------------------------
    # 建立標籤名稱
    # len(probabilities) = 類別數
    #
    # 若有3類：
    # ["X1","X2","X3"]
    #
    # f-string 語法：
    # f"X{i+1}" 可把變數放入字串中
    # --------------------------------------------------
    labels = [f"X{i+1}" for i in range(len(probabilities))]

    # --------------------------------------------------
    # 建立 pandas 表格
    # key = 欄位名稱
    # value = 該欄資料
    # --------------------------------------------------
    df = pd.DataFrame({
        "類別": labels,
        "樣本平均": empirical_mean,
        "理論期望值": theoretical_mean,
        "絕對誤差": abs_error
    })

    return df


# ======================================================
# 建立變異數比較表
# ======================================================
def build_variance_table(samples, n, probabilities):
    """
    功能：
        比較樣本變異數 與 理論變異數
    """

    # --------------------------------------------------
    # np.var() 計算變異數
    #
    # axis=0 ：每欄計算一次
    #
    # ddof=1：
    # 使用樣本變異數公式（除以 n-1）
    # 若 ddof=0 則是母體變異數
    # --------------------------------------------------
    empirical_var = np.var(samples, axis=0, ddof=1)

    # --------------------------------------------------
    # multinomial 每個 Xi 的理論變異數：
    #
    # Var(Xi) = n*pi*(1-pi)
    # --------------------------------------------------
    theoretical_var = n * probabilities * (1 - probabilities)

    # 絕對誤差
    abs_error = np.abs(empirical_var - theoretical_var)

    # 建立類別名稱
    labels = [f"X{i+1}" for i in range(len(probabilities))]

    # 建立表格
    df = pd.DataFrame({
        "類別": labels,
        "樣本變異數": empirical_var,
        "理論變異數": theoretical_var,
        "絕對誤差": abs_error
    })

    return df


# ======================================================
# 建立共變異數比較結果
# ======================================================
def build_covariance_results(samples, n, probabilities):
    """
    功能：
        比較樣本共變異數矩陣 與 理論共變異數矩陣

    回傳：
        empirical_cov   = 樣本共變異數矩陣
        theoretical_cov = 理論共變異數矩陣
        abs_error       = 絕對誤差矩陣
    """

    # --------------------------------------------------
    # np.cov() 計算共變異數矩陣
    #
    # rowvar=False 很重要：
    #
    # False 表示：
    # 每一欄是一個變數
    # 每一列是一筆觀測值
    #
    # 這通常是資料科學最常見格式
    # --------------------------------------------------
    empirical_cov = np.cov(samples, rowvar=False, ddof=1)

    # --------------------------------------------------
    # 呼叫你自己寫的理論函式
    # 計算 multinomial 的理論共變異數矩陣
    # --------------------------------------------------
    theoretical_cov = theoretical_covariance_matrix(n, probabilities)

    # --------------------------------------------------
    # 每個位置做誤差比較
    # --------------------------------------------------
    abs_error = np.abs(empirical_cov - theoretical_cov)

    return empirical_cov, theoretical_cov, abs_error