from .classes_new import Color, Gradient, Palette

# Core colors
lightgrey = Color("lightgrey", "#EBEDE8")
shell = Color("shell", "#EDE0D6")
dawn = Color("dawn", "#F8F4F1")
seafoam = Color("seafoam", "#F9FCF0")
tangerine = Color("tangerine", "#FFB984")
black = Color("black", "#09090A")
charcoal = Color("charcoal", "#484B50")
marineblue = Color("marineblue", "#8A99AD")
forest = Color("forest", "#596F74")

# Neutral colors
zephyr = Color("zephyr", "#F4FBFF")
paleazure = Color("paleazure", "#F7F9FD")
lichen = Color("lichen", "#F7FBEF")
orchid = Color("orchid", "#FFFDF7")
buff = Color("buff", "#FFFBF8")
bark = Color("bark", "#8F8885")
slate = Color("slate", "#43413F")
crow = Color("crow", "#292928")

# Accent colors
aegean = Color("aegean", "#5088C5")
amber = Color("amber", "#F28360")
seaweed = Color("seaweed", "#3B9886")
canary = Color("canary", "#F7B846")
aster = Color("aster", "#7A77AB")
rose = Color("rose", "#F898AE")

# Light accent colors
bluesky = Color("bluesky", "#C6E7F4")
dress = Color("dress", "#F8C5C1")
sage = Color("sage", "#B5BEA4")
oat = Color("oat", "#F5E4BE")
periwinkle = Color("periwinkle", "#DCBFFC")
blossom = Color("blossom", "#F5CBE4")

# Accent expanded colors
lime = Color("lime", "#97CD78")
vitalblue = Color("vitalblue", "#73B5E3")
# tangerine is included in both Core and Accent
chateau = Color("chateau", "#BAB0A8")
dragon = Color("dragon", "#C85152")
# marineblue is included in both Core and Accent

# Light accent expanded colors
mint = Color("mint", "#D1EADF")
wish = Color("wish", "#BABEE0")
satin = Color("satin", "#F1E8DA")
taupe = Color("taupe", "#DAD3C7")
mars = Color("mars", "#DA9085")
denim = Color("denim", "#B6C8D4")

# Other Arcadia colors
concord = Color("concord", "#341E60")
grape = Color("grape", "#5A4596")
taffy = Color("taffy", "#E87485")
brightgrey = Color("brightgrey", "#EAEAEA")
paper = Color("paper", "#FCFCFC")
redwood = Color("redwood", "#52180A")
cocoa = Color("cocoa", "#4D2C03")
royal = Color("royal", "#3F2D5C")
carmine = Color("carmine", "#471122")
depths = Color("depths", "#09473E")
bluegrass = Color("bluegrass", "#458F99")
yucca = Color("yucca", "#1E4812")
pitaya = Color("pitaya", "#C74970")
soil = Color("soil", "#4D2500")
umber = Color("umber", "#A85E28")

# Other named colors
w = Color("w", "#FFFFFF")
r = Color("r", "#FF0000")
g = Color("g", "#00FF00")
b = Color("b", "#0000FF")
c = Color("c", "#00FFFF")
m = Color("m", "#FF00FF")
y = Color("y", "#FFFF00")
k = Color("k", "#000000")

# Core palette
CORE = Palette(
    "Core",
    [lightgrey, shell, dawn, seafoam, tangerine, black, charcoal, marineblue, forest],
)

# Neutral palette
NEUTRAL = Palette("Neutral", [zephyr, paleazure, lichen, orchid, buff, bark, slate, crow])

# Accent palette
ACCENT = Palette(
    "Accent",
    [aegean, amber, seaweed, canary, aster, rose],
)

# Light accent palette
LIGHT_ACCENT = Palette(
    "LightAccent",
    [bluesky, dress, sage, oat, periwinkle, blossom],
)

# Accent expanded palette
ACCENT_EXPANDED = Palette(
    "AccentExpanded",
    [lime, vitalblue, tangerine, chateau, marineblue, dragon],
)

# Light accent expanded palette
LIGHT_ACCENT_EXPANDED = Palette("LightAccentExpanded", [mint, wish, satin, taupe, mars, denim])

# Other Arcadia palette
ARCADIA = Palette(
    "Other",
    [
        concord,
        grape,
        taffy,
        brightgrey,
        paper,
        redwood,
        cocoa,
        royal,
        carmine,
        depths,
        bluegrass,
        yucca,
        pitaya,
        soil,
        umber,
    ],
)

# Other named palette
NAMED = Palette(
    "Named",
    [w, r, g, b, c, m, y, k],
)

# All palettes
ALL = (
    CORE
    + NEUTRAL
    + ACCENT
    + LIGHT_ACCENT
    + ACCENT_EXPANDED
    + LIGHT_ACCENT_EXPANDED
    + ARCADIA
    + NAMED
)
ALL.rename("All")


# Perceptually Uniform Gradients

VIRIDIS = Gradient(
    "viridis",
    [concord, grape, aegean, lime, y],
    [0, 0.23, 0.49, 0.77, 1],
)

MAGMA = Gradient(
    "magma",
    [black, grape, taffy, tangerine, oat],
    [0, 0.38, 0.72, 0.9, 1],
)

CIVIDIS = Gradient(
    "cividis",
    [crow, forest, canary, satin],
    [0, 0.39, 0.85, 1],
)

# Strong Monocolor Gradients
REDS = Gradient(
    "reds",
    [redwood, dragon, amber, paper],
    [0.0, 0.43, 0.64, 1.0],
)

ORANGES = Gradient(
    "oranges",
    [soil, umber, tangerine, paper],
    [0.0, 0.38, 0.8, 1.0],
)

YELLOWS = Gradient(
    "yellows",
    [cocoa, canary, oat, paper],
    [0.0, 0.76, 0.9, 1.0],
)

GREENS = Gradient(
    "greens",
    [yucca, lime, paper],
    [0, 0.7, 1],
)

TEALS = Gradient(
    "teals",
    [depths, seaweed, paper],
    [0, 0.42, 1],
)

BLUES = Gradient(
    "blues",
    [concord, aegean, vitalblue, paper],
    [0, 0.47, 0.66, 1.0],
)

PURPLES = Gradient(
    "purples",
    [royal, aster, wish, paper],
    [0, 0.4, 0.74, 1.0],
)

MAGENTAS = Gradient(
    "magentas",
    [carmine, pitaya, rose, paper],
    [0, 0.44, 0.73, 1],
)

# Weak Bicolor Gradients

AEGEANAMBER = Gradient(
    "aegeanamber",
    [aegean, paper, amber],
    [0, 0.5, 1],
)

ASTERCANARY = Gradient(
    "astercanary",
    [aster, paper, canary],
    [0, 0.5, 1],
)

LIMEROSE = Gradient(
    "limerose",
    [lime, paper, rose],
    [0, 0.5, 1],
)

SEAWEEDTANGERINE = Gradient(
    "seaweedtangerine",
    [seaweed, paper, tangerine],
    [0, 0.5, 1],
)

# Strong Bicolor Gradients

POPPIES = Gradient(
    "poppies",
    [concord, aegean, vitalblue, paper, amber, dragon, redwood],
    [0, 0.235, 0.33, 0.5, 0.68, 0.785, 1.0],
)

PANSIES = Gradient(
    "pansies",
    [royal, aster, wish, paper, oat, canary, cocoa],
    [0, 0.2, 0.37, 0.5, 0.55, 0.62, 1.0],
)

DAHLIAS = Gradient(
    "dahlias",
    [yucca, lime, paper, rose, pitaya, carmine],
    [0, 0.35, 0.5, 0.635, 0.78, 1.0],
)

LILIES = Gradient(
    "lilies",
    [depths, seaweed, paper, tangerine, umber, soil],
    [0.0, 0.21, 0.5, 0.6, 0.81, 1.0],
)
