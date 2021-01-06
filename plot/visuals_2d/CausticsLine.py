import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to customize the caustics plotted over data. 

To plot a caustic, we need a `Tracer` object which performs the strong lensing calculation to produce a caustic. 
Lets make a simple `Tracer`.
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

"""We also need the `Grid` that we can use to make plots of the `Tracer`'s properties."""
grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)


"""The `Tracer` includes its caustics as an internal property, meaning we can plot them via an `Include2D` object."""
include_2d = aplt.Include2D(critical_curves=False, caustics=True)
tracer_plotter = aplt.TracerPlotter(tracer=tracer, grid=grid, include_2d=include_2d)
tracer_plotter.figure_image()


"""
The appearance of the caustics is customized using a `CausticsPlot` object.

To plot the caustics this object wraps the following matplotlib method:

 https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.plot.html
"""

caustics_plot = aplt.CausticsPlot(linestyle="--", linewidth=10, colors="r")

mat_plot_2d = aplt.MatPlot2D(caustics_plot=caustics_plot)

tracer_plotter = aplt.TracerPlotter(
    tracer=tracer, grid=grid, include_2d=include_2d, mat_plot_2d=mat_plot_2d
)
tracer_plotter.figure_image()

"""
By specifying two colors to the `CausticsPlot` object the radial and tangential caustics
will be plotted in different colors.

By default, PyAutoLens uses the same alternating colors for the caustics and caustics, so they 
appear the same color on image-plane and source-plane figures.
"""

caustics_plot = aplt.CausticsPlot(colors=["r", "w"])

mat_plot_2d = aplt.MatPlot2D(caustics_plot=caustics_plot)

tracer_plotter = aplt.TracerPlotter(
    tracer=tracer, grid=grid, include_2d=include_2d, mat_plot_2d=mat_plot_2d
)
tracer_plotter.figure_image()


"""
To plot caustics manually, we can pass them into a` Visuals2D` object. This is useful for plotting caustics on
figures where they are not an internal property, like an `Array`.
"""

visuals_2d = aplt.Visuals2D(caustics=tracer.caustics)
image = tracer.image_from_grid(grid=grid)

array_plotter = aplt.ArrayPlotter(
    array=image, mat_plot_2d=mat_plot_2d, visuals_2d=visuals_2d
)
array_plotter.figure_array()
