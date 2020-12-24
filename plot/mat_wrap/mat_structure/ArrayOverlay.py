from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to overlay a 2D `Array` over PyAutoLens figures and subplots.

First, lets load an example image of of a strong lens as an `Array` from the directory 
`autolens_workspace/output/dataset/imaging/slacs1430+4105/`.
"""

dataset_path = path.join("dataset", "slacs", "slacs1430+4105")
image_path = path.join(dataset_path, "image.fits")
image = al.Array.from_fits(file_path=image_path, hdu=0, pixel_scales=0.03)

"""
We next need the 2D `Array` we overlay. We'll create a simple 3x3 array.
"""
arr = al.Array.manual_2d(
    array=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], pixel_scales=0.5
)

"""
We can customize the overlaid array using the `ArrayOverlay` `mat_obj` in PyAutoLens. 

To overlay the array this objects wrap the following matplotlib method:

 https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.pyplot.imshow.html
"""

array_overlayer = aplt.ArrayOverlayer(alpha=0.5)

plotter = aplt.Plotter(array_overlayer=array_overlayer)

aplt.Array(array=image, plotter=plotter, array_overlay=arr)
