import os

# This pipeline runner demonstrates how to load a custom mask for a lens from the hard-disk, and use this as the
# default mask in a pipeline. To be clear, the mask used in a pipeline is decided as follows:

# - If a phase is NOT supplied with a mask_function, the custom input mask is used.
# - If a phase IS supplied with a mask_function, the mask described by the mask_function is used instead.
# - Regardless of the mask used above, use of the inner_circular_mask_radii function will add that circular mask
#   to the mask.

# Most of this runner repeats the command described in the 'runner.'py' file. Therefore, to make it clear where the
# specific mask functionality is used, I have deleted all comments not related to that feature.

### AUTOFIT + CONFIG SETUP ###

import autofit as af

workspace_path = "{}/../../".format(os.path.dirname(os.path.realpath(__file__)))

config_path = workspace_path + "config"

af.conf.instance = af.conf.Config(
    config_path=workspace_path + "config", output_path=workspace_path + "output"
)

dataset_label = "imaging"
dataset_name = "lens_sersic_sie__source_sersic"
pixel_scales = 0.1

### AUTOLENS + DATA SETUP ###

import autolens as al

dataset_path = af.path_util.make_and_return_path_from_path_and_folder_names(
    path=workspace_path, folder_names=["dataset", dataset_label, dataset_name]
)

imaging = al.imaging.from_fits(
    image_path=dataset_path + "image.fits",
    psf_path=dataset_path + "psf.fits",
    noise_map_path=dataset_path + "noise_map.fits",
    pixel_scales=pixel_scales,
)

# Okay, we need to load the mask from a .fits file, in the same fashion as the imaging above. To draw a mask for an
# image, checkout the files
# 'autolens_workspace/tools/data_making/mask_maker.py and autolens_workspace/tools/data_making/mask_maker__irregular.py'

# The example autolens_workspace dataset_label comes with a mask already, if you look in
# autolens_workspace/dataset/imaging/lens_sie__source_sersic/ you'll see a mask.fits file!
mask = al.mask.from_fits(
    file_path=dataset_path + "mask.fits", hdu=0, pixel_scales=pixel_scales
)

# When we plotters the imaging dataset_label, we can:
# - Pass the mask to show it on the image.
# - Extract only the regions of the image in the mask, to remove contaminating bright sources away from the lens.
# - zoom in around the mask to emphasize the lens.
al.plot.imaging.subplot(imaging=imaging, mask=mask)

# Finally, we import and make the pipeline as described in the runner.py file, but pass the mask into the
# 'pipeline.run() function.

from pipelines.simple import lens_sersic_sie__source_sersic

pipeline = lens_sersic_sie__source_sersic.make_pipeline(
    phase_folders=[dataset_label, dataset_name]
)

pipeline.run(dataset=imaging, mask=mask)
