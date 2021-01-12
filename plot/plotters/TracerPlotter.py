import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `Tracer` using a `TracerPlotter`.

First, lets create a `Tracer`.
"""
lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0), einstein_radius=1.6, elliptical_comps=(0.2, 0.2)
    ),
)

source_galaxy = al.Galaxy(
    redshift=1.0,
    bulge=al.lp.SphericalSersic(
        centre=(0.1, 0.1), intensity=0.3, effective_radius=1.0, sersic_index=2.5
    ),
)

tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

"""We also need an image-plane `Grid` which we'll ray-trace via the `Tracer`."""
grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)

"""
We now pass the tracer` and grid to a `TracerPlotter` and call various `figure_*` methods to plot different attributes.
"""
tracer_plotter = aplt.TracerPlotter(tracer=tracer, grid=grid)
tracer_plotter.figure_image()
tracer_plotter.figure_convergence()
tracer_plotter.figure_potential()
tracer_plotter.figure_deflections_y()
tracer_plotter.figure_deflections_x()
tracer_plotter.figure_magnification()

"""
A `Tracer` and its `Grid` contains the following attributes which can be plotted automatically via 
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
    origin=True,
    mask=True,
    border=True,
    light_profile_centres=True,
    mass_profile_centres=True,
    critical_curves=True,
)
tracer_plotter = aplt.TracerPlotter(
    tracer=tracer, grid=masked_grid, include_2d=include_2d
)
tracer_plotter.figure_image()
tracer_plotter.figure_plane_image_of_plane(plane_index=1)
tracer_plotter.subplot_tracer()

"""
Whereas a `PlanePlotter` had a method to plot its `plane_image`, it did not know the caustics of the source-plane as
they depend on the `MassProfile`'s of `Galaxy`'s in lower redshift planes. When we plot a plane image with a `Tracer`,
this information is now available and thus the caustics of the source-plane are now plotted.

The same is true of the `border, where the `border` plotted on the image-plane image has been ray-traced to the 
source-plane. This is noteworthy as it means in the source-plane we can see where our entire masked region traces too.
"""
tracer_plotter.figure_plane_image_of_plane(plane_index=1)
