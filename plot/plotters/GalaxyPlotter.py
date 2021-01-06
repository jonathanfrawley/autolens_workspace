from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `Galaxy` using a `GalaxyPlotter`.

First, lets create a `Galaxy` with multiple `LightProfile`'s and a `MassProfile`.
"""

bulge = al.lp.EllipticalSersic(
    centre=(0.0, -0.05),
    elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.9, phi=45.0),
    intensity=4.0,
    effective_radius=0.6,
    sersic_index=3.0,
)

disk = al.lp.EllipticalExponential(
    centre=(0.0, 0.05),
    elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.7, phi=30.0),
    intensity=2.0,
    effective_radius=1.6,
)

mass = al.mp.EllipticalIsothermal(
    centre=(0.0, 0.0),
    einstein_radius=0.8,
    elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.7, phi=45.0),
)

galaxy = al.Galaxy(redshift=0.5, bulge=bulge, disk=disk, mass=mass)

"""We also need the 2D grid the `Galaxy`'s `Profile`'s are evaluated on."""
grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)

"""
We now pass the galaxy and grid to a `GalaxyPlotter` and call various `figure_*` methods to 
plot different attributes.
"""

galaxy_plotter = aplt.GalaxyPlotter(galaxy=galaxy, grid=grid)
galaxy_plotter.figure_image()
galaxy_plotter.figure_convergence()
# galaxy_plotter.figure_potential()
galaxy_plotter.figure_deflections_y()
galaxy_plotter.figure_deflections_x()
galaxy_plotter.figure_magnification()

"""
The `GalaxyPlotter` also has subplot method that plot each individual `Profile` in 2D as well as a 1D plot showing all
`Profiles` together.
"""

galaxy_plotter.subplot_image()
galaxy_plotter.subplot_convergence()
# galaxy_plotter.subplot_potential()
galaxy_plotter.subplot_deflections_y()
galaxy_plotter.subplot_deflections_x()

"""
A `Galaxy` and its `Grid` contains the following attributes which can be plotted automatically via 
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
galaxy_plotter = aplt.GalaxyPlotter(
    galaxy=galaxy, grid=masked_grid, include_2d=include_2d
)
galaxy_plotter.figure_image()
