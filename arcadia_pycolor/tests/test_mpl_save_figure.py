import matplotlib.pyplot as plt
import pytest

import arcadia_pycolor as apc


def simple_plot():
    plt.figure(figsize=(3, 3))
    plt.plot([1, 2, 3], [1, 2, 3])


@pytest.mark.parametrize(
    "fname, fname_types, expected_outputs",
    [
        ("test.pdf", None, ["test.pdf"]),
        ("test.pdf", ["pdf"], ["test.pdf"]),
        ("test.pdf", ["pdf", "png"], ["test.pdf", "test.png"]),
        ("test.pdf", ["png", "eps"], ["test.pdf", "test.png", "test.eps"]),
        ("test.pdf", ["png"], ["test.pdf", "test.png"]),
        ("test", None, ["test.pdf"]),
        ("test", ["pdf"], ["test.pdf"]),
        ("test", ["pdf", "png"], ["test.pdf", "test.png"]),
    ],
)
def test_mpl_save_figure_suffix_examples(tmp_path, fname, fname_types, expected_outputs):
    """
    Test the `mpl.save_figure` function with various suffixes.
    """

    simple_plot()
    apc.mpl.save_figure(fname=tmp_path / fname, fname_types=fname_types)

    for output in expected_outputs:
        output_path = tmp_path / output
        assert output_path.is_file()


@pytest.mark.parametrize(
    "fname, fname_types",
    [
        ("test.pdf", ["invalid"]),
        ("test", ["invalid"]),
        ("test.invalid", ["pdf"]),
    ],
)
def test_mpl_save_figure_fname_suffix_invalid(tmp_path, fname, fname_types, capsys):
    simple_plot()

    apc.mpl.save_figure(fname=tmp_path / fname, fname_types=fname_types)

    captured = capsys.readouterr()
    assert "Invalid file suffix 'invalid'. Skipping." in captured.out


def test_mpl_save_figure_fname_suffix_invalid_no_fname_types(tmp_path):
    simple_plot()

    with pytest.raises(ValueError):
        apc.mpl.save_figure(fname=tmp_path / "test.invalid")
