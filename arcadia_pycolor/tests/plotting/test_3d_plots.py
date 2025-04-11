import plotly.express as px
import plotly.graph_objects as go
import pytest

import arcadia_pycolor as apc

IRIS_DATASET = px.data.iris()


def plot_3d_scatter_plot_with_plotly_express():
    """Plot a 3D scatter plot using Plotly Express."""
    fig = px.scatter_3d(
        IRIS_DATASET,
        x="sepal_length",
        y="sepal_width",
        z="petal_width",
        color="species",
        size="sepal_length",
        color_discrete_map={
            "setosa": apc.aegean,
            "versicolor": apc.amber,
            "virginica": apc.seaweed,
        },
    )
    apc.plotly.style_plot(fig, monospaced_axes="all")
    return fig


def plot_3d_scatter_plot_with_plotly_graph_objects():
    """Plot a 3D scatter plot using Plotly Graph Objects."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=IRIS_DATASET["sepal_length"],
            y=IRIS_DATASET["sepal_width"],
            z=IRIS_DATASET["petal_width"],
            mode="markers",
            marker=dict(
                size=5,
                color=IRIS_DATASET["species"].map(
                    {
                        "setosa": apc.aegean,
                        "versicolor": apc.amber,
                        "virginica": apc.seaweed,
                    }
                ),
                opacity=0.8,
            ),
            text=IRIS_DATASET["species"],
            hoverinfo="text",
        )
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="sepal_length",
            yaxis_title="sepal_width",
            zaxis_title="petal_width",
        ),
        showlegend=False,
    )

    apc.plotly.style_plot(fig, monospaced_axes="all")
    return fig


@pytest.mark.parametrize(
    "plotting_function",
    [
        plot_3d_scatter_plot_with_plotly_express,
        plot_3d_scatter_plot_with_plotly_graph_objects,
    ],
)
def test_3d_plots_with_plotly(output_dirpath, plotting_function):
    fig = plotting_function()
    fig.write_html(output_dirpath / f"{plotting_function.__name__}.html")
