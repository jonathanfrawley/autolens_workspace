from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the critical curves plotted over data. 

To plot a critical curve, we need a `Tracer` object which performs the strong lensing calculation to
produce a critical curve. Lets make a simple `Tracer`.
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

"""The image of the `Tracer` with critical curves included is plotted as follows:"""

aplt.Tracer.image(
    tracer=tracer, grid=grid, include=aplt.Include(critical_curves=True, caustics=False)
)

"""
The appearance of the critical curves is customized using a `CriticalCurvesPlot` object.

To plot the critical curves this object wraps the following matplotlib method:

 https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.pyplot.plot.html
"""

critical_curves_plot = aplt.CriticalCurvesPlot(linestyle="--", linewidth=10, colors="r")

plotter = aplt.Plotter(critical_curves_plot=critical_curves_plot)

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(critical_curves=True, caustics=False),
    plotter=plotter,
)

"""
By specifying two colors to the `CriticalCurvesPlot` object the radial and tangential critical curves
will be plotted in different colors.

By default, PyAutoLens uses the same alternating colors for the critical curves and caustics, so they 
appear the same color on image-plane and source-plane figures.
"""

critical_curves_plot = aplt.CriticalCurvesPlot(colors=["r", "w"])

plotter = aplt.Plotter(critical_curves_plot=critical_curves_plot)

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(critical_curves=True, caustics=False),
    plotter=plotter,
)
