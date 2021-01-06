from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot a `Inversion` using a `InversionPlotter`.

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

"""We now mask the `Imaging` data so we can fit it with an `Inversion`."""
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

"""
The `Inversion` maps pixels from the image-plane of our `Imaging` data to its source plane, via a lens model.

Lets create a `Tracer` which we will use to create the `Inversion`.
"""
lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0), elliptical_comps=(0.111111, 0.0), einstein_radius=1.6
    ),
)
source_galaxy = al.Galaxy(
    redshift=1.0,
    pixelization=al.pix.VoronoiMagnification(shape=(25, 25)),
    regularization=al.reg.Constant(coefficient=1.0),
)

tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

"""We can extract the `Inversion` from the `Tracer` by passing it the masked data."""
inversion = tracer.inversion_imaging_from_grid_and_data(
    grid=masked_imaging.grid,
    image=masked_imaging.image,
    noise_map=masked_imaging.noise_map,
    convolver=masked_imaging.convolver,
)

"""We now pass the inversion to a `InversionPlotter` and call various `figure_*` methods to plot different attributes."""
inversion_plotter = aplt.InversionPlotter(inversion=inversion)
inversion_plotter.figure_reconstructed_image()
inversion_plotter.figure_reconstruction()
inversion_plotter.figure_errors()
inversion_plotter.figure_residual_map()
inversion_plotter.figure_normalized_residual_map()
inversion_plotter.figure_chi_squared_map()
inversion_plotter.figure_regularization_weights()
inversion_plotter.figure_interpolated_reconstruction()
inversion_plotter.figure_interpolated_errors()

"""The `Inversion` attributes can also be plotted as a subplot."""
inversion_plotter = aplt.InversionPlotter(inversion=inversion)
inversion_plotter.subplot_inversion()

"""`Inversion`'s have their own unique attributes that can be plotted via the `Include2D` class:"""
include_2d = aplt.Include2D(
    origin=True,
    mask=True,
    border=True,
    mapper_data_pixelization_grid=True,
    mapper_source_pixelization_grid=True,
    mapper_source_full_grid=True,
)

inversion_plotter = aplt.InversionPlotter(inversion=inversion, include_2d=include_2d)
inversion_plotter.figure_reconstructed_image()
inversion_plotter.figure_reconstruction()
