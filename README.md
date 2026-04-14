# Conditional Multinomial & Mixture Method Simulation App

這是一個使用 **Streamlit** 製作的模擬展示工具，整合了兩個作業主題：

1. **Conditional Multinomial Sampler**
   - 使用條件二項分布（conditional binomial decomposition）來模擬 multinomial 隨機向量
   - 可調整變數個數 `k`
   - 前 `k-1` 個機率手動輸入，最後一個機率自動補齊為 1
   - 比較樣本平均、理論期望值、樣本變異數、理論變異數
   - 比較樣本 covariance matrix 與理論 covariance matrix
   - 可切換檢視單一 `X_i` 的模擬分布與理論二項分布

2. **Mixture Method**
   - 使用混合方法（mixture method）模擬離散隨機變數 `X`
   - 題目分布為：
     - `P(X=j)=0.11`，當 `j=5,7,9,11,13`
     - `P(X=j)=0.09`，當 `j=6,8,10,12,14`
   - 透過 mixture indicator 先決定奇數組或偶數組，再於組內均勻抽樣
   - 提供模擬分布圖、樣本統計與樣本預覽

---

## 專案結構

```text
project/
│
├── main.py
│
└── modules/
    ├── sampler.py
    ├── theory.py
    ├── stats_utils.py
    ├── plotting.py
    └── ui/
        ├── __init__.py
        ├── app.py
        ├── sidebar.py
        ├── summary.py
        ├── single_x.py
        ├── tables.py
        ├── covariance.py
        ├── preview.py
        ├── formulas.py
        └── page_mixture.py
```

---

## 安裝方式

建議先建立虛擬環境：

### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Windows cmd

```bash
python -m venv .venv
.venv\Scripts\activate
```

接著安裝套件：

```bash
pip install -r requirements.txt
```

---

## 執行方式

在專案根目錄執行：

```bash
streamlit run main.py
```

執行後可在左側欄切換頁面：

- `Multinomial`
- `Mixture Method`

---

## 第一頁：Conditional Multinomial Sampler

若

\[
(X_1, X_2, \dots, X_k) \sim \mathrm{Multinomial}(n; p_1, p_2, \dots, p_k)
\]

則可使用條件二項分解抽樣：

\[
X_1 \sim \mathrm{Binomial}(n, p_1)
\]

\[
X_2 \mid X_1 \sim \mathrm{Binomial}\left(n-X_1, \frac{p_2}{1-p_1}\right)
\]

一般形式為：

\[
X_i \sim \mathrm{Binomial}\left(
n-\sum_{j=1}^{i-1}X_j,
\frac{p_i}{1-\sum_{j=1}^{i-1}p_j}
\right)
\]

最後一個分量為：

\[
X_k = n - \sum_{i=1}^{k-1}X_i
\]

### 理論公式

期望值：

\[
E[X_i] = n p_i
\]

變異數：

\[
\mathrm{Var}(X_i) = n p_i (1-p_i)
\]

協方差（當 `i \neq j`）：

\[
\mathrm{Cov}(X_i, X_j) = -n p_i p_j
\]

---

## 第二頁：Mixture Method

題目機率質量函數：

\[
P(X=j)=
\begin{cases}
0.11, & j=5,7,9,11,13 \\
0.09, & j=6,8,10,12,14
\end{cases}
\]

可將其視為混合分布：

- 奇數集合總機率：`5 × 0.11 = 0.55`
- 偶數集合總機率：`5 × 0.09 = 0.45`

因此先抽：

\[
Z \sim \mathrm{Bernoulli}(0.55)
\]

- 若 `Z=1`，則從 `{5,7,9,11,13}` 中均勻抽樣
- 若 `Z=0`，則從 `{6,8,10,12,14}` 中均勻抽樣

也就是：

\[
X=
\begin{cases}
\mathrm{Uniform}\{5,7,9,11,13\}, & 0.55 \\
\mathrm{Uniform}\{6,8,10,12,14\}, & 0.45
\end{cases}
\]

例如：

\[
P(X=5)=0.55 \times \frac{1}{5}=0.11
\]

\[
P(X=6)=0.45 \times \frac{1}{5}=0.09
\]

---

## 使用套件

- `streamlit`
- `numpy`
- `pandas`
- `matplotlib`

---

## Git 建議流程

### 初始化 Git

```bash
git init
git add .
git commit -m "Initial commit"
```

### 新增遠端倉庫後推送

```bash
git remote add origin <你的-repo-url>
git branch -M main
git push -u origin main
```

---

## .gitignore 建議忽略內容

已附上 `.gitignore`，會忽略：

- `.venv/`
- `__pycache__/`
- `.pyc`
- `.streamlit/`
- `.idea/`
- `.vscode/`
- 系統暫存檔

---

## 備註

這份專案適合：

- 模擬方法課程作業
- multinomial 抽樣展示
- mixture method 題目展示
- 作為 Streamlit 統計互動小工具範例
