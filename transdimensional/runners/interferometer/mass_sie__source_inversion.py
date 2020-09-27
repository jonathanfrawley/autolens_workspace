# %%
"""
__WELCOME__ 

This transdimensional pipeline runner loads a strong lens dataset and analyses it using a transdimensional lens
modeling pipeline.

Using a pipeline composed of three phases this runner fits `Interferometer` data of a strong lens system, where in
the final phase of the pipeline:

 - The lens `Galaxy`'s light is omitted from the data and model.
 - The lens `Galaxy`'s `MassProfile` is modeled as an _EllipticalIsothermal_.
 - The source galaxy is modeled using an _Inversion_.

This uses the pipeline (Check it out full description of the pipeline):

 `autolens_workspace/pipelines/interferometer/lens_sie__source_inversion.py`.
"""

# %%
"""Use the WORKSPACE environment variable to determine the path to the `autolens_workspace`."""

# %%
import os

workspace_path = os.environ["WORKSPACE"]
print("Workspace Path: ", workspace_path)

# %%
""" AUTOLENS + DATA SETUP """

# %%
import autolens as al
import autolens.plot as aplt
import numpy as np

dataset_type = "interferometer"
dataset_name = "mass_sie__source_sersic"
pixel_scales = 0.1

# %%
"""
Create the path where the dataset will be loaded from, which in this case is
`/autolens_workspace/dataset/interferometer/mass_sie__source_sersic`
"""

# %%
dataset_path = f"{workspace_path}/dataset/{dataset_type}/{dataset_name}"

# %%
"""Using the dataset path, load the data (image, noise-map, PSF) as an `Interferometer` object from .fits files."""

interferometer = al.Interferometer.from_fits(
    visibilities_path=f"{dataset_path}/visibilities.fits",
    noise_map_path=f"{dataset_path}/noise_map.fits",
    uv_wavelengths_path=f"{dataset_path}/uv_wavelengths.fits",
)

aplt.Interferometer.subplot_interferometer(interferometer=interferometer)

# %%
"""
The perform a fit, we need two masks, firstly a ‘real-space mask’ which defines the grid the image of the lensed 
source galaxy is evaluated using.
"""

# %%
real_space_mask = al.Mask2D.circular(shape_2d=(200, 200), pixel_scales=0.05, radius=3.0)

# %%
"""
We also need a ‘visibilities mask’ which defines which visibilities are omitted from the chi-squared evaluation.
"""

# %%
visibilities_mask = np.full(fill_value=False, shape=interferometer.visibilities.shape)

# %%
"""Make a quick subplot to make sure the data looks as we expect."""

# %%
aplt.Interferometer.subplot_interferometer(interferometer=interferometer)

# %%
"""
__Settings__

The `SettingsPhaseInterferometer` describe how the model is fitted to the data in the log likelihood function.

These settings are used and described throughout the `autolens_workspace/examples/model` example scripts, with a 
complete description of all settings given in `autolens_workspace/examples/model/customize/settings.py`.

The settings chosen here are applied to all phases in the pipeline.
"""

# %%
settings_masked_interferometer = al.SettingsMaskedInterferometer(
    grid_class=al.Grid, sub_size=2, transformer_class=al.TransformerNUFFT
)

# %%
"""
_Inversion_`s may infer unphysical solution where the source reconstruction is a demagnified reconstruction of the 
lensed source (see **HowToLens** chapter 4). 

To prevent this, auto-positioning is used, which uses the lens mass model of earlier phases to automatically set 
positions and a threshold that resample inaccurate mass models (see `examples/model/positions.py`).

The *auto_positions_factor* is a factor that the threshold of the inferred positions using the previous mass model are 
multiplied by to set the threshold in the next phase. The *auto_positions_minimum_threshold* is the minimum value this
threshold can go to, even after multiplication.
"""

settings_lens = al.SettingsLens(
    auto_positions_factor=3.0, auto_positions_minimum_threshold=0.8
)

settings = al.SettingsPhaseInterferometer(
    settings_masked_interferometer=settings_masked_interferometer,
    settings_lens=settings_lens,
)

# %%
"""
__Pipeline_Setup__:

Pipelines can contain `Setup` objects, which customize how different aspects of the model are fitted. 

First, we create a a `SetupMassTotal`, which customizes:

 - If there is an `ExternalShear` in the mass model or not.
"""

# %%
setup_mass = al.SetupMassTotal(no_shear=False)

# %%
"""
Next, we create a `SetupSourceInversion` which customizes:

 - The `Pixelization` used by the `Inversion` in phase 3 of the pipeline.
 - The `Regularization` scheme used by the `Inversion` in phase 3 of the pipeline.
"""

# %%
setup_source = al.SetupSourceInversion(
    pixelization=al.pix.VoronoiMagnification, regularization=al.reg.Constant
)

"""
_Pipeline Tagging_

The `Setup` objects are input into a `SetupPipeline` object, which is passed into the pipeline and used to customize
the analysis depending on the setup. This includes tagging the output path of a pipeline. For example, if `no_shear` 
is True, the pipeline`s output paths are `tagged` with the string `no_shear`.

This means you can run the same pipeline on the same data twice (with and without shear) and the results will go
to different output folders and thus not clash with one another!

The `prefix_path` below specifies the path the pipeline results are written to, which is:

 `autolens_workspace/output/pipelines/dataset_type/dataset_name` 
 `autolens_workspace/output/pipelines/interferometer/mass_sie__source_inversion/`
 

The redshift of the lens and source galaxies are also input (see `examples/model/customimze/redshift.py`) for a 
description of what inputting redshifts into **PyAutoLens** does.
"""

# %%
setup = al.SetupPipeline(
    prefix_path=f"transdimensional/{dataset_type}/{dataset_name}",
    redshift_lens=0.5,
    redshift_source=1.0,
    setup_mass=setup_mass,
    setup_source=setup_source,
)

# %%
"""
__Pipeline Creation__

To create a pipeline we import it from the pipelines folder and run its `make_pipeline` function, inputting the 
*Setup* and `SettingsPhase` above.
"""

# %%
from autolens_workspace.transdimensional.pipelines.interferometer import (
    mass_sie__source_inversion,
)

pipeline = mass_sie__source_inversion.make_pipeline(setup=setup, settings=settings)

# %%
"""
__Pipeline Run__

Running a pipeline is the same as running a phase, we simply pass it our lens dataset and mask to its run function.
"""

# %%
pipeline.run(dataset=interferometer)
