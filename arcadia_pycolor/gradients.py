import arcadia_pycolor.colors as colors
from arcadia_pycolor.gradient import Gradient

# Perceptually Uniform Gradients
viridis = Gradient(
    "viridis",
    [colors.concord, colors.grape, colors.aegean, colors.lime, colors.yellow],
    [0, 0.23, 0.49, 0.77, 1],
)

magma = Gradient(
    "magma",
    [colors.pitch, colors.grape, colors.taffy, colors.tangerine, colors.oat],
    [0, 0.38, 0.72, 0.9, 1],
)

cividis = Gradient(
    "cividis",
    [colors.crow, colors.forest, colors.canary, colors.satin],
    [0, 0.39, 0.85, 1],
)

# Strong Monocolor Gradients
reds = Gradient(
    "reds",
    [colors.redwood, colors.dragon, colors.amber, colors.paper],
    [0.0, 0.43, 0.64, 1.0],
)

oranges = Gradient(
    "oranges",
    [colors.soil, colors.umber, colors.tangerine, colors.paper],
    [0.0, 0.38, 0.8, 1.0],
)

yellows = Gradient(
    "yellows",
    [colors.cocoa, colors.canary, colors.oat, colors.paper],
    [0.0, 0.76, 0.9, 1.0],
)

greens = Gradient(
    "greens",
    [colors.yucca, colors.lime, colors.paper],
    [0, 0.7, 1],
)

teals = Gradient(
    "teals",
    [colors.depths, colors.seaweed, colors.paper],
    [0, 0.42, 1],
)

blues = Gradient(
    "blues",
    [colors.concord, colors.aegean, colors.vitalblue, colors.paper],
    [0, 0.47, 0.66, 1.0],
)

purples = Gradient(
    "purples",
    [colors.royal, colors.aster, colors.wish, colors.paper],
    [0, 0.4, 0.74, 1.0],
)

magentas = Gradient(
    "magentas",
    [colors.carmine, colors.pitaya, colors.rose, colors.paper],
    [0, 0.44, 0.73, 1],
)

# Weak Bicolor Gradients
aegean_amber = Gradient(
    "aegean_amber",
    [colors.aegean, colors.paper, colors.amber],
    [0, 0.5, 1],
)

aster_canary = Gradient(
    "aster_canary",
    [colors.aster, colors.paper, colors.canary],
    [0, 0.5, 1],
)

lime_rose = Gradient(
    "lime_rose",
    [colors.lime, colors.paper, colors.rose],
    [0, 0.5, 1],
)

seaweed_tangerine = Gradient(
    "seaweed_tangerine",
    [colors.seaweed, colors.paper, colors.tangerine],
    [0, 0.5, 1],
)

# Strong Bicolor Gradients
poppies = Gradient(
    "poppies",
    [
        colors.concord,
        colors.aegean,
        colors.vitalblue,
        colors.paper,
        colors.amber,
        colors.dragon,
        colors.redwood,
    ],
    [0, 0.235, 0.33, 0.5, 0.68, 0.785, 1.0],
)

pansies = Gradient(
    "pansies",
    [
        colors.royal,
        colors.aster,
        colors.wish,
        colors.paper,
        colors.oat,
        colors.canary,
        colors.cocoa,
    ],
    [0, 0.2, 0.37, 0.5, 0.55, 0.62, 1.0],
)

dahlias = Gradient(
    "dahlias",
    [colors.yucca, colors.lime, colors.paper, colors.rose, colors.pitaya, colors.carmine],
    [0, 0.35, 0.5, 0.635, 0.78, 1.0],
)

lillies = Gradient(
    "lillies",
    [colors.depths, colors.seaweed, colors.paper, colors.tangerine, colors.umber, colors.soil],
    [0.0, 0.21, 0.5, 0.6, 0.81, 1.0],
)
