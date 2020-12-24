from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the (y,x) origin of plotted data. 

The origin is plotted using the `GridScatter` object described in `autolens_workspace.plot.mat_wrap.mat_structure`. 
The `OriginScatter` object serves the purpose is allowing us to unique customize the appearance of an origin on a plot.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
To plot the origin on the image, we set `origin=True` in the `aplt.Include` object.

As can be seen below, the origin of the data is (0.0, 0.0), which is where the black cross marking the origin
appears.
"""

aplt.Array(array=image, include=aplt.Include(origin=True))

"""
The appearance of the (y,x) origin coordinates is customized using a `Scatter` object.

To plot these (y,x) grids of coordinates these objects wrap the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
 
The example script `plot/mat_wrap/Scatter.py` gives a more detailed description on how to customize its appearance.
"""

origin_scatter = aplt.OriginScatter(marker="o", s=50)

plotter = aplt.Plotter(origin_scatter=origin_scatter)

aplt.Array(array=image, include=aplt.Include(origin=True), plotter=plotter)
