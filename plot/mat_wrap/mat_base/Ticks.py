from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the Ticks of a figure or subplot displayed in PyAutoLens, by 
wrapping the inputs of the Matplotlib methods `plt.tick_params`, `plt.yticks` and `plt.xticks`.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can customize the ticks using the `YTicks` and `XTicks `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.tick_params.html
 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.yticks.html
 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.xticks.html
"""

tickparams = aplt.TickParams(
    axis="y",
    which="major",
    direction="out",
    color="b",
    labelsize=20,
    labelcolor="r",
    length=2,
    pad=5,
    width=3,
    grid_alpha=0.8,
)

yticks = aplt.YTicks(alpha=0.8, fontsize=10, length=0.1, rotation="vertical")

xticks = aplt.XTicks(alpha=0.5, fontsize=5, length=0.2, rotation="horizontal")

plotter = aplt.Plotter(tickparams=tickparams, yticks=yticks, xticks=xticks)

aplt.Array(array=image, plotter=plotter)
