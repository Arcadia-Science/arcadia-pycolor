# arcadia-pycolor
Tools for using the Arcadia palette in Python.  
This package automatically generate color palettes and color maps for use with Matplotlib.

# Installation
You can install this package directly from GitHub using pip.
First, make sure you're using the right `pip` for your desired environment.  
`which pip`

Install using the pip in that environment.  
`pip install git+https://github.com/Arcadia-Science/arcadia-pycolor.git#egg=arcadia_pycolor`

## Import

Import the colors as follows.  
You can access the `'color':'HEX'` dictionaries from the below options:
- `arcadia_Core`: Core colors such as `'arcadia:forest'`
- `arcadia_Neutral`: Dark and light colors for lines and backgrounds.
- `arcadia_Accent`: Bright accent colors for figure labels. Colorblind-safe.
- `arcadia_Light_accent`: Light accent colors for figure labels. Colorblind-safe.
- `arcadia_Accent_expanded`: Additional bright accent colors for figure labels that are compatible with Accent colors.
- `arcadia_Light_accent_expanded`: Additional light accent colors for figure labels that are compatible with Light_accent colors.


```python
import arcadia_pycolor as apc

display(apc.arcadia_Accent)
```


    {'arcadia:aegean': '#5088C5',
     'arcadia:amber': '#F28360',
     'arcadia:seaweed': '#3B9886',
     'arcadia:canary': '#F7B846',
     'arcadia:aster': '#7A77AB',
     'arcadia:rose': '#F898AE'}


## Matplotlib Named Colors
Arcadia colors are automatically added to the named colors list in Matplotlib.  
You can access them using a string such as `'arcadia:seaweed'`.


```python
import matplotlib.pyplot as plt
import numpy as np

colors = ['arcadia:seaweed', 'arcadia:amber']

plt.figure(figsize = (3, 2))

for color in colors:
    x, y = np.arange(5), np.random.rand(5)
    plt.plot(x, y, color = color, label = color)
    
plt.legend(loc = 'upper right', bbox_to_anchor = (1.8, 1))
plt.show()
```


    
![png](README_files/README_4_0.png)
    


## Matplotlib Named `LinearSegmentedColorMap`s

All Arcadia colors can be loaded as `LinearSegmentedColorMap` objects in a gradient starting or ending with white (`#FFFFFF`).  
These colors are added to the `mpl.colormaps` dictionary and can be accessed as follows:

- `'arcadia:color'` + `'s'` (e.g. `'arcadia:asters'`): starts with white and goes to color
- `'arcadia:color'` + `'s_r'` (e.g. `'arcadia:asters_r'`): starts with color and goes to white


```python
import matplotlib as mpl

data = [np.arange(0, 11)]
fig, (ax1, ax2) = plt.subplots(nrows=2)

ax1.imshow(data, cmap='arcadia:asters')
ax2.imshow(data, cmap='arcadia:asters_r')

plt.show()
```


    
![png](README_files/README_6_0.png)
    


## Matplotlib Bicolor `LinearSegmentedColorMap`s

Three pairs of colors are automatically loaded as opposing `LinearSegmentedColorMap` objects:
- `arcadia:amber` and `arcadia:aegean` ==> `arcadia:aegeanamber` or `arcadia:aegeanamber_r`
- `arcadia:canary` and `arcadia:aster` ==> `arcadia:astercanary` or `arcadia:astercanary_r`
- `arcadia:rose` and `arcadia:seaweed` ==> `arcadia:seaweedrose` or `arcadia:seaweedrose_r`

These color pairs are good for showing over/under plots such as heatmaps, and are colorblind-friendly for protanopia, deuteranopia, and tritanopia.


```python
data = [np.arange(0, 11)]
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)

ax1.imshow(data, cmap='arcadia:aegeanamber')
ax2.imshow(data, cmap='arcadia:astercanary_r')
ax3.imshow(data, cmap='arcadia:seaweedrose')

plt.show()

apc.plot_examples([mpl.colormaps['arcadia:aegeanamber'], 
                   mpl.colormaps['arcadia:astercanary_r'], 
                   mpl.colormaps['arcadia:seaweedrose']])
```


    
![png](README_files/README_8_0.png)
    



    
![png](README_files/README_8_1.png)
    


## Matplotlib `ListedColormap`s

This package also includes some selected `ListedColormap` objects to cycle through when you have a variable number of samples to plot.  
The colors are selected to be visually distinct and (mostly) colorblind-friendly regardless of the number of samples, up to 12 samples for each Accent and Light palettes.  

You can also combine the two palettes together to get up to 24 distinct colors (although this becomes less colorblind-friendly).

The palettes are:
- `arcadia:AccentOrdered`
- `arcadia:LightOrdered`
- `arcadia:AllOrdered`: AccentOrdered followed by LightOrdered.


```python
data = [np.arange(0, 12)]

fig, (ax1, ax2) = plt.subplots(nrows=2)

ax1.imshow(data, cmap='arcadia:AccentOrdered')
ax1.title.set_text('AccentOrdered')
ax2.imshow(data, cmap='arcadia:LightOrdered')
ax2.title.set_text('LightOrdered')

plt.show()

apc.randspline_colortest('arcadia:AccentOrdered', 4)
apc.randspline_colortest('arcadia:AccentOrdered', 8)
apc.randspline_colortest('arcadia:LightOrdered', 12)
```


    
![png](README_files/README_10_0.png)
    



    
![png](README_files/README_10_1.png)
    



    
![png](README_files/README_10_2.png)
    



    
![png](README_files/README_10_3.png)
    



```python

```
