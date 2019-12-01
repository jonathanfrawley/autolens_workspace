import autofit as af
import autolens as al

# In this pipeline, we'll perform an inversion analysis which fits an image with a source galaxy and a lens light
# component.
#
# This first reconstructs the source using a magnification based pxielized inversion, initialized using the
# light-profile source fit of a previous pipeline. This ensures that the hyper_galaxies-image used by the pipeline_settings.pixelization and
# pipeline_settings.regularization is fitted using a pixelized source-plane, which ensures that irstructure in the lensed
# source is adapted too.

# The pipeline is as follows:

# Phase 1:

# Description: initialize the inversion's pixelization and regularization, using a magnification based pixel-grid and
#              the previous lens mass model.
# Lens Light: EllipticalSersic + EllipticalExponential
# Lens Mass: EllipitcalIsothermal + ExternalShear
# Source Light: VoronoiBrightnessImage + Constant
# Previous Pipelines: initialize/lens_sie__source_sersic_from_init.py
# Prior Passing: Lens Mass (variable -> previous pipeline).
# Notes: Uses the lens subtracted image corresponding to the light model of a previous pipeline.

# Phase 2:

# Description: Refine the lens light and mass model using the source inversion.
# Lens Light: EllipticalSersic + EllipticalExponential
# Lens Mass: EllipitcalIsothermal + ExternalShear
# Source Light: VoronoiBrightnessImage + Constant
# Previous Pipelines: initialize/lens_sie__source_sersic_from_init.py
# Prior Passing: Lens light and mass (variable -> previous pipeline), source inversion (variable -> phase 1).
# Notes: None

# Phase 3:

# Description: initialize the inversion's pixelization and regularization, using the input hyper_galaxies-pixelization,
#              hyper_galaxies-regularization and the previous lens mass model.
# Lens Light: EllipticalSersic + EllipticalExponential
# Lens Mass: EllipitcalIsothermal + ExternalShear
# Source Light: VoronoiBrightnessImage + Constant
# Previous Pipelines: None
# Prior Passing: Lens light and mass (constant -> phase 2), source inversion (variable -> phase 1 & 2).
# Notes: Source inversion resolution varies.

# Phase 4:

# Description: Refine the lens mass model using the hyper_galaxies-inversion.
# Lens Light: EllipticalSersic + EllipticalExponential
# Lens Mass: EllipitcalIsothermal + ExternalShear
# Source Light: pipeline_settings.pixelization + pipeline_settings.regularization
# Previous Pipelines: initialize/lens_sie__source_sersic_from_init.py
# Prior Passing: Lens Mass (variable -> previous pipeline), source inversion (variable -> phase 1).
# Notes: Source inversion is fixed.


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
    inversion_uses_border=True,
    inversion_pixel_limit=None,
):

    ### SETUP PIPELINE AND PHASE NAMES, TAGS AND PATHS ###

    # We setup the pipeline name using the tagging module. In this case, the pipeline name is tagged according to
    # whether the lens light model is fixed throughout the pipeline and if certain components of the lens light's
    # bulge-disk model are aligned.

    pipeline_name = "pipeline_inv_hyper__lens_bulge_disk_sie__source_inversion"

    pipeline_tag = al.pipeline_tagging.pipeline_tag_from_pipeline_settings(
        hyper_galaxies=pipeline_settings.hyper_galaxies,
        hyper_image_sky=pipeline_settings.hyper_image_sky,
        hyper_background_noise=pipeline_settings.hyper_background_noise,
        include_shear=pipeline_settings.include_shear,
        fix_lens_light=pipeline_settings.fix_lens_light,
        pixelization=pipeline_settings.pixelization,
        regularization=pipeline_settings.regularization,
        align_bulge_disk_centre=pipeline_settings.align_bulge_disk_centre,
        align_bulge_disk_axis_ratio=pipeline_settings.align_bulge_disk_axis_ratio,
        disk_as_sersic=pipeline_settings.disk_as_sersic,
        align_bulge_disk_phi=pipeline_settings.align_bulge_disk_phi,
    )

    phase_folders.append(pipeline_name)
    phase_folders.append(pipeline_tag)

    ### PHASE 1 ###

    # In phase 1, we initialize the inversion's resolution and regularization coefficient, where we:

    # 1) Use a lens-subtracted image generated by subtracting model lens galaxy image from phase 3 of the initialize
    #    pipeline.
    # 2) Fix our mass model to the lens galaxy mass-model from phase 3 of the initialize pipeline.
    # 3) Use a circular mask which includes all of the source-galaxy light.

    # We begin with a Voronoi Magnification + Constant inversion because if our source is too complex to have its
    # morphology well fitted by the initialize pipeline's Sersic profile, the model image will be inadequate to use as
    # a hyper_galaxies-image.

    phase1 = al.PhaseImaging(
        phase_name="phase_1__source_inversion_magnification_initialization",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=al.GalaxyModel(
                redshift=redshift_lens,
                bulge=af.last.instance.galaxies.lens.bulge,
                disk=af.last.instance.galaxies.lens.disk,
                mass=af.last.instance.galaxies.lens.mass,
                shear=af.last.instance.galaxies.lens.shear,
                hyper_galaxy=af.last.hyper_combined.instance.galaxies.lens.hyper_galaxy,
            ),
            source=al.GalaxyModel(
                redshift=redshift_source,
                pixelization=al.pix.VoronoiMagnification,
                regularization=al.reg.Constant,
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
        inversion_uses_border=inversion_uses_border,
        inversion_pixel_limit=inversion_pixel_limit,
        optimizer_class=af.MultiNest,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 20
    phase1.optimizer.sampling_efficiency = 0.8

    phase1 = phase1.extend_with_multiple_hyper_phases(
        hyper_galaxy=pipeline_settings.hyper_galaxies,
        include_background_sky=pipeline_settings.hyper_image_sky,
        include_background_noise=pipeline_settings.hyper_background_noise,
        inversion=False,
    )

    ### PHASE 2 ###

    # In phase 2, we fit the len galaxy light, mass and source galaxy simultaneously, using an inversion. We will:

    # 1) Initialize the priors of the lens galaxy and source galaxy from phase 3 of the previous pipeline and phase 1
    #    of this pipeline.
    # 2) Use a circular mask including both the lens and source galaxy light.

    lens = al.GalaxyModel(
        redshift=redshift_lens,
        bulge=af.last[-1].model.galaxies.lens.bulge,
        disk=af.last[-1].model.galaxies.lens.disk,
        mass=af.last[-1].model.galaxies.lens.mass,
        shear=af.last[-1].model.galaxies.lens.shear,
        hyper_galaxy=phase1.result.hyper_combined.instance.galaxies.lens.hyper_galaxy,
    )

    # If the lens light is fixed, over-write the pass prior above to fix the lens light model.

    if pipeline_settings.fix_lens_light:

        lens.bulge = af.last.instance.galaxies.lens.bulge
        lens.disk = af.last.instance.galaxies.lens.disk

    phase2 = al.PhaseImaging(
        phase_name="phase_2__lens_bulge_disk_sie__source_inversion_magnification",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=lens,
            source=al.GalaxyModel(
                redshift=redshift_source,
                pixelization=phase1.result.instance.galaxies.source.pixelization,
                regularization=phase1.result.instance.galaxies.source.regularization,
            ),
        ),
        hyper_image_sky=phase1.result.hyper_combined.instance.hyper_image_sky,
        hyper_background_noise=phase1.result.hyper_combined.instance.hyper_background_noise,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        positions_threshold=positions_threshold,
        inner_mask_radii=inner_mask_radii,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        inversion_uses_border=inversion_uses_border,
        inversion_pixel_limit=inversion_pixel_limit,
        optimizer_class=af.MultiNest,
    )

    phase2.optimizer.const_efficiency_mode = True
    phase2.optimizer.n_live_points = 75
    phase2.optimizer.sampling_efficiency = 0.2

    phase2 = phase2.extend_with_multiple_hyper_phases(
        hyper_galaxy=pipeline_settings.hyper_galaxies,
        include_background_sky=pipeline_settings.hyper_image_sky,
        include_background_noise=pipeline_settings.hyper_background_noise,
        inversion=False,
    )

    ### PHASE 3 ###

    # In phase 3, we initialize the inversion's resolution and regularization coefficient, where we:

    # 1) Use a lens-subtracted image generated by subtracting model lens galaxy image from phase 3 of the initialize
    #    pipeline.
    # 2) Fix our mass model to the lens galaxy mass-model from phase 3 of the initialize pipeline.
    # 3) Use a circular mask which includes all of the source-galaxy light.

    phase3 = al.PhaseImaging(
        phase_name="phase_3__source_inversion_initialization",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=al.GalaxyModel(
                redshift=redshift_lens,
                bulge=phase2.result.instance.galaxies.lens.bulge,
                disk=phase2.result.instance.galaxies.lens.disk,
                mass=phase2.result.instance.galaxies.lens.mass,
                shear=phase2.result.instance.galaxies.lens.shear,
                hyper_galaxy=phase2.result.hyper_combined.instance.galaxies.lens.hyper_galaxy,
            ),
            source=al.GalaxyModel(
                redshift=redshift_source,
                pixelization=pipeline_settings.pixelization,
                regularization=pipeline_settings.regularization,
                hyper_galaxy=phase2.result.hyper_combined.instance.galaxies.source.hyper_galaxy,
            ),
        ),
        hyper_image_sky=phase2.result.hyper_combined.instance.hyper_image_sky,
        hyper_background_noise=phase2.result.hyper_combined.instance.hyper_background_noise,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        positions_threshold=positions_threshold,
        inner_mask_radii=inner_mask_radii,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        inversion_uses_border=inversion_uses_border,
        inversion_pixel_limit=inversion_pixel_limit,
        optimizer_class=af.MultiNest,
    )

    phase3.optimizer.const_efficiency_mode = True
    phase3.optimizer.n_live_points = 20
    phase3.optimizer.sampling_efficiency = 0.8

    phase3 = phase3.extend_with_multiple_hyper_phases(
        hyper_galaxy=pipeline_settings.hyper_galaxies,
        include_background_sky=pipeline_settings.hyper_image_sky,
        include_background_noise=pipeline_settings.hyper_background_noise,
        inversion=False,
    )

    ### PHASE 4 ###

    # In phase 4, we fit the len galaxy light, mass and source galaxy simultaneously, using an inversion. We will:

    # 1) Initialize the priors of the lens galaxy and source galaxy from phase 3 of the previous pipeline and phase 1
    #    of this pipeline.
    # 2) Use a circular mask including both the lens and source galaxy light.

    lens = al.GalaxyModel(
        redshift=redshift_lens,
        bulge=phase2.result.model.galaxies.lens.bulge,
        disk=phase2.result.model.galaxies.lens.disk,
        mass=phase2.result.model.galaxies.lens.mass,
        shear=phase2.result.model.galaxies.lens.shear,
        hyper_galaxy=phase3.result.hyper_combined.instance.galaxies.lens.hyper_galaxy,
    )

    # If the lens light is fixed, over-write the pass prior above to fix the lens light model.

    if pipeline_settings.fix_lens_light:

        lens.bulge = phase2.result.instance.galaxies.lens.bulge
        lens.disk = phase2.result.last.instance.galaxies.lens.disk

    phase4 = al.PhaseImaging(
        phase_name="phase_4__lens_bulge_disk_sie__source_inversion",
        phase_folders=phase_folders,
        galaxies=dict(
            lens=lens,
            source=al.GalaxyModel(
                redshift=redshift_source,
                pixelization=phase3.result.instance.galaxies.source.pixelization,
                regularization=phase3.result.instance.galaxies.source.regularization,
                hyper_galaxy=phase3.result.hyper_combined.instance.galaxies.source.hyper_galaxy,
            ),
        ),
        hyper_image_sky=phase3.result.hyper_combined.instance.hyper_image_sky,
        hyper_background_noise=phase3.result.hyper_combined.instance.hyper_background_noise,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        positions_threshold=positions_threshold,
        inner_mask_radii=inner_mask_radii,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        inversion_uses_border=inversion_uses_border,
        inversion_pixel_limit=inversion_pixel_limit,
        optimizer_class=af.MultiNest,
    )

    phase4.optimizer.const_efficiency_mode = True
    phase4.optimizer.n_live_points = 75
    phase4.optimizer.sampling_efficiency = 0.2

    phase4 = phase4.extend_with_multiple_hyper_phases(
        hyper_galaxy=pipeline_settings.hyper_galaxies,
        include_background_sky=pipeline_settings.hyper_image_sky,
        include_background_noise=pipeline_settings.hyper_background_noise,
        inversion=True,
    )

    return al.PipelineDataset(
        pipeline_name, phase1, phase2, phase3, phase4, hyper_mode=True
    )
