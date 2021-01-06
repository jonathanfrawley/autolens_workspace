from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to customize the border of plotted data. 

A border is the `Grid` of (y,x) coordinates at the centre of every pixel at the border of a mask. A border is defined 
as a pixel that is on an exterior edge of a mask (e.g. it does not include the inner pixels of an annular mask).

The `BorderScatter` object serves the purpose is allowing us to uniquely customize the appearance of any border on 
a plot.

First, lets load an example Hubble Space Telescope image of a real strong lens as an `Array`.
"""
dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""We will also need a mask whose border we will plot on the figure, which we associate with the image."""
mask = al.Mask2D.circular_annular(
    shape_2d=image.shape_2d,
    pixel_scales=image.pixel_scales,
    inner_radius=0.3,
    outer_radius=3.0,
    sub_size=image.sub_size,
)
masked_image = al.Array.manual_mask(array=image.in_2d, mask=mask)


"""The `Array` includes a its border as an internal property, meaning we can plot it via an `Include2D` object."""
include_2d = aplt.Include2D(border=True)
array_plotter = aplt.ArrayPlotter(array=masked_image, include_2d=include_2d)
array_plotter.figure_array()


"""
The appearance of the border is customized using a `BorderScatter` object.

To plot the border this object wraps the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""
border_scatter = aplt.BorderScatter(marker="o", colors="r", s=50)

mat_plot_2d = aplt.MatPlot2D(border_scatter=border_scatter)

array_plotter = aplt.ArrayPlotter(
    array=masked_image, mat_plot_2d=mat_plot_2d, include_2d=include_2d
)
array_plotter.figure_array()


"""
To plot the border manually, we can pass it into a` Visuals2D` object.

This means we don't need to create the `masked_image` array we used above.
"""
visuals_2d = aplt.Visuals2D(border=mask.geometry.border_grid_1d)

array_plotter = aplt.ArrayPlotter(array=image, visuals_2d=visuals_2d)
array_plotter.figure_array()
