from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to plot and customize (y,x) grids of coordinates in PyAutoLens figures and subplots.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
The appearance of a (y,x) `Grid` of coordinates is customized using `Scatter` objects. To illustrate this, we will 
customize the appearance of the (y,x) origin on a figure using an `OriginScatter` object.

To plot a (y,x) grids of coordinates (like an origin) these objects wrap the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

origin_scatter = aplt.OriginScatter(marker="o", s=50)

plotter = aplt.Plotter(origin_scatter=origin_scatter)

aplt.Array(
    array=image,
    include=aplt.Include(
        origin=True
    ),  # The `Include` object is described in `plot/include`.
    plotter=plotter,
)

"""
There are numerous (y,x) grids of coordinates that PyAutoLens plots. For example, in addition to the origin,
there are grids like the multiple images of a strong lens, a source-plane grid of traced coordinates, etc.

All of these grids are plotted using a `Scatter` object and they are described in more detail in the 
`plot/include` example scripts. 
"""
