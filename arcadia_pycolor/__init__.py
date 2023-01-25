import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

arcadia_Core = {
    'arcadia:lightgrey': '#EBEDE8',
    'arcadia:shell': '#EDE0D6',
    'arcadia:dawn': '#F8F4F1',
    'arcadia:seafoam': '#F9FCF0',
    'arcadia:orange': '#FFB984',
    'arcadia:black': '#09090A',
    'arcadia:charcoal': '#484B50',
    'arcadia:marineblue': '#8A99AD',
    'arcadia:forest': '#596F74'
}

arcadia_Neutral = {
    'arcadia:zephyr': '#F4FBFF',
    'arcadia:paleazure': '#F7F9FD',
    'arcadia:lichen': '#F7FBEF',
    'arcadia:orchid': '#FFFDF7',
    'arcadia:buff': '#FFFBF8',
    'arcadia:bark': '#8F8885',
    'arcadia:slate': '#43413F',
    'arcadia:crow': '#292928'
}

arcadia_Accent = {
    'arcadia:aegean': '#5088C5', 
    'arcadia:amber': '#F28360', 
    'arcadia:seaweed': '#3B9886', 
    'arcadia:canary': '#F7B846', 
    'arcadia:aster': '#7A77AB', 
    'arcadia:rose': '#F898AE',
}

arcadia_Light = {
    'arcadia:bluesky': '#C6E7F4',
    'arcadia:dress': '#F8C5C1',
    'arcadia:sage': '#B5BEA4',
    'arcadia:oat': '#F5E4BE',
    'arcadia:periwinkle': '#DCBFFC',
    'arcadia:blossom': '#F5CBE4'
}

arcadia_Accent_expanded = {
    'arcadia:lime': '#97CD78',
    'arcadia:vitalblue': '#73B5E3',
    'arcadia:orange': '#FFB984',
    'arcadia:chateau': '#BAB0A8',
    'arcadia:dragon': '#C85152',
    'arcadia:marineblue': '#8A99AD',
}

arcadia_Light_expanded = {
    'arcadia:mint': '#D1EADF',
    'arcadia:wish': '#BABEE0',
    'arcadia:satin': '#F1E8DA',
    'arcadia:taupe': '#DAD3C7',
    'arcadia:mars': '#DA9085',
    'arcadia:denim': '#B6C8D4'
}

arcadia_all = arcadia_Core | arcadia_Neutral | arcadia_Accent | arcadia_Light | arcadia_Accent_expanded | arcadia_Light_expanded
arcadia_Accent_full = arcadia_Accent | arcadia_Accent_expanded
arcadia_Light_full = arcadia_Light | arcadia_Light_expanded

plt.cm.colors.get_named_colors_mapping().update(arcadia_all)

def plot_examples(colormaps):
    """
    Helper function to plot data with associated colormap.
    """
    np.random.seed(19680801)
    data = np.random.randn(30, 30)
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
        fig.colorbar(psm, ax=ax)
    plt.show()
    
def randspline_colortest(cmap, nlines = 8, timepoints = 6, title = '', save = ''):
    from cycler import cycler
    import numpy as np
    
    default_cycler = (cycler(color=mpl.colormaps[cmap].colors))
    plt.rc('axes', prop_cycle=default_cycler)
    
    for i in np.arange(nlines):
        x = np.arange(timepoints)
        y = np.random.rand(timepoints)
        
        spline = make_interp_spline(x, y)
        
        X_ = np.linspace(x.min(), x.max(), 500)
        Y_ = spline(X_)
        
        plt.plot(X_, Y_, label = str(i), linewidth = 3)
    
    plt.title(title)
    plt.legend(loc = 'upper right', bbox_to_anchor = (1.2, 1))
    
    if save != '':
        plt.savefig(save)
    plt.show()

for color in arcadia_all:
    colors = ['white', color]
    cmapname = color + 's'
    cmap = mpl.colors.LinearSegmentedColormap.from_list(cmapname, colors)
    cmap_r = cmap.reversed()
    mpl.colormaps.register(cmap=cmap)
    mpl.colormaps.register(cmap=cmap_r)

arcadia_color_pairs = [
    ['arcadia:aegean', 'arcadia:amber'],
    ['arcadia:aster', 'arcadia:canary'],
    ['arcadia:seaweed', 'arcadia:rose']
]

for colors in arcadia_color_pairs:
    topcolorname = colors[0] + 's_r'
    bottomcolorname = colors[1] + 's'
    jointname = colors[0] + colors[1].replace('arcadia:', '')
    
    top = mpl.colormaps[topcolorname]
    bottom = mpl.colormaps[bottomcolorname]
    
    bicolors = np.vstack((top(np.linspace(0, 1, 128)),
                       bottom(np.linspace(0, 1, 128))))
    bicmap = mpl.colors.ListedColormap(bicolors, name=jointname)
    bicmap_r = bicmap.reversed()
    mpl.colormaps.register(cmap=bicmap)
    mpl.colormaps.register(cmap=bicmap_r)

arcadia_Accent_ordered = {
    'arcadia:aegean': '#5088C5', 
    'arcadia:amber': '#F28360',  
    'arcadia:canary': '#F7B846', 
    'arcadia:lime': '#97CD78',
    'arcadia:aster': '#7A77AB',
    'arcadia:rose': '#F898AE',
    'arcadia:seaweed': '#3B9886',
    'arcadia:dragon': '#C85152',
    'arcadia:vitalblue': '#73B5E3',
    'arcadia:chateau': '#BAB0A8',
    'arcadia:marineblue': '#8A99AD',
    'arcadia:orange': '#FFB984'
}

arcadia_Light_ordered = {
    'arcadia:bluesky': '#C6E7F4',
    'arcadia:dress': '#F8C5C1',
    'arcadia:oat': '#F5E4BE',
    'arcadia:sage': '#B5BEA4',
    'arcadia:periwinkle': '#DCBFFC',
    'arcadia:denim': '#B6C8D4',
    'arcadia:taupe': '#DAD3C7',
    'arcadia:mars': '#DA9085',
    'arcadia:blossom': '#F5CBE4',
    'arcadia:mint': '#D1EADF',
    'arcadia:wish': '#BABEE0',
    'arcadia:satin': '#F1E8DA'
}

arcadia_All_ordered = arcadia_Accent_ordered | arcadia_Light_ordered

arcadia_Accent_ordered_cmap = mpl.colors.ListedColormap(arcadia_Accent_ordered.keys(), name = 'arcadia:AccentOrdered')
arcadia_Light_ordered_cmap = mpl.colors.ListedColormap(arcadia_Light_ordered.keys(), name = 'arcadia:LightOrdered')
arcadia_All_ordered_cmap = mpl.colors.ListedColormap(arcadia_All_ordered.keys(), name = 'arcadia:AllOrdered')
mpl.colormaps.register(cmap=arcadia_Accent_ordered_cmap)
mpl.colormaps.register(cmap=arcadia_Light_ordered_cmap)
mpl.colormaps.register(cmap=arcadia_All_ordered_cmap)


color_lists = {
    'arcadia:viridis': {
        'colors': ["arcadia:crow", "arcadia:aegean", "arcadia:lime", "yellow"],
        'nodes': [0, 0.49, 0.75, 1]
    },
    'arcadia:magma': {
        'colors': ["arcadia:black", "#5A4596", "#E87485", "arcadia:orange", "arcadia:oat"],
        'nodes': [0, 0.38, 0.72, 0.9, 1]
    }
}

def make_LSCM(key, colors, nodes):
    if nodes == []:
        cmap = mpl.colors.LinearSegmentedColormap.from_list(key, colors)
    else:
        cmap = mpl.colors.LinearSegmentedColormap.from_list(key, list(zip(nodes, colors)))
    
    if key not in mpl.colormaps.keys():
        mpl.colormaps.register(cmap=cmap)

for key, attr in color_lists.items():
    make_LSCM(key, attr['colors'], attr['nodes'])