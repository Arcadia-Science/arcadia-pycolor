import numpy as np
import pytest
import seaborn as sns
from matplotlib import pyplot as plt

import arcadia_pycolor as apc


@pytest.mark.parametrize("figure_size", apc.style_defaults.FIGURE_SIZES_IN_INCHES.keys())
def test_plot_stacked_barplot(output_dirpath, figure_size):
    """
    Plot a stacked barplot using custom mocked data and colors from the Arcadia palette.
    """
    fig, ax = plt.subplots(figsize=apc.mpl.get_figure_dimensions(figure_size), layout="constrained")
    categories = ["Water", "Salt", "Drug A", "Drug B", "Drug C"]
    subcategories = ["Dead", "Malformed", "Alive"]
    data = np.array(
        [
            [5, 10, 15],
            [7, 14, 21],
            [10, 20, 30],
            [3, 6, 20],
            [23, 4, 7],
        ]
    )

    # Initialize the bottom array to 0.
    bottom = np.zeros(len(categories))

    colors = [apc.denim, apc.canary, apc.seaweed]
    for ind in range(len(subcategories)):
        ax.bar(categories, data[:, ind], bottom=bottom, label=subcategories[ind], color=colors[ind])
        bottom += data[:, ind]

    ax.set_xlabel("Condition")
    ax.set_ylabel("Number of embryos")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(reversed(handles), reversed(labels))
    legend = ax.get_legend()
    assert legend is not None
    legend.set_title("Viability")

    apc.mpl.style_plot(ax, categorical_axes="x", monospaced_axes="y")
    apc.mpl.save_figure(
        output_dirpath / f"test_plot_stacked_barplot_{figure_size}.pdf",
        size=figure_size,
        filetypes=["pdf"],
    )
    plt.close(fig)


@pytest.mark.parametrize("figure_size", apc.style_defaults.FIGURE_SIZES_IN_INCHES.keys())
def test_plot_multiple_line_plot(output_dirpath, figure_size):
    """
    Plot multiple line plots using custom mocked data and colors from the Arcadia palette.
    Note: the line plots are not stacked; they are independently plotted on separate axes.
    """
    lines = np.random.rand(10, 20)
    fig, axes = plt.subplots(
        nrows=len(lines),
        figsize=apc.mpl.get_figure_dimensions(figure_size),
    )

    colors = [apc.aegean, apc.gray, apc.dragon]
    cmap = apc.Gradient(name="", colors=colors).to_mpl_cmap()

    for ind, line in enumerate(lines):
        ax = axes[ind]  # type: ignore
        color = cmap(ind / len(lines))
        ax.plot(line, color=color)
        apc.mpl.style_plot(axes=ax, monospaced_axes="all")
        ax.set_yticks([])

        if ind != len(lines) - 1:
            ax.spines["bottom"].set_visible(False)
            ax.set_xticks([])
        else:
            ax.set_xlabel("Time (s)")

    fig.supylabel("Brightness")
    fig.subplots_adjust(hspace=0)
    apc.mpl.save_figure(
        output_dirpath / f"test_plot_multiple_line_plot_{figure_size}.pdf",
        size=figure_size,
        filetypes=["pdf"],
    )
    plt.close(fig)


@pytest.mark.parametrize("figure_size", apc.style_defaults.FIGURE_SIZES_IN_INCHES.keys())
def test_plot_heatmaps_with_seaborn(output_dirpath, figure_size):
    """
    Plot a heatmap using Seaborn with a colormap from an Arcadia gradient.
    """
    random_data = np.random.rand(8, 8)

    fig, axes = plt.subplots(
        1, 2, figsize=apc.mpl.get_figure_dimensions(figure_size), layout="constrained"
    )
    sns.heatmap(
        random_data,
        ax=axes[0],  # type: ignore
        square=True,
        cmap="apc:magma",
        cbar_kws={"label": "Intensity"},
        annot=True,
        annot_kws={"fontsize": 12},
    )
    sns.heatmap(
        random_data - 0.5,
        ax=axes[1],  # type: ignore
        square=True,
        cmap="apc:purple_green",
        cbar_kws={"label": "Intensity"},
    )

    for ax in axes:  # type: ignore
        apc.mpl.style_plot(
            ax,
            categorical_axes="all",
            monospaced_axes="all",
            colorbar_exists=True,
        )
        ax.set_xlabel("Category 1")
        ax.set_ylabel("Category 2")

    apc.mpl.save_figure(
        output_dirpath / f"test_plot_heatmaps_with_seaborn_{figure_size}.pdf",
        size=figure_size,
        filetypes=["pdf"],
    )
    plt.close(fig)
