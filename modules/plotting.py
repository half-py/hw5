import matplotlib.pyplot as plt
from modules.theory import binomial_pmf

plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False


def plot_single_x(samples, n, probabilities, selected_index):

    xi_samples = samples[:, selected_index]
    pi = probabilities[selected_index]

    fig, ax = plt.subplots(figsize=(9, 5))

    # 深色背景
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    bins = list(range(0, n + 2))
    bins = [b - 0.5 for b in bins]

    # histogram 顏色
    ax.hist(
        xi_samples,
        bins=bins,
        density=True,
        alpha=0.5,
        color="#4FC3F7",
        edgecolor="#4FC3F7",
        label=f"模擬分布 X{selected_index + 1}"
    )

    # 理論線顏色
    x_values, pmf_values = binomial_pmf(n, pi)

    ax.plot(
        x_values,
        pmf_values,
        marker="o",
        markersize=3,
        linewidth=2,
        color="#00E5FF",
        label=f"理論 Binomial({n}, {pi})"
    )

    # 文字顏色
    ax.set_title(
        f"X{selected_index + 1} 的模擬分布 vs 理論二項分布",
        color="white"
    )

    ax.set_xlabel("x", color="white")
    ax.set_ylabel("機率 / 密度", color="white")

    # 軸顏色
    ax.tick_params(colors="white")

    # 邊框顏色
    for spine in ax.spines.values():
        spine.set_color("#888888")

    # 網格
    ax.grid(alpha=0.2, color="white")

    # legend
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color("white")

    legend.get_frame().set_facecolor("#0E1117")
    legend.get_frame().set_edgecolor("#444")

    return fig