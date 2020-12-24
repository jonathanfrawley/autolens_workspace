from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the multiple images plotted over data.

The multiple images are defined as the unique set of multiple images that are traced from the centre of
every source galaxy in a `Tracer`. These are computed using the `PositionSolver` object.
"""

lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0), einstein_radius=0.8, elliptical_comps=(0.2, 0.2)
    ),
)

source_galaxy = al.Galaxy(
    redshift=1.0,
    bulge_0=al.lp.SphericalSersic(
        centre=(0.1, 0.1), intensity=0.3, effective_radius=1.0, sersic_index=2.5
    ),
    bulge_1=al.lp.SphericalSersic(
        centre=(0.4, 0.3), intensity=0.3, effective_radius=1.0, sersic_index=2.5
    ),
)
tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

"""We also need the `Grid` that we can use to make plots of the `Tracer`'s properties."""

grid = al.Grid.uniform(shape_2d=(100, 100), pixel_scales=0.05)

"""The image of the `Tracer` with multiple images included is plotted as follows:"""

aplt.Tracer.image(tracer=tracer, grid=grid, include=aplt.Include(multiple_images=True))

"""
The appearance of the multiple images are customized using a `MultipleImagesScatter` object.

To plot the multiple images this object wraps the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

multiple_images_scatter = aplt.MultipleImagesScatter(marker="o", colors="r", s=150)

plotter = aplt.Plotter(multiple_images_scatter=multiple_images_scatter)

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(multiple_images=True),
    plotter=plotter,
)

"""
By specifying two colors to the `MultipleImagesScatter` object the multiple images of each `LightProfile`
would be plotted in different colors (note how the `Galaxy` objects we created above had different redshifts and
each therefore had its own `Plane` in the `Tracer`).
"""

multiple_images_scatter = aplt.MultipleImagesScatter(colors=["r", "w"], s=150)

plotter = aplt.Plotter(multiple_images_scatter=multiple_images_scatter)

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(multiple_images=True),
    plotter=plotter,
)
