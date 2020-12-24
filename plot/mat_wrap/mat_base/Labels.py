from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the Labels of a figure or subplot displayed in PyAutoLens.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can customize the ticks using the `YTicks` and `XTicks `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.title.html
 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.ylabel.html
 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.xlabel.html
"""

"""We can manually specify the label of the title, ylabel and xlabel."""

title = aplt.Title(label="This is the title", color="r", fontsize=20)

ylabel = aplt.YLabel(
    manual_label="Label of Y", color="b", fontsize=5, position=(0.2, 0.5)
)

xlabel = aplt.XLabel(manual_label="Label of X", color="g", fontsize=10)

plotter = aplt.Plotter(title=title, ylabel=ylabel, xlabel=xlabel)

aplt.Array(array=image, plotter=plotter)

"""
If we do not manually specify a label, the name of the function used to plot the image will be used as the title 
and the units of the image will be used for the ylabel and xlabel.
"""

title = aplt.Title()
ylabel = aplt.YLabel()
xlabel = aplt.XLabel()

plotter = aplt.Plotter(title=title, ylabel=ylabel, xlabel=xlabel)

aplt.Array(array=image, plotter=plotter)

"""
The units can be manually specified.
"""

plotter = aplt.Plotter(units=aplt.Units(in_kpc=True, conversion_factor=5.0))

aplt.Array(array=image, plotter=plotter)
