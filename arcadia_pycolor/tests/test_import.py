def test_import_arcadia_pycolor():
    import arcadia_pycolor

    assert arcadia_pycolor is not None
    assert hasattr(arcadia_pycolor, "classes")
    assert hasattr(arcadia_pycolor, "colors")
    assert hasattr(arcadia_pycolor, "gradients")
    assert hasattr(arcadia_pycolor, "mpl")
    assert hasattr(arcadia_pycolor, "palettes")
    assert hasattr(arcadia_pycolor, "plot")
    assert hasattr(arcadia_pycolor, "Gradient")
    assert hasattr(arcadia_pycolor, "HexCode")
    assert hasattr(arcadia_pycolor, "Palette")
    assert hasattr(arcadia_pycolor, "aegean")


def test_import_apc():
    import arcadia_pycolor as apc

    assert apc is not None
    assert hasattr(apc, "classes")
    assert hasattr(apc, "colors")
    assert hasattr(apc, "gradients")
    assert hasattr(apc, "mpl")
    assert hasattr(apc, "palettes")
    assert hasattr(apc, "plot")
    assert hasattr(apc, "Gradient")
    assert hasattr(apc, "HexCode")
    assert hasattr(apc, "Palette")
    assert hasattr(apc, "aegean")
