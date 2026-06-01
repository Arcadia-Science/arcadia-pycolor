import logging

import plotly.express as px
import pytest

import arcadia_pycolor as apc


def simple_plot():
    proteins = ["Protein A", "Protein B", "Protein C"]
    molecular_weights = [50, 75, 100]
    fig = px.bar(
        x=proteins,
        y=molecular_weights,
        labels={"x": "Proteins", "y": "Molecular Weight (kDa)"},
    )
    apc.plotly.style_plot(fig, categorical_axes="x", monospaced_axes="y")
    apc.plotly.set_figure_dimensions(fig, "half_square")
    return fig


@pytest.mark.parametrize(
    "fname, filetypes, expected_outputs",
    [
        ("test.pdf", None, ["test.pdf"]),
        ("test.pdf", ["pdf"], ["test.pdf"]),
        ("test.pdf", ["pdf", "png"], ["test.pdf", "test.png"]),
        ("test.pdf", ["png", "svg"], ["test.pdf", "test.png", "test.svg"]),
        ("test.pdf", ["png"], ["test.pdf", "test.png"]),
        ("test", ["pdf"], ["test.pdf"]),
        ("test", ["svg"], ["test.svg"]),
        ("test", ["pdf", "png"], ["test.pdf", "test.png"]),
    ],
)
def test_plotly_save_figure_filetype_examples(tmp_path, fname, filetypes, expected_outputs):
    """Test the `plotly.save_figure` function with various suffixes."""
    fig = simple_plot()
    apc.plotly.save_figure(
        fig,
        tmp_path / fname,
        "half_square",
        filetypes=filetypes,
    )
    for output in expected_outputs:
        output_path = tmp_path / output
        assert output_path.is_file()


@pytest.mark.parametrize(
    "fname, filetypes, expected_outputs",
    [
        # An invalid filetype is skipped (with a warning) while valid ones are still written.
        ("test.pdf", ["invalid"], ["test.pdf"]),
        ("test.invalid", ["pdf"], ["test.pdf"]),
    ],
)
def test_plotly_save_figure_filetype_invalid_skipped(
    tmp_path, fname, filetypes, expected_outputs, caplog
):
    fig = simple_plot()
    with caplog.at_level(logging.WARNING, logger="arcadia_pycolor.plotly_utils"):
        apc.plotly.save_figure(
            fig,
            tmp_path / fname,
            "float",
            filetypes=filetypes,
        )
    assert "invalid" in caplog.text.lower()
    for output in expected_outputs:
        assert (tmp_path / output).is_file()


@pytest.mark.parametrize(
    "fname, filetypes",
    [
        ("test", ["invalid"]),
        ("test.invalid", None),
    ],
)
def test_plotly_save_figure_filetype_all_invalid_raises(tmp_path, fname, filetypes):
    """When no valid filetypes remain, the function raises instead of silently doing nothing."""
    fig = simple_plot()
    with pytest.raises(ValueError):
        apc.plotly.save_figure(
            fig,
            tmp_path / fname,
            "float",
            filetypes=filetypes,
        )


def test_plotly_save_figure_no_filetype(tmp_path):
    fig = simple_plot()
    with pytest.raises(ValueError):
        apc.plotly.save_figure(
            fig,
            tmp_path / "test",
            "full_wide",
            filetypes=None,
        )
