from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to plot a 2D `Grid` of (y,x) coordinates over PyAutoLens figures and subplots.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We next need the 2D `Grid` we overlay. We'll create a uniform grid at a coarser resolution than our dataset.
"""
grid = al.Grid.uniform(shape_2d=(30, 30), pixel_scales=0.1)

"""
We can customize the grid's appearance using the `GridScatter` `mat_structure` in PyAutoLens. 

To plot the grid this objects wrap the following matplotlib method:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

grid_scatter = aplt.GridScatter(colors="r", marker=".", s=1)

plotter = aplt.Plotter(grid_scatter=grid_scatter)

aplt.Array(array=image, grid=grid, plotter=plotter)
