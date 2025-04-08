import arcadia_pycolor as apc


def test_plotly_setup():
    """Test that `plotly.setup` can be called multiple times without raising an error.

    TODO: consider adding more complex tests.
    """
    apc.plotly.setup()
    apc.plotly.setup()
