# %%

"""
__Example: Modeling__

To fit a lens model to a dataset, we must perform lens modeling, which uses a non-linear search algorithm to fit many
different tracers to the dataset.

Model-fitting is handled by our project **PyAutoFit**, a probablistic programming language for non-linear model
fitting. The setting up of configuration files is performed by our project **PyAutoConf**. We'll need to import
both to perform the model-fit.
"""

# %%
"""
In this example script, we fit _Imaging_ of a strong lens system where:

 - The lens galaxy's _LightProfile_ is omitted (and is not present in the simulated data).
 - The lens galaxy's _MassProfile_ is modeled as an _EllipticalIsothermal_.
 - The source galaxy's surface-brightness is modeled using an _Inversion_.

An _Inversion_ reconstructs the source's light using a pixel-grid, which is regularized using a prior that enforces
this reconstructioon to be smooth. This uses _Pixelization_ and _Regularization_ objects and in this example we will
use their simplest forms, a _Rectangular_ _Pixelization_ and _Constant_ _Regularization_ scheme.

Inversions are covered in detail in chapter 4 of the **HowToLens** lectures.
"""

# %%
"""Use the WORKSPACE environment variable to determine the path to the autolens workspace."""

# %%
"""Use the WORKSPACE environment variable to determine the workspace path."""

# %%
import os
workspace_path = os.environ["WORKSPACE"]
print("Workspace Path: ", workspace_path)

# %%
"""
Load the strong lens dataset 'mass_sie__source_sersic' 'from .fits files, which is the dataset we will
use to perform lens modeling.

This is the same dataset we fitted in the 'autolens/intro/fitting.py' example.
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
    psf_path=f"{dataset_path}/psf.fits",
    noise_map_path=f"{dataset_path}/noise_map.fits",
    pixel_scales=0.1,
)

# %%
"""
The model-fit also requires a mask, which defines the regions of the image we use to fit the lens model to the data.
"""

# %%
mask = al.Mask.circular(
    shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
)

aplt.Imaging.subplot_imaging(imaging=imaging, mask=mask)

# %%
"""
__Phase__

To perform lens modeling, we create a *PhaseImaging* object, which comprises:

   - The _GalaxyModel_'s used to fit the data.
   - The *SettingsPhase* which customize how the model is fitted to the data.
   - The *NonLinearSearch* used to sample parameter space.
   
Once we have create the phase, we 'run' it by passing it the data and mask.
"""

# %%
"""
__Model__

We compose our lens model using _GalaxyModel_ objects, which represent the galaxies we fit to our data. In this 
example our lens mooel is:

 - An _EllipticalIsothermal_ _MassProfile_ for the lens galaxy's mass (5 parameters).
 - A _Rectangular_ _Pixelization_ which reconstructs the source galaxy's light. We will fix its resolution to 
   30 x 30 pixels, which balances fast-run time with sufficient resolution to reconstruct its light. (0 parameters).
 - A _Constant_ _Regularization_ scheme which imposes a smooothness prior on the source reconstruction (1 parameter). 

The number of free parameters and therefore the dimensionality of non-linear parameter space is N=1. 
 
It is worth noting the _Pixelization_ and _Regularization_ use significantly fewer parameter (1 parameteer) than 
fitting the source using _LightProfile_'s (7+ parameters). 
"""

# %%
lens = al.GalaxyModel(redshift=0.5, mass=al.mp.EllipticalIsothermal)
source = al.GalaxyModel(
    redshift=1.0,
    pixelization=al.pix.Rectangular(shape=(30, 30)),
    regularization=al.reg.Constant,
)

# %%
"""
__Settings__

Next, we specify the _SettingsPhaseImaging_, which describe how the model is fitted to the data in the log likelihood
function. Below, we specify:
 
 - That a regular *Grid* is used to fit create the model-image when fitting the data 
      (see 'autolens_workspace/examples/grids.py' for a description of grids).
 - The sub-grid size of this grid.

We specifically specify the grid that is used to perform the _Inversion_. In **PyAutoLens** it is possible to fit
data simultaneously with _LightProfile_'s and an _Inversion_. Each fit uses a different grid, which are specified 
independently.

Different *SettingsPhase* are used in different example model scripts and a full description of all *SettingsPhase* 
can be found in the example script 'autolens/workspace/examples/model/customize/settings.py' and the following 
link -> <link>
"""

# %%
settings_masked_imaging = al.SettingsMaskedImaging(
    grid_inversion_class=al.Grid, sub_size=2
)

settings = al.SettingsPhaseImaging(settings_masked_imaging=settings_masked_imaging)

# %%
"""
__Search__

The lens model is fitted to the data using a *NonLinearSearch*, which we specify below. In this example, we use the
nested sampling algorithm Dynesty (https://dynesty.readthedocs.io/en/latest/), with:

 - 50 live points.

The script 'autolens_workspace/examples/model/customize/non_linear_searches.py' gives a description of the types of
non-linear searches that can be used with **PyAutoLens**. If you do not know what a non-linear search is or how it 
operates, I recommend you complete chapters 1 and 2 of the HowToLens lecture series.
"""

# %%
search = af.DynestyStatic(n_live_points=50)

# %%
"""
__Phase__

We can now combine the model, settings and non-linear search above to create and run a phase, fitting our data with
the lens model.

The phase_name and folders inputs below specify the path of the results in the output folder:  

 '/autolens_workspace/output/examples/beginner/mass_sie__source_sersic/phase__mass_sie__source_sersic'.
"""

# %%
phase = al.PhaseImaging(
    phase_name="phase__lens_sie__source_inversion",
    folders=["examples", "beginner", dataset_name],
    galaxies=dict(lens=lens, source=source),
    settings=settings,
    search=search,
)

# %%
"""
We can now begin the fit by passing the dataset and mask to the phase, which will use the non-linear search to fit
the model to the data. 

The fit outputs visualization on-the-fly, so checkout the path 
'/path/to/autolens_workspace/output/examples/phase__mass_sie__source_sersic' to see how your fit is doing!
"""

# %%
result = phase.run(dataset=imaging, mask=mask)

# %%
"""
The phase above returned a result, which, for example, includes the lens model corresponding to the maximum
log likelihood solution in parameter space.
"""

# %%
print(result.max_log_likelihood_instance)

# %%
"""
It also contains instances of the maximum log likelihood Tracer and FitImaging, which can be used to visualize
the fit.
"""

# %%
aplt.Tracer.subplot_tracer(
    tracer=result.max_log_likelihood_tracer, grid=mask.geometry.masked_grid_sub_1
)
aplt.FitImaging.subplot_fit_imaging(fit=result.max_log_likelihood_fit)

# %%
"""
Checkout '/path/to/autolens_workspace/examples/model/results.py' for a full description of the result object.
"""
