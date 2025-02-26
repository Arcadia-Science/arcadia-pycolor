import arcadia_pycolor.colors as colors
from arcadia_pycolor.gradient import Gradient

# Perceptually Uniform Gradients.
magma = Gradient(
    "magma",
    [colors.concord, colors.tanzanite, colors.heather, colors.tumbleweed, colors.wheat],
    [0, 0.217, 0.498, 0.799, 1],
)

viridis = Gradient(
    "viridis",
    [colors.space, colors.aegean, colors.lime, colors.butter],
    [0, 0.468, 0.746, 1],
)

verde = Gradient(
    "verde",
    [colors.depths, colors.shire, colors.topaz, colors.putty],
    [0, 0.357, 0.909, 1],
)

sunset = Gradient(
    "sunset",
    [colors.soil, colors.umber, colors.tumbleweed, colors.topaz, colors.putty],
    [0.0, 0.407, 0.767, 0.915, 1.0],
)

wine = Gradient(
    "wine",
    [colors.redwood, colors.dragon, colors.tangerine, colors.dawn],
    [0, 0.451, 0.828, 1],
)

lisafrank = Gradient(
    "lisafrank",
    [colors.depths, colors.aegean, colors.wish, colors.blossom],
    [0, 0.484, 0.862, 1],
)

# Strong Monocolor Gradients.
reds = Gradient(
    "reds",
    [colors.cinnabar, colors.dragon, colors.blush],
    [0.0, 0.212, 1.0],
)

oranges = Gradient(
    "oranges",
    [colors.terracotta, colors.tangerine, colors.dawn],
    [0.0, 0.761, 1.0],
)

greens = Gradient(
    "greens",
    [colors.fern, colors.lime, colors.lichen],
    [0, 0.622, 1],
)

sages = Gradient(
    "sages",
    [colors.asparagus, colors.sage, colors.lichen],
    [0, 0.641, 1],
)

blues = Gradient(
    "blues",
    [colors.lapis, colors.aegean, colors.zephyr],
    [0, 0.254, 1.0],
)

purples = Gradient(
    "purples",
    [colors.lilac, colors.aster, colors.ghost],
    [0, 0.144, 1.0],
)

# Strong Bicolor Gradients.
orange_sage = oranges + sages.reverse()
orange_sage.name = "orange_sage"

red_blue = reds + blues.reverse()
red_blue.name = "red_blue"

purple_green = purples + greens.reverse()
purple_green.name = "purple_green"

all_gradients = [obj for obj in globals().values() if isinstance(obj, Gradient)]
