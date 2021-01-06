from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `Grid` data structure using an `GridPlotter`.

Lets create a simple uniform grid.
"""
grid = al.Grid.uniform(shape_2d=(30, 30), pixel_scales=0.1)

"""We now pass the grid to a `GridPlotter` and call the `figure_grid` method."""
grid_plotter = aplt.GridPlotter(grid=grid)
grid_plotter.figure_grid()

"""We can easily ray-trace grids using a `MassProfile` and plot them with a `GridPlotter`."""
mass_profile = al.mp.EllipticalIsothermal(
    centre=(0.0, 0.0), elliptical_comps=(0.1, 0.2), einstein_radius=1.0
)
deflections = mass_profile.deflections_from_grid(grid=grid)

lensed_grid = grid.grid_from_deflection_grid(deflection_grid=deflections)

grid_plotter = aplt.GridPlotter(grid=lensed_grid)
grid_plotter.figure_grid()

"""A `Grid` contains the following attributes which can be plotted automatically via the `Include2D` object."""
include_2d = aplt.Include2D(origin=True)
grid_plotter = aplt.GridPlotter(grid=lensed_grid, include_2d=include_2d)
grid_plotter.figure_grid()
