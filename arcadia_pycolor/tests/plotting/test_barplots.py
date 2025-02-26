import pytest
import seaborn as sns
from matplotlib import pyplot as plt

import arcadia_pycolor as apc

BARPLOT_NUM_READS = [
    1_500_000,
    1_200_000,
    1_000_000,
    400_000,
    1_000_000,
    1_700_000,
    1_300_000,
    600_000,
    1_200_000,
    1_500_000,
    1_600_000,
    300_000,
    900_000,
    1_700_000,
    800_000,
]
BARPLOT_SAMPLE_IDS = [
    "AL 4M",
    "EL 2W",
    "EL 4W",
    "EL 4W WGA",
    "EL 12W",
    "OM 2W",
    "OM 4W",
    "OM 4W WGA",
    "OM 8W",
    "WH 1M",
    "WH 2M",
    "WH 2M WGA",
    "WH 4M",
    "WH 2M Hous",
    "WI 3W",
]
BARPLOT_ERRORS = [
    100000,
    80000,
    70000,
    30000,
    70000,
    120000,
    90000,
    40000,
    80000,
    100000,
    110000,
    20000,
    60000,
    120000,
    50000,
]


def _word_wrap_sample_ids(sample_ids):
    return [sample_id.replace(" ", "\n") for sample_id in sample_ids]


def plot_vertical_barplot_with_matplotlib_with_error_bars(ax):
    """
    Plot a vertical barplot using Matplotlib with error bars.
    """
    sample_ids = _word_wrap_sample_ids(BARPLOT_SAMPLE_IDS)
    plt.bar(sample_ids, BARPLOT_NUM_READS, color=apc.aster)
    apc.mpl.style_plot(ax, monospaced_axes="y")
    apc.mpl.set_xaxis_categorical()
    apc.mpl.add_commas_to_axis_tick_labels(ax.get_yaxis())

    plt.errorbar(sample_ids, BARPLOT_NUM_READS, yerr=BARPLOT_ERRORS, fmt="none", color=apc.crow)
    plt.ylabel("Number of reads")
    plt.xlabel("Sample")


def plot_horizontal_barplot_with_matplotlib_with_error_bars(ax):
    """
    Plot a horizontal barplot using Matplotlib.
    This plot is identical to the vertical version, but with the x and y axes swapped.
    """
    plt.barh(BARPLOT_SAMPLE_IDS, BARPLOT_NUM_READS, color=apc.aster)
    apc.mpl.style_plot(ax, monospaced_axes="x")
    apc.mpl.set_yaxis_categorical()
    apc.mpl.add_commas_to_axis_tick_labels(ax.get_xaxis())
    plt.xticks(rotation=30, ha="right")

    plt.errorbar(
        BARPLOT_NUM_READS, BARPLOT_SAMPLE_IDS, xerr=BARPLOT_ERRORS, fmt="none", color=apc.crow
    )
    plt.xlabel("Number of reads")
    plt.ylabel("Sample")


def plot_vertical_barplot_with_matplotlib_with_categories(ax):
    """
    Plot a vertical barplot using Matplotlib with bar colors based on categories
    derived from the sample IDs.
    """
    sample_categories = [sample_id.split(" ")[0] for sample_id in BARPLOT_SAMPLE_IDS]
    category_to_color = dict(
        zip(set(sample_categories), [apc.aster, apc.aegean, apc.amber, apc.seaweed, apc.rose])
    )
    colors = [category_to_color[category] for category in sample_categories]

    plt.bar(
        _word_wrap_sample_ids(BARPLOT_SAMPLE_IDS),
        BARPLOT_NUM_READS,
        color=colors,
    )
    apc.mpl.style_plot(ax, monospaced_axes="y")
    apc.mpl.set_xaxis_categorical()
    apc.mpl.add_commas_to_axis_tick_labels(ax.get_yaxis())
    plt.ylabel("Number of reads")
    plt.xlabel("Sample")


def plot_vertical_barplot_with_seaborn(ax):
    """
    Plot a vertical barplot using Seaborn.
    """
    sns.barplot(
        x=_word_wrap_sample_ids(BARPLOT_SAMPLE_IDS),
        y=BARPLOT_NUM_READS,
        color=apc.aster,
        # Seaborn by default desaturates the colors. This prevents that.
        saturation=1,
        ax=ax,
    )
    apc.mpl.style_plot(ax, monospaced_axes="y")
    apc.mpl.set_xaxis_categorical()
    apc.mpl.add_commas_to_axis_tick_labels(ax.get_yaxis())
    plt.ylabel("Number of reads")
    plt.xlabel("Sample")


def plot_horizontal_barplot_with_seaborn(ax):
    """
    Plot a horizontal barplot using Seaborn.
    This plot is identical to the vertical version, but with the x and y axes swapped.
    """
    sns.barplot(x=BARPLOT_NUM_READS, y=BARPLOT_SAMPLE_IDS, color=apc.aster, saturation=1, ax=ax)
    apc.mpl.style_plot(ax, monospaced_axes="x")
    apc.mpl.set_yaxis_categorical()
    apc.mpl.add_commas_to_axis_tick_labels(ax.get_xaxis())
    plt.xticks(rotation=30, ha="right")
    plt.xlabel("Number of reads")
    plt.ylabel("Sample")


def plot_vertical_barplot_with_seaborn_with_categories(ax):
    """
    Plot a vertical barplot using Seaborn with bar colors based on categories
    derived from the sample IDs.
    """
    sample_categories = [sample_id.split(" ")[0] for sample_id in BARPLOT_SAMPLE_IDS]
    category_to_color = dict(
        zip(set(sample_categories), [apc.aster, apc.aegean, apc.amber, apc.seaweed, apc.rose])
    )

    sns.barplot(
        x=_word_wrap_sample_ids(BARPLOT_SAMPLE_IDS),
        y=BARPLOT_NUM_READS,
        color=apc.aster,
        hue=sample_categories,
        palette=category_to_color,
        saturation=1,
        ax=ax,
    )

    apc.mpl.style_plot(ax, monospaced_axes="y")
    apc.mpl.set_xaxis_categorical()
    apc.mpl.add_commas_to_axis_tick_labels(ax.get_yaxis())

    plt.xlabel("Number of reads")
    plt.ylabel("Sample")

    legend = ax.get_legend()
    legend.set_title("ID")
    legend.set_bbox_to_anchor((1.06, 1))


@pytest.mark.parametrize(
    "plotting_function",
    [
        plot_vertical_barplot_with_matplotlib_with_error_bars,
        plot_horizontal_barplot_with_matplotlib_with_error_bars,
        plot_vertical_barplot_with_matplotlib_with_categories,
        plot_vertical_barplot_with_seaborn,
        plot_horizontal_barplot_with_seaborn,
        plot_vertical_barplot_with_seaborn_with_categories,
    ],
)
@pytest.mark.parametrize("figure_size", apc.style_defaults.FIGURE_SIZES.keys())
def test_barplots(output_dirpath, plotting_function, figure_size):
    fig, ax = plt.subplots(figsize=apc.mpl.get_figure_dimensions(figure_size), layout="constrained")
    plotting_function(ax)
    apc.mpl.save_figure(
        output_dirpath / f"{plotting_function.__name__}_{figure_size}.pdf",
        filetypes=["pdf"],
    )
    plt.close(fig)
