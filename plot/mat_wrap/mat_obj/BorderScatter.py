from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the border of plotted data. 

A border is the `Grid` of (y,x) coordinates at the centre of every pixel at the border of a mask. A border is defined 
as a pixel that is on an exterior edge of a mask (e.g. it does not include the inner pixels of an annular mask).

The `BorderScatter` object serves the purpose is allowing us to uniquely customize the appearance of any border on 
a plot.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""We will also need a mask whose border we will plot on the figure."""
mask = al.Mask2D.circular_annular(
    shape_2d=image.shape_2d, pixel_scales=0.03, inner_radius=0.3, outer_radius=3.0
)

"""
To plot the border on the image, we pass the mask to the `Array` plot method and specify to include the border.
"""

aplt.Array(array=image, mask=mask, include=aplt.Include(border=True))

"""
The appearance of the border is customized using a `Scatter` object.

To plot the border this object wraps the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

border_scatter = aplt.BorderScatter(marker="o", colors="r", s=50)

plotter = aplt.Plotter(border_scatter=border_scatter)

aplt.Array(array=image, mask=mask, include=aplt.Include(border=True))

"""
Objects such as a `MaskedImaging` or `FitImaging` objects include the border as an internal property.

The border can be customized as shown above using the `BorderScatter`, but we must also tell the plotter to include the 
border.
"""

include = aplt.Include(border=True)
