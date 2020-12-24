from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to plot and customize patches in PyAutoLens figures and subplots.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
To plot a patch on an image, we use the `matplotlib.patches` module. In this example, we will use
the `Ellipse` patch.
"""
from matplotlib.patches import Ellipse

patch_0 = Ellipse(xy=(1.0, 2.0), height=1.0, width=2.0, angle=1.0)
patch_1 = Ellipse(xy=(-2.0, -3.0), height=1.0, width=2.0, angle=1.0)

"""
We can customize the patches using the `Patcher` `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/collections_api.html
"""

patch_overlay = aplt.PatchOverlay(
    facecolor=["r", "g"], edgecolor="none", linewidth=10, offsets=3.0
)

plotter = aplt.Plotter(patch_overlay=patch_overlay)

aplt.Array(array=image, plotter=plotter, patches=[patch_0, patch_1])
