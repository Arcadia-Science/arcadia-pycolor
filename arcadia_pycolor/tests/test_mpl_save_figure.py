import logging

import matplotlib.pyplot as plt
import pytest

import arcadia_pycolor as apc


def simple_plot():
    plt.figure(figsize=(3, 3))
    plt.plot([1, 2, 3], [1, 2, 3])


@pytest.mark.parametrize(
    "fname, filetypes, expected_outputs",
    [
        ("test.pdf", None, ["test.pdf"]),
        ("test.pdf", ["pdf"], ["test.pdf"]),
        ("test.pdf", ["pdf", "png"], ["test.pdf", "test.png"]),
        ("test.pdf", ["png", "eps"], ["test.pdf", "test.png", "test.eps"]),
        ("test.pdf", ["png"], ["test.pdf", "test.png"]),
        ("test", ["pdf"], ["test.pdf"]),
        ("test", ["pdf", "png"], ["test.pdf", "test.png"]),
    ],
)
def test_mpl_save_figure_filetype_examples(tmp_path, fname, filetypes, expected_outputs):
    """
    Test the `mpl.save_figure` function with various suffixes.
    """

    simple_plot()
    apc.mpl.save_figure(
        tmp_path / fname,
        size="half_square",
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
def test_mpl_save_figure_filetype_invalid_skipped(
    tmp_path, fname, filetypes, expected_outputs, caplog
):
    simple_plot()

    with caplog.at_level(logging.WARNING, logger="arcadia_pycolor.mpl"):
        apc.mpl.save_figure(
            tmp_path / fname,
            size="half_square",
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
def test_mpl_save_figure_filetype_all_invalid_raises(tmp_path, fname, filetypes):
    """When no valid filetypes remain, the function raises instead of silently doing nothing."""
    simple_plot()

    with pytest.raises(ValueError):
        apc.mpl.save_figure(
            tmp_path / fname,
            size="half_square",
            filetypes=filetypes,
        )


def test_mpl_save_figure_no_filetype(tmp_path):
    simple_plot()

    with pytest.raises(ValueError):
        apc.mpl.save_figure(
            tmp_path / "test",
            size="half_square",
            filetypes=None,
        )
