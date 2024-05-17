from .classes_new import Color, Palette

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
