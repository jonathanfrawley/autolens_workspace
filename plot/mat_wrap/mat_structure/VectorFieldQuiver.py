from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to plot and customize vector fields in PyAutoLens figures and subplots.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""We need a `VectorField` to plot over the image. We make a simple example of a vector field below."""

vector_field = al.VectorFieldIrregular(
    vectors=[(1.0, 2.0), (2.0, 1.0)], grid=[(-1.0, 0.0), (-2.0, 0.0)]
)

"""
We can customize the appearance of the vectors using the `VectorFieldQuiver `mat_obj` in PyAutoLens. 

This wraps the following matplotlib methods:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.quiver.html
"""

quiver = aplt.VectorFieldQuiver(
    headlength=1,
    pivot="tail",
    color="w",
    linewidth=10,
    units="width",
    angles="uv",
    scale=None,
    width=0.5,
    headwidth=3,
    alpha=0.5,
)

plotter = aplt.Plotter(vector_field_quiver=quiver)

aplt.Array(array=image, plotter=plotter, vector_field=vector_field)
