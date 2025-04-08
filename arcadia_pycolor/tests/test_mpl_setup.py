import arcadia_pycolor as apc


def test_mpl_setup():
    """Test that `mpl.setup` can be called multiple times without raising an error.

    TODO: consider adding more complex tests.
    """
    apc.mpl.setup()
    apc.mpl.setup()
