import numpy as np


class ConditionalMultinomialSampler:
    """
    使用條件二項分佈依序抽樣來產生 multinomial 樣本

    若
        (X1,...,Xk) ~ Multinomial(n; p1,...,pk)

    則可用條件二項分解：

        X1 ~ Binomial(n, p1)

        X2 | X1 ~ Binomial(
                        n-X1 ,
                        p2/(1-p1)
                        )

        X3 | X1,X2 ~ Binomial(
                        n-X1-X2 ,
                        p3/(1-p1-p2)
                        )

        ...

        Xk = 剩餘數量
    """

    def __init__(self, probabilities, rng=None):
        """
        probabilities : (p1,...,pk)
        rng : numpy random generator
        """

        # 驗證機率是否合法
        self.probabilities = self._validate_probabilities(probabilities)

        # 若沒有提供隨機數產生器，建立一個固定 seed 的
        self.rng = rng if rng is not None else np.random.default_rng(seed=42)

    def sample(self, n):
        """
        產生一筆 multinomial 樣本

        回傳:
            [X1,X2,...,Xk]
        """

        # n 必須 >=0
        if n < 0:
            raise ValueError("n must be non-negative.")

        # 建立結果向量
        # 例如 k=4 → [0,0,0,0]
        counts = np.zeros(len(self.probabilities), dtype=int)

        # 剩餘尚未分配的樣本數
        # 一開始全部是 n
        remaining_count = n

        # 剩餘機率質量
        # 一開始總機率為 1
        remaining_probability = 1.0

        # 依序抽前 k-1 個
        # 最後一個直接補剩餘
        for category_index, category_probability in enumerate(self.probabilities[:-1]):

            # 如果已經分完就停止
            if remaining_count == 0:
                break

            """
            條件機率計算

            原本機率:
                p_i

            條件化後:
                p_i / (剩餘機率)

            即：

            p_i / (1 - p1 - ... - p_{i-1})
            """
            conditional_probability = (
                category_probability /
                remaining_probability
            )

            # 保證數值落在 [0,1]
            conditional_probability = np.clip(
                conditional_probability,
                0.0,
                1.0
            )

            """
            抽樣

            Xi ~ Binomial(
                    剩餘樣本數 ,
                    條件機率
                 )
            """
            sampled_count = self.rng.binomial(
                remaining_count,
                conditional_probability
            )

            # 存入 Xi
            counts[category_index] = sampled_count

            # 更新剩餘樣本數
            remaining_count -= sampled_count

            # 更新剩餘機率
            remaining_probability -= category_probability

        """
        最後一個變數直接補剩餘

        Xk = n - (X1+...+X_{k-1})
        """
        counts[-1] = remaining_count

        return counts

    def sample_many(self, n, sample_size):
        """
        產生多筆 multinomial 樣本

        回傳 shape:

            (sample_size , k)
        """

        if sample_size < 0:
            raise ValueError("sample_size must be non-negative.")

        # 建立結果矩陣
        samples = np.zeros(
            (sample_size, len(self.probabilities)),
            dtype=int
        )

        # 重複抽樣
        for sample_index in range(sample_size):

            # 每一列是一筆 multinomial
            samples[sample_index] = self.sample(n)

        return samples

    @staticmethod
    def _validate_probabilities(probabilities):
        """
        檢查機率是否合法
        """

        # 轉 numpy array
        probabilities = np.asarray(
            probabilities,
            dtype=float
        )

        # 必須為一維
        if probabilities.ndim != 1:
            raise ValueError("probabilities must be a 1D vector.")

        # 機率不可為負
        if np.any(probabilities < 0):
            raise ValueError("probabilities must be non-negative.")

        # 總和必須為 1
        total_probability = probabilities.sum()

        if not np.isclose(total_probability, 1.0):
            raise ValueError(
                f"probabilities must sum to 1, got {total_probability}."
            )

        return probabilities