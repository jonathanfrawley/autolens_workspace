from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot an `Array` data structure using an `ArrayPlotter`.

First, lets load an example image of of a strong lens as an `Array`.
"""
dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""We now pass the array to an `ArrayPlotter` and call the `figure_array` method."""
array_plotter = aplt.ArrayPlotter(array=image)
array_plotter.figure_array()

"""
An `Array` contains the following attributes which can be plotted automatically via the `Include2D` object.

(By default, an `Array` does not contain a `Mask2D`, we therefore manually created an `Array` with a mask to illustrate
plotting its mask and border below).
"""
mask = al.Mask2D.circular_annular(
    shape_2d=image.shape_2d,
    pixel_scales=image.pixel_scales,
    inner_radius=0.3,
    outer_radius=3.0,
    sub_size=image.sub_size,
)
masked_image = al.Array.manual_mask(array=image.in_2d, mask=mask)

include_2d = aplt.Include2D(origin=True, mask=True, border=True)

array_plotter = aplt.ArrayPlotter(array=masked_image, include_2d=include_2d)
array_plotter.figure_array()
