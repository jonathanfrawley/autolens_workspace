from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the Matplotlib legend of a PyAutoLens figures and subplot.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can customize the legend using the `Legend` `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.legend.html
"""

legend = aplt.Legend(include=True, loc="upper left", fontsize=10, ncol=2)

plotter = aplt.Plotter(legend=legend)

aplt.Array(array=image, plotter=plotter)
