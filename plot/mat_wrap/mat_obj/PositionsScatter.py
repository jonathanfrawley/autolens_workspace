from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to plot positions on a figure and customize their appearance. 

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We will also need a positions to plot on the figure, we'll set these up as a `GridIrregular` of 2D (y,x) coordinates.
"""
positions = al.GridIrregular(grid=[[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])

"""To plot the positions on the image, we pass the positions to the `Array` plot method."""

aplt.Array(array=image, positions=positions)

"""
The appearance of the positions is customized using a `Scatter` object.

To plot the positions this object wraps the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

positions_scatter = aplt.PositionsScatter(marker="o", colors="r", s=50)

plotter = aplt.Plotter(positions_scatter=positions_scatter)

aplt.Array(array=image, positions=positions, plotter=plotter)

"""
Objects such as a `FitImaging` object include the positions as an internal property.

The positions can be customized as shown above using the `PositionsScatter`, but we must also tell the plotter to 
include the positions.
"""

include = aplt.Include(positions=True)
