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
- `arcadia_Neural`: 
- `arcadia_Accent`
- `arcadia_Light_accent`
- `arcadia_Accent_expanded`
- `arcadia_Light_accent_expanded`


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

display(mpl.colormaps['arcadia:asters'])
display(mpl.colormaps['arcadia:asters_r'])
```


<div style="vertical-align: middle;"><strong>arcadia:asters</strong> </div><div class="cmap"><img alt="arcadia:asters colormap" title="arcadia:asters" style="border: 1px solid #555;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABsv8+/AAAAHXRFWHRUaXRsZQBhcmNhZGlhOmFzdGVycyBjb2xvcm1hcHljWx8AAAAjdEVYdERlc2NyaXB0aW9uAGFyY2FkaWE6YXN0ZXJzIGNvbG9ybWFwf0i+7gAAADB0RVh0QXV0aG9yAE1hdHBsb3RsaWIgdjMuNS4zLCBodHRwczovL21hdHBsb3RsaWIub3JnZ9HokgAAADJ0RVh0U29mdHdhcmUATWF0cGxvdGxpYiB2My41LjMsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmdJd3e1AAABjUlEQVR4nO3WwWrCQBRA0Wn//5/HRUUxrTQkTWdxz9kEw9M3GJH7MeecY4xxv4z75WFubjxf/vH86+UxuHn7mOPn+VV7D88v3vu8fex7+/+9+871bX5z3st+v7/sPfs8V+3dPf/mPKv2nn2+x/dee67L/gdP7j37PFftfTu/83tbtXfzsQfmv3wOACBHAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIEgAAECQAACBIAABAkAAAgCABAABBAgAAggQAAAQJAAAIugHgd2QqCBwNAwAAAABJRU5ErkJggg=="></div><div style="vertical-align: middle; max-width: 514px; display: flex; justify-content: space-between;"><div style="float: left;"><div title="#ffffffff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #ffffffff;"></div> under</div><div style="margin: 0 auto; display: inline-block;">bad <div title="#00000000" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #00000000;"></div></div><div style="float: right;">over <div title="#7a77abff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #7a77abff;"></div></div>



<div style="vertical-align: middle;"><strong>arcadia:asters_r</strong> </div><div class="cmap"><img alt="arcadia:asters_r colormap" title="arcadia:asters_r" style="border: 1px solid #555;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABsv8+/AAAAH3RFWHRUaXRsZQBhcmNhZGlhOmFzdGVyc19yIGNvbG9ybWFwNCqs5AAAACV0RVh0RGVzY3JpcHRpb24AYXJjYWRpYTphc3RlcnNfciBjb2xvcm1hcOntbMQAAAAwdEVYdEF1dGhvcgBNYXRwbG90bGliIHYzLjUuMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZ2fR6JIAAAAydEVYdFNvZnR3YXJlAE1hdHBsb3RsaWIgdjMuNS4zLCBodHRwczovL21hdHBsb3RsaWIub3JnSXd3tQAAAZFJREFUeJzt1kFuwjAUQEG7l67UK/WQ7QpR0kYgEurFm9mgEIdvJSh68+P982v8MOcYt8dz/H1+Hls/Lx9zc3x74eby3fWr5j68fmc/q+Zef+a557tq7u/1m/N37tPL9vXi57lq7u76B+/bqrlHn+/5c8/Z12nvwXvr/+t/tHju9X313H1bNffo+sv3bwMAyBEAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIK+AfR9BHyzlklHAAAAAElFTkSuQmCC"></div><div style="vertical-align: middle; max-width: 514px; display: flex; justify-content: space-between;"><div style="float: left;"><div title="#7a77abff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #7a77abff;"></div> under</div><div style="margin: 0 auto; display: inline-block;">bad <div title="#00000000" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #00000000;"></div></div><div style="float: right;">over <div title="#ffffffff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #ffffffff;"></div></div>


## Matplotlib Bicolor `LinearSegmentedColorMap`s

Three pairs of colors are automatically loaded as opposing `LinearSegmentedColorMap` objects:
- `arcadia:amber` and `arcadia:aegean` ==> `arcadia:aegeanamber` or `arcadia:aegeanamber_r`
- `arcadia:canary` and `arcadia:aster` ==> `arcadia:astercanary` or `arcadia:astercanary_r`
- `arcadia:rose` and `arcadia:seaweed` ==> `arcadia:seaweedrose` or `arcadia:seaweedrose_r`

These color pairs are good for showing over/under plots such as heatmaps, and are colorblind-friendly for protanopia, deuteranopia, and tritanopia.


```python
display(mpl.colormaps['arcadia:aegeanamber'])
display(mpl.colormaps['arcadia:astercanary_r'])
display(mpl.colormaps['arcadia:seaweedrose'])

apc.plot_examples([mpl.colormaps['arcadia:aegeanamber'], 
                   mpl.colormaps['arcadia:astercanary_r'], 
                   mpl.colormaps['arcadia:seaweedrose']])
```


<div style="vertical-align: middle;"><strong>arcadia:aegeanamber</strong> </div><div class="cmap"><img alt="arcadia:aegeanamber colormap" title="arcadia:aegeanamber" style="border: 1px solid #555;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABsv8+/AAAAInRFWHRUaXRsZQBhcmNhZGlhOmFlZ2VhbmFtYmVyIGNvbG9ybWFwe5UIPgAAACh0RVh0RGVzY3JpcHRpb24AYXJjYWRpYTphZWdlYW5hbWJlciBjb2xvcm1hcI0izl4AAAAwdEVYdEF1dGhvcgBNYXRwbG90bGliIHYzLjUuMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZ2fR6JIAAAAydEVYdFNvZnR3YXJlAE1hdHBsb3RsaWIgdjMuNS4zLCBodHRwczovL21hdHBsb3RsaWIub3JnSXd3tQAAAblJREFUeJzt1klSwkAAQNGGE3osL+a1jAuShWAqjWBJ1X9vQxLogTDUP729fyxjjHEaF6f14LwebOen9eB8db73+tvxO9fHz/POrjO//jrv+H6+P352/Tv3P73+vff/YN6xs875YB/jaB+/vA9H72/80bxP+35Mfr9n9z/um/dZv8/NsnxuBzuPc88vD46/vr48OP5p+xsvvr+r52/n2Rs/d31+vhf5PHc+r5fZ33/fv3F53P7vAIAQAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAg6AtGKwtjnN7/PwAAAABJRU5ErkJggg=="></div><div style="vertical-align: middle; max-width: 514px; display: flex; justify-content: space-between;"><div style="float: left;"><div title="#5088c5ff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #5088c5ff;"></div> under</div><div style="margin: 0 auto; display: inline-block;">bad <div title="#00000000" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #00000000;"></div></div><div style="float: right;">over <div title="#f28360ff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #f28360ff;"></div></div>



<div style="vertical-align: middle;"><strong>arcadia:astercanary_r</strong> </div><div class="cmap"><img alt="arcadia:astercanary_r colormap" title="arcadia:astercanary_r" style="border: 1px solid #555;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABsv8+/AAAAJHRFWHRUaXRsZQBhcmNhZGlhOmFzdGVyY2FuYXJ5X3IgY29sb3JtYXC7ACM8AAAAKnRFWHREZXNjcmlwdGlvbgBhcmNhZGlhOmFzdGVyY2FuYXJ5X3IgY29sb3JtYXCs+tmpAAAAMHRFWHRBdXRob3IATWF0cGxvdGxpYiB2My41LjMsIGh0dHBzOi8vbWF0cGxvdGxpYi5vcmdn0eiSAAAAMnRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHYzLjUuMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZ0l3d7UAAAG7SURBVHic7dZLUsJAFEDRjotzze7MWeIA1BLEfEAd3HMmqaQqrxsIqTu9vjwvY4wxxnQ+nI/jad/5dD7fOWdanXNs7tY5V+vvnrNxfzfum/bO3b2fn+d8fv7L7+HO9TbOWf38N3/vo/tZef4O7+fYnNXnb23uwf/r9LGvk3k+vQaW5f04Ls5/6fqd687/tO726xfn8537Pnp9/v76fPC+R+/36vu4ue7v7mOZ79z3H637qOfy61sAAEgQAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACCBAAABAkAAAgSAAAQJAAAIEgAAECQAACAIAEAAEECAACC3gBbfVUqqxvAfQAAAABJRU5ErkJggg=="></div><div style="vertical-align: middle; max-width: 514px; display: flex; justify-content: space-between;"><div style="float: left;"><div title="#f7b846ff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #f7b846ff;"></div> under</div><div style="margin: 0 auto; display: inline-block;">bad <div title="#00000000" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #00000000;"></div></div><div style="float: right;">over <div title="#7a77abff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #7a77abff;"></div></div>



<div style="vertical-align: middle;"><strong>arcadia:seaweedrose</strong> </div><div class="cmap"><img alt="arcadia:seaweedrose colormap" title="arcadia:seaweedrose" style="border: 1px solid #555;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAgAAAABACAYAAABsv8+/AAAAInRFWHRUaXRsZQBhcmNhZGlhOnNlYXdlZWRyb3NlIGNvbG9ybWFwnAMCpAAAACh0RVh0RGVzY3JpcHRpb24AYXJjYWRpYTpzZWF3ZWVkcm9zZSBjb2xvcm1hcGq0xMQAAAAwdEVYdEF1dGhvcgBNYXRwbG90bGliIHYzLjUuMywgaHR0cHM6Ly9tYXRwbG90bGliLm9yZ2fR6JIAAAAydEVYdFNvZnR3YXJlAE1hdHBsb3RsaWIgdjMuNS4zLCBodHRwczovL21hdHBsb3RsaWIub3JnSXd3tQAAAdJJREFUeJzt1kty4jAUQFFBlpX99Rp6tVEGsQcNgchOUj2450yM4WFLfKru5fXvnznGGJfx4Xr5eHTZjnfn44vX9/Px/PXVue2wft+bdf7+fsbi3Mn7nt7PeD6/zb1cr4vrHofWfXZ/R7+H/fM/+vs7et/z+xkH93Pu/3R4P/vCNnPO/cF2HDfnc9y84fn88tznz8/b+QdzR697N784N8cX93u479W5Y/Pzu9fdn3gb/56fXPfdelbX8Uu/q/nD3//y5/Pgug//X//rd7W5DgAgRwAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACBIAABAkAAAgSAAAQJAAAIAgAQAAQQIAAIIEAAAECQAACHoHDe7Bvb5jk0oAAAAASUVORK5CYII="></div><div style="vertical-align: middle; max-width: 514px; display: flex; justify-content: space-between;"><div style="float: left;"><div title="#3b9886ff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #3b9886ff;"></div> under</div><div style="margin: 0 auto; display: inline-block;">bad <div title="#00000000" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #00000000;"></div></div><div style="float: right;">over <div title="#f898aeff" style="display: inline-block; width: 1em; height: 1em; margin: 0; vertical-align: middle; border: 1px solid #555; background-color: #f898aeff;"></div></div>



    
![png](README_files/README_8_3.png)
    



```python

```
