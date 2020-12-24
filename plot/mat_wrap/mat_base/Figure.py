from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the Matplotlib figure window that displays PyAutoLens figures and 
subplots.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We can customize the figure using the `Figure` `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.figure.html
"""

figure = aplt.Figure(
    figsize=(7, 7),
    dpi=100.0,
    facecolor="white",
    edgecolor="black",
    frameon=True,
    clear=False,
    tight_layout=False,
    constrained_layout=False,
)

plotter = aplt.Plotter(figure=figure)

aplt.Array(array=image, plotter=plotter)

"""
We can also customize the aspect ratio of the image displayed in a figure by passing the `Figure` an aspect ratio. 

This customizes the aspect ratio when the method `plt.imshow` is called.

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.imshow.html
"""

figure = aplt.Figure(aspect="square")

plotter = aplt.Plotter(figure=figure)

aplt.Array(array=image, plotter=plotter)
