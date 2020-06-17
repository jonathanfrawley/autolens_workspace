# %%
"""
In this tutorial, we'll go back to our complex source pipeline, but this time, as you've probably guessed, fit it
using an inversion. As we discussed in tutorial 6, we'll begin by modeling the source with a _LightProfile_,
to initialize the mass model, and then switch to an inversion.
"""

# %%
import os
import autofit as af

# %%
"""
Setup the path to the autolens_workspace, using a relative directory name.
"""

# %%
workspace_path = "/path/to/user/autolens_workspace"
workspace_path = "/home/jammy/PycharmProjects/PyAuto/autolens_workspace"

# %%
"""
Use this path to explicitly set the config path and output path.
"""

# %%
conf.instance = conf.Config(
    config_path=f"{workspace_path}/config", output_path=f"{workspace_path}/output"
)

# %%
#%matplotlib inline

import autolens as al
import autolens.plot as aplt

# %%
"""
This function simulates the complex source, and is the same function we used in chapter 3, tutorial 3.
"""

# %%
def simulate():

    grid = al.Grid.uniform(shape_2d=(180, 180), pixel_scales=0.05, sub_size=1)

    psf = al.Kernel.from_gaussian(shape_2d=(11, 11), sigma=0.05, pixel_scales=0.05)

    lens_galaxy = al.Galaxy(
        redshift=0.5,
        mass=al.mp.EllipticalIsothermal(
            centre=(0.0, 0.0), elliptical_comps=(0.1, 0.0), einstein_radius=1.6
        ),
    )

    source_galaxy_0 = al.Galaxy(
        redshift=1.0,
        light=al.lp.EllipticalSersic(
            centre=(0.1, 0.1),
            elliptical_comps=(0.1, 0.0),
            intensity=0.2,
            effective_radius=1.0,
            sersic_index=1.5,
        ),
    )

    source_galaxy_1 = al.Galaxy(
        redshift=1.0,
        light=al.lp.EllipticalSersic(
            centre=(-0.25, 0.25),
            elliptical_comps=(0.0, 0.15),
            intensity=0.1,
            effective_radius=0.2,
            sersic_index=3.0,
        ),
    )

    source_galaxy_2 = al.Galaxy(
        redshift=1.0,
        light=al.lp.EllipticalSersic(
            centre=(0.45, -0.35),
            elliptical_comps=(0.0, 0.222222),
            intensity=0.03,
            effective_radius=0.3,
            sersic_index=3.5,
        ),
    )

    source_galaxy_3 = al.Galaxy(
        redshift=1.0,
        light=al.lp.EllipticalSersic(
            centre=(-0.05, -0.0),
            elliptical_comps=(0.05, 0.1),
            intensity=0.03,
            effective_radius=0.1,
            sersic_index=4.0,
        ),
    )

    tracer = al.Tracer.from_galaxies(
        galaxies=[
            lens_galaxy,
            source_galaxy_0,
            source_galaxy_1,
            source_galaxy_2,
            source_galaxy_3,
        ]
    )

    simulator = al.SimulatorImaging(
        exposure_time_map=al.Array.full(fill_value=300.0, shape_2d=grid.shape_2d),
        psf=psf,
        background_sky_map=al.Array.full(fill_value=0.1, shape_2d=grid.shape_2d),
        add_noise=True,
    )

    return simulator.from_tracer_and_grid(tracer=tracer, grid=grid)


# %%
"""
Lets simulate the we'll fit, which is the same complex source as the
'chapter_3_pipelines/tutorial_3_complex_source.py' tutorial.
"""

# %%
imaging = simulate()
aplt.Imaging.subplot_imaging(imaging=imaging)

# %%
"""
Lets also use the same mask as before.
"""
mask = al.Mask.circular(
    shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
)

# %%
"""
Lets import the pipeline and run it.
"""

# %%
from howtolens.chapter_4_inversions import tutorial_8_pipeline

pipeline_inversion = tutorial_8_pipeline.make_pipeline(
    phase_folders=["howtolens", "c4_t8_inversion"]
)
pipeline_inversion.run(dataset=imaging, mask=mask)

# %%
"""
And with that, we now have a pipeline to model strong lenses using an inversion! Checkout the example pipeline in
'autolens_workspace/pipelines/examples/inversion_hyper_galaxies_bg_noise.py' for an example of an inversion pipeline that includes the lens light
component.
"""
