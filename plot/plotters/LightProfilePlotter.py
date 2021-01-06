from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `LightProfile` using a `LightProfilePlotter`.

First, lets create a simple `LightProfile` which we'll plot.
"""

bulge = al.lp.EllipticalSersic(
    centre=(0.0, 0.0),
    elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.9, phi=45.0),
    intensity=1.0,
    effective_radius=0.8,
    sersic_index=4.0,
)

"""We also need the 2D grid the `LightProfile` is evaluated on."""
grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)

"""
We now pass the light profile and grid to a `LightProfilePlotter` and call various `figure_*` methods to 
plot different attributes.
"""

light_profile_plotter = aplt.LightProfilePlotter(light_profile=bulge, grid=grid)
light_profile_plotter.figure_image()

"""
A `LightProfile` and its `Grid` contains the following attributes which can be plotted automatically via 
the `Include2D` object.

(By default, a `Grid` does not contain a `Mask2D`, we therefore manually created a `Grid` with a mask to illustrate
plotting its mask and border below).
"""
mask = al.Mask2D.circular(
    shape_2d=grid.shape_2d,
    pixel_scales=grid.pixel_scales,
    radius=2.0,
    sub_size=grid.sub_size,
)
masked_grid = al.Grid.from_mask(mask=mask)

include_2d = aplt.Include2D(
    origin=True, mask=True, border=True, light_profile_centres=True
)
light_profile_plotter = aplt.LightProfilePlotter(
    light_profile=bulge, grid=masked_grid, include_2d=include_2d
)
light_profile_plotter.figure_image()
