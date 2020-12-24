from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to output a PyAutoLens figure or subplot.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can specify the output of the figure using the `Output` `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.show.html
 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.savefig.html

Below, we specify that the figure should be output as a `.png` file, with the name `example.png` in the `plot/plots` 
folder of the workspace.
"""

output = aplt.Output(path=path.join("plot", "plots"), filename="example", format="png")

plotter = aplt.Plotter(output=output)

aplt.Array(array=image, plotter=plotter)

"""
This `Output` object does not display the figure on your computer screen, bypassing this to output the `.png`. This is
the default behaviour of PyAutoLens plots, but can be manually specified using the `format-"show"`
"""

output = aplt.Output(format="show")

plotter = aplt.Plotter(output=output)

aplt.Array(array=image, plotter=plotter)
