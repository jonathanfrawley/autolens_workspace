from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the mask of plotted data. 

Although a mask is a 2D array of values, it is actually plotted as a `Grid` of (y,x) coordinates corresponding to the
centre of every pixel at the edge of the mask. The mask is therefore plotted using the `GridScatter` object described 
in `autolens_workspace.plot.mat_wrap.mat_structure`. 

The `MaskScatter` object serves the purpose is allowing us to uniquely customize the appearance of any mask on a plot.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""We will also need a mask to plot on the figure."""
mask = al.Mask2D.circular_annular(
    shape_2d=image.shape_2d, pixel_scales=0.03, inner_radius=0.3, outer_radius=3.0
)

"""To plot the mask on the image, we pass the mask to the `Array` plot method."""

aplt.Array(array=image, mask=mask)

"""
The appearance of the mask is customized using a `Scatter` object.

To plot the mask this object wraps the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

mask_scatter = aplt.MaskScatter(marker="o", colors="r", s=50)

plotter = aplt.Plotter(mask_scatter=mask_scatter)

aplt.Array(array=image, mask=mask, plotter=plotter)

"""
Objects such as a `MaskedImaging` or `FitImaging` objects include the mask as an internal property.

The mask can be customized as shown above using the `MaskScatter`, but we must also tell the plotter to include the 
mask.
"""

include = aplt.Include(mask=True)
