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
