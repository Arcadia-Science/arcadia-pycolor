import arcadia_pycolor


def test_import_arcadia_pycolor():
    assert arcadia_pycolor is not None

    attrs = [
        "classes",
        "colors",
        "gradients",
        "mpl",
        "palettes",
        "plot",
        "Gradient",
        "HexCode",
        "Palette",
        "aegean",
    ]

    for attr in attrs:
        assert hasattr(arcadia_pycolor, attr)
