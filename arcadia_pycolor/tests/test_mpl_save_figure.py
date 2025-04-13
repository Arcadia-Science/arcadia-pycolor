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
    "fname, filetypes",
    [
        ("test.pdf", ["invalid"]),
        ("test", ["invalid"]),
        ("test.invalid", ["pdf"]),
        ("test.invalid", None),
    ],
)
def test_mpl_save_figure_filetype_invalid(tmp_path, fname, filetypes, capsys):
    simple_plot()

    apc.mpl.save_figure(
        tmp_path / fname,
        size="half_square",
        filetypes=filetypes,
    )

    captured = capsys.readouterr()
    assert "Invalid filetype 'invalid'. Skipping." in captured.out


def test_mpl_save_figure_no_filetype(tmp_path):
    simple_plot()

    with pytest.raises(ValueError):
        apc.mpl.save_figure(
            tmp_path / "test",
            size="half_square",
            filetypes=None,
        )
