from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a 2D `Grid` of (y,x) coordinates over PyAutoLens figures and subplots.

First, lets load an example Hubble Space Telescope image of a real strong lens as an `Array`.
"""
dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""We next need the 2D `Grid` we overlay. We'll create a uniform grid at a coarser resolution than our dataset."""
grid = al.Grid.uniform(shape_2d=(30, 30), pixel_scales=0.1)

"""We input this `Grid` into the `Visuals2D` object, which plots it over the figure."""
visuals_2d = aplt.Visuals2D(grid=grid)

"""We now plot the image with the grid overlaid."""
array_plotter = aplt.ArrayPlotter(array=image, visuals_2d=visuals_2d)
array_plotter.figure_array()

"""
We customize the grid's appearance using the `GridScatter` `matplotlib wrapper object which wraps the following method(s): 

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

grid_scatter = aplt.GridScatter(c="r", marker=".", s=1)

mat_plot_2d = aplt.MatPlot2D(grid_scatter=grid_scatter)

array_plotter = aplt.ArrayPlotter(
    array=image, mat_plot_2d=mat_plot_2d, visuals_2d=visuals_2d
)
array_plotter.figure_array()
