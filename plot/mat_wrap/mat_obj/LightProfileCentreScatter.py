from os import path
import autolens as al
import autolens.plot as aplt

"""
In this example, we illustrate how to customize the light profile centres plotted over data.

This means the centre of every `LightProfile` of every `Galaxy` in a plot are plotted on the figure. 
A `Tracer` object is a good example of an object with many `LightProfiles`, so lets make one with three.

We will show the plots in the image-plane, however it is the centre's of the source galaxy `LightProfile`'s in the 
source-plane that are plotted.
"""

lens_galaxy = al.Galaxy(
    redshift=0.5,
    bulge=al.lp.EllipticalSersic(
        centre=(0.0, 0.0),
        elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.9, phi=45.0),
        intensity=1.0,
        effective_radius=0.6,
        sersic_index=3.0,
    ),
    mass=al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0), einstein_radius=1.6, elliptical_comps=(0.2, 0.2)
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

"""The image of the `Tracer` with light profile centres included is plotted as follows:"""

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(light_profile_centres=True, mass_profile_centres=False),
)

"""
The appearance of the light profile centres are customized using a `LightProfileCentresScatter` object.

To plot the light profile centres this object wraps the following matplotlib method:

 https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html
"""

light_profile_centres_scatter = aplt.LightProfileCentresScatter(
    marker="o", colors="r", s=150
)

plotter = aplt.Plotter(light_profile_centres_scatter=light_profile_centres_scatter)

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(light_profile_centres=True, mass_profile_centres=False),
    plotter=plotter,
)

"""
By specifying two colors to the `LightProfileCentresScatter` object the light profile centres of each plane
are plotted in different colors.
"""

light_profile_centres_scatter = aplt.LightProfileCentresScatter(
    colors=["r", "w"], s=150
)

plotter = aplt.Plotter(light_profile_centres_scatter=light_profile_centres_scatter)

aplt.Tracer.image(
    tracer=tracer,
    grid=grid,
    include=aplt.Include(light_profile_centres=True, mass_profile_centres=False),
    plotter=plotter,
)
