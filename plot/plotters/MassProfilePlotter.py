import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `MassProfile` using a `MassProfilePlotter`.

First, lets create a simple `MassProfile` which we'll plot.
"""

mass = al.mp.EllipticalIsothermal(
    centre=(0.0, 0.0),
    einstein_radius=1.6,
    elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.7, phi=45.0),
)

"""We also need the 2D grid the `MassProfile` is evaluated on."""
grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)

"""
We now pass the mass profile and grid to a `MassProfilePlotter` and call various `figure_*` methods to 
plot different attributes.
"""

mass_profile_plotter = aplt.MassProfilePlotter(mass_profile=mass, grid=grid)
mass_profile_plotter.figure_convergence()
# mass_profile_plotter.figure_potential()
mass_profile_plotter.figure_deflections_y()
mass_profile_plotter.figure_deflections_x()
mass_profile_plotter.figure_magnification()

"""
A `MassProfile` and its `Grid` contains the following attributes which can be plotted automatically via 
the `Include2D` object.

(By default, a `Grid` does not contain a `Mask2D`, we therefore manually created a `Grid` with a mask to illustrate
plotting its mask and border below).
"""
mask = al.Mask2D.circular_annular(
    shape_2d=grid.shape_2d,
    pixel_scales=grid.pixel_scales,
    inner_radius=0.3,
    outer_radius=2.0,
    sub_size=grid.sub_size,
)
masked_grid = al.Grid.from_mask(mask=mask)

include_2d = aplt.Include2D(
    origin=True, mask=True, border=True, mass_profile_centres=True, critical_curves=True
)
mass_profile_plotter = aplt.MassProfilePlotter(
    mass_profile=mass, grid=masked_grid, include_2d=include_2d
)
mass_profile_plotter.figure_convergence()
