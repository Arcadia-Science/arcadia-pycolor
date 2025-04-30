import pandas as pd
import pytest
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import datasets

import arcadia_pycolor as apc


def _load_iris_data():
    iris = datasets.load_iris()
    iris_data = pd.DataFrame(iris.data)  # type: ignore
    iris_data.columns = [name.replace(" (cm)", "") for name in iris.feature_names]  # type: ignore
    iris_data["species"] = iris.target_names[iris.target]  # type: ignore
    return iris_data


DATASET = _load_iris_data()


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
        data=DATASET,
        x="sepal length",
        y="sepal width",
        hue="species",
        palette=colors,
        ax=ax,
        s=80,
    )
    apc.mpl.style_plot(monospaced_axes="all")


def plot_seaborn_violinplot(ax):
    """
    Plot a violin plot using Seaborn with custom colors from the Arcadia palette.
    """
    colors = {
        "setosa": "apc:aegean",
        "versicolor": apc.amber,
        "virginica": apc.seaweed,
    }
    sns.violinplot(
        data=DATASET,
        x="species",
        y="sepal width",
        hue="species",
        palette=colors,
        ax=ax,
    )
    apc.mpl.style_plot(categorical_axes="x", monospaced_axes="y")


@pytest.mark.parametrize("figure_size", apc.style_defaults.FIGURE_SIZES_IN_INCHES.keys())
@pytest.mark.parametrize(
    "plotting_function",
    [plot_seaborn_scatterplot, plot_seaborn_violinplot],
)
def test_seaborn_plots(output_dirpath, plotting_function, figure_size):
    fig, ax = plt.subplots(figsize=apc.mpl.get_figure_dimensions(figure_size), layout="constrained")
    plotting_function(ax)
    apc.mpl.save_figure(
        output_dirpath / f"{plotting_function.__name__}_{figure_size}.pdf",
        size=figure_size,
        filetypes=["pdf"],
    )
    plt.close(fig)
