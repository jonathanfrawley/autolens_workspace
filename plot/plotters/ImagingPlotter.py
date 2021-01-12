from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot an `Imaging` dataset using an `ImagingPlotter`.

First, lets load example imaging of of a strong lens as an `Imaging` object.
"""
dataset_name = "mass_sie__source_sersic"
dataset_path = path.join("dataset", "imaging", "no_lens_light", dataset_name)

imaging = al.Imaging.from_fits(
    image_path=path.join(dataset_path, "image.fits"),
    psf_path=path.join(dataset_path, "psf.fits"),
    noise_map_path=path.join(dataset_path, "noise_map.fits"),
    pixel_scales=0.1,
)

"""We now pass the imaging to an `ImagingPlotter` and call various `figure_*` methods to plot different attributes."""
imaging_plotter = aplt.ImagingPlotter(imaging=imaging)
imaging_plotter.figure_image()
imaging_plotter.figure_noise_map()
imaging_plotter.figure_psf()
imaging_plotter.figure_inverse_noise_map()
imaging_plotter.figure_potential_chi_squared_map()
imaging_plotter.figure_absolute_signal_to_noise_map()

"""The `ImagingPlotter` may also plot a subplot of all of these attributes."""
imaging_plotter.subplot_imaging()

"""`
Imaging` contains the following attributes which can be plotted automatically via the `Include2D` object.

(By default, an `Array` does not contain a `Mask2D`, we therefore manually created an `Array` with a mask to illustrate
the plotted of a mask and its border below).
"""

mask = al.Mask2D.circular_annular(
    shape_2d=imaging.shape_2d,
    pixel_scales=imaging.pixel_scales,
    sub_size=1,
    inner_radius=0.3,
    outer_radius=3.0,
)
masked_imaging = al.MaskedImaging(
    imaging=imaging, mask=mask, settings=al.SettingsMaskedImaging(sub_size=2)
)

include_2d = aplt.Include2D(origin=True, mask=True, border=True)
imaging_plotter = aplt.ImagingPlotter(imaging=masked_imaging, include_2d=include_2d)
imaging_plotter.subplot_imaging()