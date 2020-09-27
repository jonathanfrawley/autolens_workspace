# %%

"""
__Example: Non-linear Searches__

In the `beginner` examples all model-fits were performed using the nested sampling algorithm `Dynesty`, which is a
very effective non-linear search algorithm for lens modeling, but may not always be the optimal choice for your
problem. In this example we fit strong lens data using a variety of non-linear searches.
"""

# %%
"""
In this example script, we fit `Imaging` of a strong lens system where:

 - The lens `Galaxy`'s `LightProfile` is omitted (and is not present in the simulated data).
 - The lens `Galaxy`'s `MassProfile` is modeled as an `EllipticalIsothermal`.
 - The source `Galaxy`'s `LightProfile` is modeled as an `EllipticalSersic`.

"""

# %%
"""Use the WORKSPACE environment variable to determine the path to the `autolens_workspace`."""

# %%
import os

workspace_path = os.environ["WORKSPACE"]
print("Workspace Path: ", workspace_path)

# %%
"""Set up the config and output paths."""

# %%
from autoconf import conf

conf.instance = conf.Config(
    config_path=f"{workspace_path}/config", output_path=f"{workspace_path}/output"
)

# %%
"""
As per usual, load the `Imaging` data, create the `Mask2D` and plot them. In this strong lensing dataset:

 - The lens `Galaxy`'s `LightProfile` is omitted_.
 - The lens `Galaxy`'s `MassProfile` is an `EllipticalIsothermal`.
 - The source `Galaxy`'s `LightProfile` is an `EllipticalExponential`.

"""

# %%
import autofit as af
import autolens as al
import autolens.plot as aplt

dataset_type = "imaging"
dataset_label = "no_lens_light"
dataset_name = "mass_sie__source_sersic"
dataset_path = f"{workspace_path}/dataset/{dataset_type}/{dataset_label}/{dataset_name}"

imaging = al.Imaging.from_fits(
    image_path=f"{dataset_path}/image.fits",
    noise_map_path=f"{dataset_path}/noise_map.fits",
    psf_path=f"{dataset_path}/psf.fits",
    pixel_scales=0.1,
)

mask = al.Mask2D.circular(
    shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
)

aplt.Imaging.subplot_imaging(imaging=imaging, mask=mask)

# %%
"""
__Model__

We compose our lens model using `GalaxyModel` objects, which represent the galaxies we fit to our data. In this 
example our lens mooel is:

 - An `EllipticalIsothermal` `MassProfile`.for the lens `Galaxy`'s mass (5 parameters).
 - An `EllipticalSersic` `LightProfile`.for the source `Galaxy`'s light (6 parameters).

The number of free parameters and therefore the dimensionality of non-linear parameter space is N=11.
"""

# %%
lens = al.GalaxyModel(redshift=0.5, mass=al.mp.EllipticalIsothermal)
source = al.GalaxyModel(redshift=1.0, sersic=al.lp.EllipticalSersic)

# %%
"""
__Settings__

Next, we specify the `SettingsPhaseImaging`, which in this example simmply use the default values used in the beginner
examples.
"""

# %%
settings_masked_imaging = al.SettingsMaskedImaging()

settings = al.SettingsPhaseImaging(settings_masked_imaging=settings_masked_imaging)

# %%
"""
__Searches__

Below we use the following non-linear searches:

    1) Nested Sampler.
    2) Optimize.
    3) MCMC
"""

# %%
"""
__Nested Sampling__

To begin, lets again use the nested sampling method `Dynesty` that we have used in all examples up to now. We've seen 
that the method is very effective, always locating a solution that fits the lens data well.
"""

# %%
search = af.DynestyStatic(n_live_points=50)

# %%
"""
__Phase__

We can now combine the model, settings and non-linear search above to create and run a phase, fitting our data with
the lens model.

The `phase_name` and `path_prefix` below specify the path of the results in the output folder:  

 `/autolens_workspace/output/examples/customize/mass_sie__source_sersic/phase__nested_sampling/
    settings__grid_sub_2/dynesty__`.
"""

# %%
phase = al.PhaseImaging(
    path_prefix=f"examples/customimze/{dataset_name}",
    phase_name="phase__non_linear_searches",
    galaxies=dict(lens=lens, source=source),
    settings=settings,
    search=search,
)

result = phase.run(dataset=imaging, mask=mask)

# %%
"""
__Optimizer__

Now, lets use a fast `NonLinearSearch` technique called an `optimizer`, which only seeks to maximize the log 
likelihood of the fit and does not attempt to infer the errors on the model parameters. Optimizers are useful when we
want to find a lens model that fits the data well, but do not care about the full posterior of parameter space (e.g.
the errors). 

we'll use the `particle swarm optimizer algorithm *PySwarms* (https://pyswarms.readthedocs.io/en/latest/index.html) 
using:

 - 30 particles to sample parameter space.
 - 100 iterations per particle, giving a total of 3000 iterations.
    
Performing the model-fit in 3000 iterations is significantly faster than the `Dynesty` fits perforomed in other 
example scripts, that often require > 20000 - 50000 iterations.
"""

# %%
search = af.PySwarmsLocal(n_particles=50, iters=5000)

# %%
"""
__Phase__

We can now combine the model, settings and non-linear search above to create and run a phase, fitting our data with
the lens model.

The `phase_name` and `path_prefix` below specify the path of the results in the output folder:  

 `/autolens_workspace/output/examples/customize`.
"""

# %%
phase = al.PhaseImaging(
    path_prefix=f"examples/customimze/{dataset_name}",
    phase_name="phase__non_linear_searches",
    galaxies=dict(lens=lens, source=source),
    settings=settings,
    search=search,
)

result = phase.run(dataset=imaging, mask=mask)

# %%
"""
__MCMC__
"""

# %%
search = af.Emcee(nwalkers=50, nsteps=1000)

# %%
"""
__Phase__

We can now combine the model, settings and non-linear search above to create and run a phase, fitting our data with
the lens model.

The `phase_name` and `path_prefix` below specify the path of the results in the output folder:  

 `/autolens_workspace/output/examples/customize`.
"""

# %%
phase = al.PhaseImaging(
    path_prefix=f"examples/customimze/{dataset_name}",
    phase_name="phase__non_linear_searches",
    galaxies=dict(lens=lens, source=source),
    settings=settings,
    search=search,
)

result = phase.run(dataset=imaging, mask=mask)
