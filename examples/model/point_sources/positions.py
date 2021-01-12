"""
__Example: Modeling__

To fit a lens model to positional constraints of a strong lens, we must perform lens modeling, which uses
a `NonLinearSearch` to fit many different sets of multiple images to the dataset.

Model-fitting is handled by our project **PyAutoFit**, a probabilistic programming language for non-linear model
fitting. The setting up of configuration files is performed by our project **PyAutoConf**. we'll need to import
both to perform the model-fit.
"""

"""
In this example script, we fit the multiple-image `Positions` of a strong lens system where:

 - The lens `Galaxy`'s total mass distribution is modeled as an `EllipticalIsothermal`.
 - The source `Galaxy` is modeled as a `PointSource`.
"""

"""
Load the strong lens dataset `mass_sie__source_point`, which is the dataset we will use to perform lens modeling.

We begin by loading an image of the dataset. Although we are performing point-source modeling and will not use this
data in the model-fit, it is useful to load it for visualization. By passing this dataset to the model-fit at the
end of the script it will be used when visualizing the results. However, the use of an image in this way is entirely
optional, and if it were not included in the model-fit visualization would simple be performed using grids without
the image.
"""

from os import path
import autofit as af
import autolens as al
import autolens.plot as aplt

dataset_name = "mass_sie__source_point"
dataset_path = path.join("dataset", "point_source", dataset_name)

image = al.Array.from_fits(file_path=path.join(dataset_path, "image.fits"), pixel_scales=0.05)

"""
We now load these positions we will fit using point source modeling. We load them as a `GridIrregularGrouped` data 
structure, which groups different sets of positions to a common source. This is used, for example, when there are 
multiple source galaxy's in the source plane. For this simple example, we assume there is just one source and just one 
group.
"""

positions = al.GridIrregularGrouped.from_file(
    file_path=path.join(dataset_path, "positions.dat"),
)

print(positions.in_grouped_list)

"""We can now plot our positions dataset over the observed image."""

visuals_2d = aplt.Visuals2D(positions=positions)

array_plotter = aplt.ArrayPlotter(array=image, visuals_2d=visuals_2d)
array_plotter.figure_array()

"""We can also just plot the positions, omitting the image."""

grid_plotter = aplt.GridPlotter(grid=positions)
grid_plotter.figure_grid()

"""
For point-source modeling, we also need the noise of every measured position. This is simply the pixel-scale of our
observed dataset, which in this case is 0.05".

The `position_noise_map` should have the same structure as the `GridIrregularGrouped`. In this example, the positions
are a single group of 4 (y,x) coordinates, therefore their noise map should be a single group of 4 floats. We can
make this noise-map by creating a `ValuesIrregularGrouped` structure from the `GridIrregularGrouped`.
"""
positions_noise_map = positions.values_from_value(value=image.pixel_scale)

print(positions_noise_map)
stop

"""The model-fit also requires a mask defining the regions of the image we fit the lens model to the data."""

mask = al.Mask2D.circular(
    shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
)

imaging_plotter = aplt.ImagingPlotter(
    imaging=imaging, visuals_2d=aplt.Visuals2D(mask=mask)
)
imaging_plotter.subplot_imaging()

"""
__Phase__

To perform lens modeling, we create a `PhaseImaging` object, which comprises:

   - The `GalaxyModel`'s used to fit the data.
   - The `SettingsPhase` which customize how the model is fitted to the data.
   - The `NonLinearSearch` used to sample parameter space.

Once we have create the phase, we `run` it by passing it the data and mask.
"""

"""
__Model__

We compose our lens model using `GalaxyModel` objects, which represent the galaxies we fit to our data. In this 
example our lens mooel is:

 - An `EllipticalIsothermal` `MassProfile`.for the lens `Galaxy`'s mass (5 parameters).
 - An `EllipticalSersic` `LightProfile`.for the source `Galaxy`'s light (7 parameters).

The number of free parameters and therefore the dimensionality of non-linear parameter space is N=12.

NOTE: By default, **PyAutoLens** assumes the image has been reduced such that the lens galaxy centre is at (0.0", 0.0"),
with the priors on the lens `MassProfile` coordinates set accordingly. if for your dataset the lens is not centred at 
(0.0", 0.0"), we recommend you reduce your data so it is (see `autolens_workspace/preprocess`).  Alternatively, you 
can manually override the priors (see `autolens_workspace/examples/customize/priors.py`).
"""

lens = al.GalaxyModel(redshift=0.5, mass=al.mp.EllipticalIsothermal)
source = al.GalaxyModel(redshift=1.0, bulge=al.lp.EllipticalSersic)

"""
__Settings__

Next, we specify the `SettingsPhaseImaging`, which describe how the model is fitted to the data in the log likelihood
function. Below, we specify:

 - That a regular `Grid` is used to fit create the model-image when fitting the data 
      (see `autolens_workspace/examples/grids.py` for a description of grids).
 - The sub-grid size of this grid.

Different `SettingsPhase` are used in different example model scripts and a full description of all `SettingsPhase` 
can be found in the example script `autolens/workspace/examples/model/customize/settings.py` and the following 
link -> <link>
"""

settings_masked_imaging = al.SettingsMaskedImaging(grid_class=al.Grid, sub_size=2)

settings = al.SettingsPhaseImaging(settings_masked_imaging=settings_masked_imaging)

"""
__Search__

The lens model is fitted to the data using a `NonLinearSearch`, which we specify below. In this example, we use the
nested sampling algorithm Dynesty (https://dynesty.readthedocs.io/en/latest/), with:

 - 50 live points.

The script `autolens_workspace/examples/model/customize/non_linear_searches.py` gives a description of the types of
non-linear searches that can be used with **PyAutoLens**. If you do not know what a `NonLinearSearch` is or how it 
operates, I recommend you complete chapters 1 and 2 of the HowToLens lecture series.

The `name` and `path_prefix` below specify the path where results ae stored in the output folder:  

 `/autolens_workspace/output/examples/beginner/mass_sie__source_sersic/phase_mass[sie]_source[bulge]`.
"""

search = af.DynestyStatic(
    path_prefix=path.join("examples", "beginner", dataset_name),
    name="phase_mass[sie]_source[bulge]",
    n_live_points=50,
)

"""
__Phase__

We can now combine the model, settings and `NonLinearSearch` above to create and run a phase, fitting our data with
the lens model.
"""

phase = al.PhaseImaging(
    search=search,
    galaxies=af.CollectionPriorModel(lens=lens, source=source),
    settings=settings,
)

"""
We can now begin the fit by passing the dataset and mask to the phase, which will use the `NonLinearSearch` to fit
the model to the data. 

The fit outputs visualization on-the-fly, so checkout the path 
`/path/to/autolens_workspace/output/examples/phase_mass[sie]_source[bulge]` to see how your fit is doing!
"""

result = phase.run(dataset=imaging, mask=mask)

"""
The phase above returned a result, which, for example, includes the lens model corresponding to the maximum
log likelihood solution in parameter space.
"""

print(result.max_log_likelihood_instance)

"""
It also contains instances of the maximum log likelihood Tracer and FitImaging, which can be used to visualize
the fit.
"""

tracer_plotter = aplt.TracerPlotter(
    tracer=result.max_log_likelihood_tracer, grid=mask.geometry.masked_grid_sub_1
)
tracer_plotter.subplot_tracer()
fit_imaging_plotter = aplt.FitImagingPlotter(fit=result.max_log_likelihood_fit)
fit_imaging_plotter.subplot_fit_imaging()

"""
Checkout `/path/to/autolens_workspace/examples/model/results.py` for a full description of the result object.
"""
