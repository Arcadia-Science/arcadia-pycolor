import pandas as pd
import pytest
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import datasets

import arcadia_pycolor as apc
from arcadia_pycolor import mpl

FIGURE_SIZES = [
    "full_wide",
    "full_square",
    "float_wide",
    "float_square",
    "half_square",
]

BARPLOT_DATA = {
    "num_reads": [
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
    ],
    "sample_id": [
        "AL 4M",
        "EL 2W",
        "EL 4W",
        "EL 4W",
        "EL 12W",
        "OM 2W",
        "OM 4W",
        "OM 4W",
        "OM 8W",
        "WH 1M",
        "WH 2M",
        "WH 2M",
        "WH 4M",
        "WH 2M",
        "WI 3W",
    ],
    "error": [
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
    ],
}


@pytest.fixture(scope="module", autouse=True)
def setup_matplotlib():
    apc.mpl.setup()


def iris_data():
    """
    Load the iris dataset and create a DataFrame.
    """
    iris = datasets.load_iris()
    iris_data = pd.DataFrame(iris.data)
    iris_data.columns = [name.replace(" (cm)", "") for name in iris.feature_names]
    iris_data["species"] = iris.target_names[iris.target]
    return iris_data


SCATTERPLOT_DATA = iris_data()


def plot_seaborn_scatterplot(ax):
    """
    Plot a scatterplot using Seaborn with custom colors from the Arcadia palette.
    """
    colors = {
        "setosa": "apc:aegean",
        "versicolor": apc.amber,
        "virginica": apc.seaweed,
    }
    sns.scatterplot(
        data=SCATTERPLOT_DATA,
        x="sepal length",
        y="sepal width",
        hue="species",
        palette=colors,
        ax=ax,
        s=80,
    )
    apc.mpl.style_axis(monospaced_axes="both")


@pytest.mark.parametrize("figure_size", FIGURE_SIZES)
def test_scatterplot(tmpdir, figure_size):
    fig, ax = plt.subplots(figsize=apc.mpl.get_figure_dimensions(figure_size), layout="constrained")
    plot_seaborn_scatterplot(ax)
    apc.mpl.save_figure(fname=(tmpdir / f"scatterplot_{figure_size}.pdf"))
    plt.close(fig)
    assert True


def plot_vertical_matplotlib_barplot(ax):
    """
    Plot a vertical barplot using Matplotlib with error bars.
    """
    plt.bar(BARPLOT_DATA["sample_id"], BARPLOT_DATA["num_reads"], color=apc.aster)
    apc.mpl.style_axis(ax, monospaced_axes="y")
    apc.mpl.set_xaxis_categorical()

    # Use commas in the numbers used for y-axis tick labels.
    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: format(int(x), ",")))
    plt.errorbar(
        BARPLOT_DATA["sample_id"],
        BARPLOT_DATA["num_reads"],
        yerr=BARPLOT_DATA["error"],
        fmt="none",
        color=apc.crow,
    )
    plt.ylabel("Number of reads")
    plt.xlabel("Sample")


def plot_horizontal_matplotlib_barplot(ax):
    """
    Plot a horizontal barplot using Matplotlib.
    This plot is identical to the vertical version, but with the x and y axes swapped.
    """
    plt.barh(BARPLOT_DATA["sample_id"], BARPLOT_DATA["num_reads"], color=apc.aster)
    apc.mpl.style_axis(ax, monospaced_axes="x")
    apc.mpl.set_yaxis_categorical()

    # Use commas in the numbers used for x-axis tick labels.
    ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: format(int(x), ",")))
    plt.xticks(rotation=30, ha="right")

    plt.errorbar(
        BARPLOT_DATA["num_reads"],
        BARPLOT_DATA["sample_id"],
        xerr=BARPLOT_DATA["error"],
        fmt="none",
        color=apc.crow,
    )
    plt.xlabel("Number of reads")
    plt.ylabel("Sample")


def plot_horizontal_matplotlib_barplot_with_categories(ax):
    """
    Plot a horizontal barplot using Matplotlib with bar colors based on categories.
    """
    color_labels = [sample_id.split(" ")[0] for sample_id in BARPLOT_DATA["sample_id"]]
    color_dict = dict(
        zip(set(color_labels), [apc.aster, apc.aegean, apc.amber, apc.seaweed, apc.rose])
    )

    plt.bar(BARPLOT_DATA["sample_id"], BARPLOT_DATA["num_reads"], color=color_dict.values())
    apc.mpl.style_axis(ax, monospaced_axes="y")
    apc.mpl.set_xaxis_categorical()

    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: format(int(x), ",")))
    plt.ylabel("Number of reads")
    plt.xlabel("Sample")
