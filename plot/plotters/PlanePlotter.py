import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `Plane` using a `PlanePlotter`.

First, lets create a image-plane `Grid` and ray-trace it via `MassProfile` to create a source-plane `Grid`.
"""
grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)

mass_profile = al.mp.EllipticalIsothermal(
    centre=(0.0, 0.0), elliptical_comps=(0.1, 0.2), einstein_radius=1.0
)
deflections = mass_profile.deflections_from_grid(grid=grid)
lens_galaxy = al.Galaxy(redshift=0.5, mass=mass_profile)

lensed_grid = grid.grid_from_deflection_grid(deflection_grid=deflections)

"""We create a `Plane` representing a source-plane containing a `Galaxy` with a `LightProfile`."""

bulge = al.lp.EllipticalSersic(
    centre=(0.1, 0.1),
    elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.8, phi=60.0),
    intensity=0.3,
    effective_radius=1.0,
    sersic_index=2.5,
)

source_galaxy = al.Galaxy(redshift=1.0, bulge=bulge)

image_plane = al.Plane(galaxies=[lens_galaxy])
source_plane = al.Plane(galaxies=[source_galaxy])

"""
We can plot the `image_plane` by passing it and our `grid to a` PlanePlotter` and calling various `figure_*` methods.

In this example script our `lens_galaxy` only had a `MassProfile` so only methods like `figure_convergence` are
available.
"""
plane_plotter = aplt.PlanePlotter(plane=image_plane, grid=grid)
plane_plotter.figure_convergence()

"""
We can also plot the `source_plane` by passing it with the `lensed_grid` to a `PlanePlotter`.

In this case, our `source_galaxy` only had a ` LightProfile` so only a plot of its image is available.
"""
plane_plotter = aplt.PlanePlotter(plane=source_plane, grid=lensed_grid)
plane_plotter.figure_image()

"""
In addition to the lensed image of the source-plane, we can plot its unlensed image (e.g. how the source-galaxy 
appears in the source-plane before lensing) using the `figure_plane_image` method.
"""
plane_plotter.figure_plane_image()

"""
It is feasible for us to plot the caustics in the source-plane. However, to calculate the `Caustics` we must manually
compute them from the image-plane `MassProfile` and pass them to the source-plane mat_plot_2d. 
"""
visuals_2d = aplt.Visuals2D(caustics=image_plane.caustics)
plane_plotter = aplt.PlanePlotter(
    plane=source_plane, grid=lensed_grid, visuals_2d=visuals_2d
)
plane_plotter.figure_plane_image()

"""
For `PlanePlotter`'s, `GalaxyPlotter`'s and `LightProfilePlotter's that are plotting source-plane images, the only
way to plot the caustics is to manually extract them from the foreground `MassProfile`'s, as shown above. This is 
because these source-plane objects have no knowledge of what objects are in the image-plane.

`TracerPlotter`'s automatically extract and plot caustics on source-plane figures, given they have available the 
necessary information on the image-plane mass. This is shown in `autolens_workspace/plot/plotters/TracerPlotter.py`.
"""

"""
A `Plane` and its `Grid` contains the following attributes which can be plotted automatically via 
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

"""
Note that the image-plane has no `LightProfile`'s and does not plot any light-profile centres. Similarly, the 
source-plane has no `MassProfile`'s and plot no mass-profile centres.
"""
plane_plotter = aplt.PlanePlotter(
    plane=image_plane, grid=masked_grid, include_2d=include_2d
)
plane_plotter.figure_image()
plane_plotter = aplt.PlanePlotter(
    plane=source_plane, grid=masked_grid, include_2d=include_2d
)
plane_plotter.figure_image()
