from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to customize the Colorbar in PyAutoLens figures and subplots.

First, lets load an example Hubble Space Telescope image of a real strong lens as an `Array`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can customize the colorbar using the `Colorbar` matplotlib wrapper object which wraps the following method(s):

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.colorbar.html
"""

cb = aplt.Colorbar(
    fraction=0.047,
    shrink=5.0,
    aspect=1.0,
    pad=0.01,
    anchor=(0.0, 0.5),
    panchor=(1.0, 0.0),
)

mat_plot_2d = aplt.MatPlot2D(colorbar=cb)

array_plotter = aplt.ArrayPlotter(array=image, mat_plot_2d=mat_plot_2d)
array_plotter.figure_array()

"""
The labels and ticks of the `Colorbar` can also be customized. 

This uses the `cb.ax.set_yticklabels` to manually override the tick locations and labels:
 
 https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.axes.Axes.set_yticklabels.html
 
If also uses `cb.ax.tick_params` to customize the axes of the color bar:

 https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.tick_params.html
 
The input parameters of both the above methods can be passed into the `Colorbar` object.
"""

cb = aplt.Colorbar(
    manual_tick_labels=[1.0, 2.0],
    manual_tick_values=[0.0, 0.25],
    axis="both",
    reset=False,
    which="major",
    direction="in",
    length=2,
    width=2,
    color="r",
    pad=0.1,
    labelsize=10,
    labelcolor="r",
)


mat_plot_2d = aplt.MatPlot2D(colorbar=cb)

array_plotter = aplt.ArrayPlotter(array=image, mat_plot_2d=mat_plot_2d)
array_plotter.figure_array()
