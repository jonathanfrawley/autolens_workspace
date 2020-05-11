import os

# This script fits the sample of three strong lenses simulated by the script 'autolens_workspace/aggregator/sample.py'
# using a beginner pipeline to illustrate aggregator functionality.

# We will fit each lens with an SIE mass profile and each source using a pixelized inversion. The fit will use a
# beginner pipelines which performs a 3 phase analysis, which will allow us to illustrate how the results of different
# phases can be loaded using the aggregator.

# This script follows the scripts described in 'autolens_workspace/runners/beginner/' and the pipelines:

# 'autolens_workspace/pipelines/beginner/no_lens_light/lens_sie__source_inversion.py'

# If anything doesn't make sense check those scripts out for details!

### AUTOFIT + CONFIG SETUP ###

import autofit as af

# Setup the path to the autolens_workspace, using a relative directory name.
workspace_path = "{}/../..".format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path and output path.
af.conf.instance = af.conf.Config(
    config_path=f"{workspace_path}/config", output_path=f"{workspace_path}/output"
)

### AUTOLENS + DATA SETUP ###

import autolens as al

# Specify the dataset label and name, which we use to determine the path we load the data from.

pixel_scales = 0.1

for dataset_name in [
    "lens_sie__source_sersic__0",
    "lens_sie__source_sersic__1",
    "lens_sie__source_sersic__2",
]:

    # Create the path where the dataset will be loaded from, which in this case is
    # '/autolens_workspace/aggregator/dataset/imaging/lens_sie__source_sersic/'
    dataset_path = af.path_util.make_and_return_path_from_path_and_folder_names(
        path=workspace_path, folder_names=["aggregator", "dataset", dataset_name]
    )

    ### Info ###

    # The dataset name and info are accessible to the aggregator, to aid interpretation of results. The name is passed
    # as a string and info as a dictionary.

    name = dataset_name

    info = {
        "redshift_lens": 0.5,
        "redshift_source": 1.0,
        "velocity_dispersion": 250000,
        "stellar mass": 1e11,
    }

    ### DATASET ###

    # Using the dataset path, load the data (image, noise map, PSF) as an imaging object from .fits files.
    imaging = al.Imaging.from_fits(
        image_path=f"{dataset_path}/image.fits",
        psf_path=f"{dataset_path}/psf.fits",
        noise_map_path=f"{dataset_path}/noise_map.fits",
        pixel_scales=pixel_scales,
        positions_path=f"{dataset_path}/positions.dat",
        name=name,
    )

    # Next, we create the mask we'll fit this data-set with.
    mask = al.Mask.circular(
        shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, radius=3.0
    )

    ### PIPELINE SETUP ###

    # Advanced pipelines use the same 'Source', 'Light' and 'Mass' setup objects we used in beginner and intermediate
    # pipelines. However, there are many additional options now available with these setup objects, that did not work
    # for beginner and intermediate pipelines. For an explanation, checkout:

    # - 'autolens_workspace/runners/advanced/doc_setup'

    # The setup of earlier pipelines inform the model fitted in later pipelines. For example:

    # - The pixelization and regularization scheme used in the source (inversion) pipeline will be used in the light and
    #   mass pipelines.

    general_setup = al.setup.General(
        hyper_galaxies=False, hyper_image_sky=False, hyper_background_noise=False
    )

    source_setup = al.setup.Source(no_shear=True)

    mass_setup = al.setup.Mass(no_shear=True)

    setup = al.setup.Setup(general=general_setup, source=source_setup, mass=mass_setup)

    # We import and make pipelines as per usual, albeit we'll now be doing this for multiple pipelines!

    ### SOURCE ###

    from pipelines.advanced.no_lens_light.source.parametric import (
        lens_sie__source_sersic,
    )

    pipeline_source__parametric = lens_sie__source_sersic.make_pipeline(
        setup=setup,
        phase_folders=["aggregator", "grid_search", dataset_name],
        positions_threshold=1.0,
    )

    ### MASS ###

    from pipelines.advanced.no_lens_light.mass.sie import lens_sie__source

    pipeline_mass__sie = lens_sie__source.make_pipeline(
        setup=setup,
        phase_folders=["aggregator", "grid_search", dataset_name],
        positions_threshold=1.0,
    )

    ### SUBHALO ###

    from pipelines.advanced.no_lens_light.subhalo import lens_mass__subhalo_nfw__source

    pipeline_subhalo__nfw = lens_mass__subhalo_nfw__source.make_pipeline(
        setup=setup,
        phase_folders=["aggregator", "grid_search", dataset_name],
        positions_threshold=1.0,
        number_of_steps=2,
        parallel=False,
    )

    ### PIPELINE COMPOSITION AND RUN ###

    # We finally add the pipelines above together, which means that they will run back-to-back, as usual passing
    # information throughout the analysis to later phases.

    pipeline = pipeline_source__parametric + pipeline_mass__sie + pipeline_subhalo__nfw

    pipeline.run(dataset=imaging, mask=mask)
