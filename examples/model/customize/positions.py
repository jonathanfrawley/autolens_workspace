# %%

"""
__Example: Modeling Positions__

Before fitting a strong lens, we can manually specify a set of image-pixels corresponding to the multiple images of the
source-galaxy(s). During the analysis, PyAutoLens will first check that these pixels trace within a specified
arc-second threshold of one another (which is controlled by the `position_threshold` parameter input into a phase). If
they do not meet this threshold, the model is discard and a new sample is generated by the non-linear search.

This provides two benefits:

    1) The analysis runs faster as the `NonLinearSearch` avoids searching regions of parameter space where the
       mass-model is clearly not accurate.

    2) By removing these solutions, a global-maximum solution may be reached instead of a local-maxima. This is
       because removing the incorrect mass models makes the non-linear parameter space less complex.
"""

# %%
"""
In this example script, we fit `Imaging` of a strong lens system where:

 - The lens `Galaxy`'s light is omitted (and is not present in the simulated data).
 - The lens total mass distribution is modeled as an `EllipticalIsothermal`.
 - The source `Galaxy`'s light is modeled parametrically as an `EllipticalSersic`.

"""

# %%
"""
The positions are associated with the `Imaging` dataset and they are loaded from a `positions.dat` file which is in the
same folder as the dataset itself. To create this file, we used a GUI to `draw on` the positions with our mouse. This
GUI can be found in the script:

 `autolens_workspace/preprocess/imaging/gui/positions.py`

If you wish to use positions for modeling your own lens data, you should use this script to draw on the positions of
every lens in you dataset.
"""

# %%
import autofit as af
import autolens as al
import autolens.plot as aplt

dataset_type = "imaging"
dataset_label = "no_lens_light"
dataset_name = "mass_sie__source_sersic"
dataset_path = f"dataset/{dataset_type}/{dataset_label}/{dataset_name}"

imaging = al.Imaging.from_fits(
    image_path=f"{dataset_path}/image.fits",
    psf_path=f"{dataset_path}/psf.fits",
    noise_map_path=f"{dataset_path}/noise_map.fits",
    pixel_scales=0.1,
    positions_path=f"{dataset_path}/positions.dat",
)

# %%
"""
The model-fit also requires a mask, which defines the regions of the image we use to fit the lens model to the data.

We can easily check the image-positions are accurate by plotting them using our `Imaging` `Plotter`.(they are the 
black dots on the image).
"""

# %%
mask = al.Mask2D.circular(
    shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
)

aplt.Imaging.subplot_imaging(imaging=imaging, mask=mask, positions=imaging.positions)

# %%
"""
Alternative, the positions can be set up manually in the runner script after loading the data. To do this, we use the 
_GridCoordinates_ object, which is used by PyAutoLens to specify lists of (y,x) coordinates that are not on a uniform
or regular grid (which the (y,x) coordinates of a `Grid` object are).
"""

imaging = al.Imaging.from_fits(
    image_path=f"{dataset_path}/image.fits",
    psf_path=f"{dataset_path}/psf.fits",
    noise_map_path=f"{dataset_path}/noise_map.fits",
    pixel_scales=0.1,
)

imaging.positions = al.GridCoordinates(
    [(1.55, -0.55), (1.15, 1.15), (-0.65, 1.55), (-0.95, -0.95)]
)

aplt.Imaging.subplot_imaging(imaging=imaging, mask=mask, positions=imaging.positions)

# %%
"""
__Model__

We compose our lens model using `GalaxyModel` objects, which represent the galaxies we fit to our data. In this 
example our lens mooel is:

 - An `EllipticalIsothermal` `MassProfile`.for the lens `Galaxy`'s mass (5 parameters).
 - An `EllipticalSersic` `LightProfile`.for the source `Galaxy`'s light (7 parameters).

The number of free parameters and therefore the dimensionality of non-linear parameter space is N=12.
"""

# %%
lens = al.GalaxyModel(redshift=0.5, mass=al.mp.EllipticalIsothermal)
source = al.GalaxyModel(redshift=1.0, bulge=al.lp.EllipticalSersic)

# %%
"""
__Settings__

Next, we specify the `SettingsPhaseImaging`, which describe how the model is fitted to the data in the log likelihood
function. Below, we specify:

 - A positions_threshold of 0.5, meaning that the four (y,x) coordinates specified by our positions must trace
   within 0.5" of one another in the source-plane for a mass model to be accepted. If not, it is discarded and
   a new model is sampled.

The threshold of 0.5" is large. For an accurate lens model we would anticipate the positions trace within < 0.01" of
one another. However, we only want the threshold to aid the `NonLinearSearch` with the generation of the initial 
mass models. 

We do not want to risk inferring an incorrect mass model because our position threshold removed genuinely plausible 
solutions!
"""

# %%
settings_masked_imaging = al.SettingsMaskedImaging(grid_class=al.Grid, sub_size=2)
settings_lens = al.SettingsLens(positions_threshold=0.5)

settings = al.SettingsPhaseImaging(
    settings_masked_imaging=settings_masked_imaging, settings_lens=settings_lens
)

# %%
"""
__Search__

The lens model is fitted to the data using a `NonLinearSearch`, which we specify below. In this example, we use the
nested sampling algorithm Dynesty (https://dynesty.readthedocs.io/en/latest/), with:

 - 50 live points.

The script `autolens_workspace/examples/model/customize/non_linear_searches.py` gives a description of the types of
non-linear searches that can be used with **PyAutoLens**. If you do not know what a `NonLinearSearch` is or how it 
operates, I recommend you complete chapters 1 and 2 of the HowToLens lecture series.

The `name` and `path_prefix` below specify the path where results are stored in the output folder:  

 `/autolens_workspace/output/examples/beginner/mass_sie__source_sersic/phase__positions`.
"""

# %%
search = af.DynestyStatic(
    path_prefix=f"examples/customize/{dataset_name}",
    name="phase_positions",
    n_live_points=50,
)

# %%
"""
__Phase__

We can now combine the model, settings and `NonLinearSearch` above to create and run a phase, fitting our data with
the lens model.
"""

# %%
phase = al.PhaseImaging(
    search=search, galaxies=dict(lens=lens, source=source), settings=settings
)

# %%
"""
We can now begin the fit by passing the dataset and mask to the phase, which will use the `NonLinearSearch` to fit
the model to the data. The dataset contains the positions, which is how they are input in the model-fit.

The fit outputs visualization on-the-fly, so checkout the path 
`/path/to/autolens_workspace/output/examples/phase__mass_sie__source_bulge` to see how your fit is doing!
"""

# %%
result = phase.run(dataset=imaging, mask=mask)

# %%
"""
__Wrap Up__

In this example, we used positional information about the lensed source `Galaxy`'s multiple images to speed up our
model-fit and make it more robust. 

PyAutoLens supports the following more advanced use of positional information:

 - If the unlensed source contains multiple components or clumps of light, one may wish to mark positions that 
      signify they correspond to these different regions of the source-plane. To do this, a list of list of tuples
      can be input into the GridCoordinates object, e.g:
      
      [[(1.0, 1.0), (0.5, 0.5)], [(-1.0, 1.0), (-0.5, 0.5)]]

      Note that in this example we only specified a single list of tuples, indicating all 4 positions were from the
      same region of the source.
      
      Before modeling a lens, it can be extremely difficult to be sure which parts of a lensed source eminate fom the
      same regons of the source-plane, and inputting positions as multiple lists is not advised. We would only advise
      this feature is used if one has spectroscopic information on the lensed source that makes it feasible to robustly
      identify which images correspond to the same regions of the source.
      
 - When using a single phase to fit a lens, we must manually specify or draw the positions on the lensed source and
      pass them to the phase. However, the `autolens_workspace/examples/linking` scripts and PyAutoLens`s _Pipelines_
      feature break the model-fit into multiple _Phase`s_ which each perform a unique non-linear search.  
      
      If an intial phases successfully fits the lens`s mass model, this model can be used to deterine the positions 
      and position threshold of the lensed source galaxy automatically. These can be then automatically set up as the
      positions and threshold used in the later phase`s, not requiring us to manually specifc the positions at all!
      
      To do this, we pass the `SettingsPhaseImaging` the input parameters `auto_positions_factor` and 
   `auto_positions_minumum_threshold`. An example of this can be found in the example script
   `autolens_workspace/examples/model/linking/parametric_to_inversion.py`.
"""
