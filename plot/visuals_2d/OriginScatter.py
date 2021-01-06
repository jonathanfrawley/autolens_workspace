from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to customize the (y,x) origin of plotted data. 

The origin is plotted using the `GridScatter` object described in `autolens_workspace.plot.mat_wramat_plot.Mat_structure`. 
The `OriginScatter` object serves the purpose is allowing us to unique customize the appearance of an origin on a plot.

First, lets load an example Hubble Space Telescope image of a real strong lens as an `Array`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
The `Array` includes its mask as an internal property, meaning we can plot it via an `Include2D` object.

As can be seen below, the origin of the data is (0.0, 0.0), which is where the black cross marking the origin
appears.
"""
include_2d = aplt.Include2D(origin=True)

array_plotter = aplt.ArrayPlotter(array=image, include_2d=include_2d)
array_plotter.figure_array()

"""
The appearance of the (y,x) origin coordinates is customized using a `Scatter` object.

To plot these (y,x) grids of coordinates these objects wrap the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
 
The example script `plot/mat_wrap/Scatter.py` gives a more detailed description on how to customize its appearance.
"""

origin_scatter = aplt.OriginScatter(marker="o", s=50)

mat_plot_2d = aplt.MatPlot2D(origin_scatter=origin_scatter)

array_plotter = aplt.ArrayPlotter(
    array=image, mat_plot_2d=mat_plot_2d, include_2d=include_2d
)
array_plotter.figure_array()

"""To plot the origin manually, we can pass it into a` Visuals2D` object. """
visuals_2d = aplt.Visuals2D(origin=al.GridIrregular(grid=[(1.0, 1.0)]))

array_plotter = aplt.ArrayPlotter(array=image, visuals_2d=visuals_2d)
array_plotter.figure_array()
