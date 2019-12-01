import autofit as af
import autolens as al

# In this pipeline, we'll perform a subhalo analysis which determines the sensitivity map of a strong lens and
# then attempts to detection subhalos by putting subhalos at fixed intevals on a 2D (y,x) grid. The source uses a
# light profile. The pipeline is as follows:

# Phase 1:

# Description: Perform the subhalo detection analysis.
# Lens Mass: EllipitcalIsothermal + ExternalShear
# Source Light: EllipticalSersic
# Subhalo: SphericalTruncatedNFWChallenge
# Previous Pipelines: initialize/lens_sie__source_sersic_from_init.py
# Prior Passing: Lens mass (constant -> previous pipeline), source light (variable -> previous pipeline).
# Notes: Priors on subhalo are tuned to give realistic masses (10^6 - 10^10) and concentrations (6-24)

# Phase 2:

# Description: Refine the best-fit detected subhalo from the previous phase, by varying also the lens mass model..
# Lens Mass: EllipitcalIsothermal + ExternalShear
# Source Light: EllipticalSersic
# Subhalo: SphericalTruncatedNFWChallenge
# Previous Pipelines: initialize/lens_sie__source_sersic_from_init.py
# Prior Passing: Lens mass (variable -> previous pipeline), source light and subhalo mass (variable -> phase 2).
# Notes: None


def make_pipeline(
    pipeline_settings,
    phase_folders=None,
    redshift_lens=0.5,
    redshift_source=1.0,
    sub_size=2,
    signal_to_noise_limit=None,
    bin_up_factor=None,
    positions_threshold=None,
    inner_mask_radii=None,
    pixel_scale_interpolation_grid=None,
    parallel=False,
):

    ### SETUP PIPELINE AND PHASE NAMES, TAGS AND PATHS ###

    # We setup the pipeline name using the tagging module. In this case, the pipeline name is not given a tag and
    # will be the string specified below However, its good practise to use the 'tag.' function below, incase
    # a pipeline does use customized tag names.

    pipeline_name = "pipeline_subhalo_hyper__lens_sie__subhalo_nfw__source_sersic_mass"

    pipeline_tag = al.pipeline_tagging.pipeline_tag_from_pipeline_settings(
        hyper_galaxies=pipeline_settings.hyper_galaxies,
        hyper_image_sky=pipeline_settings.hyper_image_sky,
        hyper_background_noise=pipeline_settings.hyper_background_noise,
        include_shear=pipeline_settings.include_shear,
    )

    phase_folders.append(pipeline_name)
    phase_folders.append(pipeline_tag)

    ### Phase 1 ###

    # In phase 1, we attempt to detect subhalos, by performing a NxN grid search of MultiNest searches, where:

    # 1) The lens model and source-pixelization parameters are held fixed to the best-fit values from phase 1 of the
    #    initialization pipeline.
    # 2) Each grid search varies the subhalo (y,x) coordinates and mass as free parameters.
    # 3) The priors on these (y,x) coordinates are UniformPriors, with limits corresponding to the grid-cells.

    class GridPhase(af.as_grid_search(al.PhaseImaging, parallel=parallel)):
        @property
        def grid_priors(self):
            return [
                self.model.galaxies.subhalo.mass.centre_0,
                self.model.galaxies.subhalo.mass.centre_1,
            ]

    subhalo = al.GalaxyModel(
        redshift=redshift_lens, mass=al.mp.SphericalTruncatedNFWMassToConcentration
    )

    subhalo.mass.mass_at_200 = af.LogUniformPrior(
        lower_limit=10.0e6, upper_limit=10.0e9
    )

    subhalo.mass.centre_0 = af.UniformPrior(lower_limit=-2.0, upper_limit=2.0)

    subhalo.mass.centre_1 = af.UniformPrior(lower_limit=-2.0, upper_limit=2.0)

    phase1 = GridPhase(
        phase_name="phase_1__subhalo_search",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=al.GalaxyModel(
                redshift=redshift_lens,
                mass=af.last.instance.galaxies.lens.mass,
                shear=af.last.instance.galaxies.lens.shear,
            ),
            subhalo=subhalo,
            source=al.GalaxyModel(
                redshift=redshift_source,
                light=af.last.instance.galaxies.source.light,
                hyper_galaxy=af.last.hyper_combined.instance.galaxies.source.hyper_galaxy,
            ),
        ),
        hyper_image_sky=af.last.hyper_combined.instance.hyper_image_sky,
        hyper_background_noise=af.last.hyper_combined.instance.hyper_background_noise,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        positions_threshold=positions_threshold,
        inner_mask_radii=inner_mask_radii,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        optimizer_class=af.MultiNest,
        number_of_steps=5,
    )

    phase1.optimizer.const_efficiency_mode = False
    phase1.optimizer.n_live_points = 75
    phase1.optimizer.sampling_efficiency = 0.5

    phase2 = al.PhaseImaging(
        phase_name="phase_2__subhalo_refine",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=al.GalaxyModel(
                redshift=redshift_lens,
                mass=af.last[-1].model.galaxies.lens.mass,
                shear=af.last[-1].model.galaxies.lens.shear,
            ),
            subhalo=al.GalaxyModel(
                redshift=redshift_lens,
                mass=phase1.best_result.model.galaxies.subhalo.mass,
            ),
            source=al.GalaxyModel(
                redshift=redshift_source,
                light=phase1.result.model.galaxies.source.light,
                hyper_galaxy=af.last.hyper_combined.instance.galaxies.source.hyper_galaxy,
            ),
        ),
        hyper_image_sky=af.last.hyper_combined.instance.hyper_image_sky,
        hyper_background_noise=af.last.hyper_combined.instance.hyper_background_noise,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        positions_threshold=positions_threshold,
        inner_mask_radii=inner_mask_radii,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        optimizer_class=af.MultiNest,
    )

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.n_live_points = 80
    phase2.optimizer.sampling_efficiency = 0.3

    phase2 = phase2.extend_with_multiple_hyper_phases(
        hyper_galaxy=pipeline_settings.hyper_galaxies,
        include_background_sky=pipeline_settings.hyper_image_sky,
        include_background_noise=pipeline_settings.hyper_background_noise,
    )

    return al.PipelineDataset(pipeline_name, phase1, phase2, hyper_mode=True)
