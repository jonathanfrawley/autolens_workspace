from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot an `FitImaging` object using an `FitImagingPlotter`.

First, lets load example imaging of of a strong lens as an `Imaging` object.
"""
dataset_name = "light_sersic__mass_sie__source_sersic"
dataset_path = path.join("dataset", "imaging", "with_lens_light", dataset_name)

imaging = al.Imaging.from_fits(
    image_path=path.join(dataset_path, "image.fits"),
    psf_path=path.join(dataset_path, "psf.fits"),
    noise_map_path=path.join(dataset_path, "noise_map.fits"),
    pixel_scales=0.1,
)

"""We now mask the data and fit it with a `Tracer` to create a `FitImaging` object."""
mask = al.Mask2D.circular(
    shape_2d=imaging.shape_2d, pixel_scales=imaging.pixel_scales, sub_size=1, radius=3.0
)

masked_imaging = al.MaskedImaging(imaging=imaging, mask=mask)

lens_galaxy = al.Galaxy(
    redshift=0.5,
    bulge=al.lp.EllipticalSersic(
        centre=(0.0, 0.0),
        elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.9, phi=45.0),
        intensity=1.0,
        effective_radius=0.8,
        sersic_index=4.0,
    ),
    mass=al.mp.EllipticalIsothermal(
        centre=(0.0, 0.0),
        einstein_radius=1.6,
        elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.8, phi=45.0),
    ),
    shear=al.mp.ExternalShear(elliptical_comps=(0.0, 0.05)),
)

source_galaxy = al.Galaxy(
    redshift=1.0,
    bulge=al.lp.EllipticalSersic(
        centre=(0.1, 0.1),
        elliptical_comps=al.convert.elliptical_comps_from(axis_ratio=0.8, phi=60.0),
        intensity=0.3,
        effective_radius=1.0,
        sersic_index=2.5,
    ),
)

tracer = al.Tracer.from_galaxies(galaxies=[lens_galaxy, source_galaxy])

fit = al.FitImaging(masked_imaging=masked_imaging, tracer=tracer)

"""We now pass the FitImaging to an `FitImagingPlotter` and call various `figure_*` methods to plot different attributes."""
fit_imaging_plotter = aplt.FitImagingPlotter(fit=fit)
fit_imaging_plotter.figure_image()
fit_imaging_plotter.figure_noise_map()
fit_imaging_plotter.figure_signal_to_noise_map()
fit_imaging_plotter.figure_model_image()
fit_imaging_plotter.figure_residual_map()
fit_imaging_plotter.figure_normalized_residual_map()
fit_imaging_plotter.figure_chi_squared_map()

"""The `FitImagingPlotter` may also plot a subplot of these attributes."""
fit_imaging_plotter.subplot_fit_imaging()

"""It can plot of the model image of an input plane."""
fit_imaging_plotter.figure_model_image_of_plane(plane_index=0)
fit_imaging_plotter.figure_model_image_of_plane(plane_index=1)

"""It can plot the image of a plane with all other model images subtracted."""
fit_imaging_plotter.figure_subtracted_image_of_plane(plane_index=0)
fit_imaging_plotter.figure_subtracted_image_of_plane(plane_index=1)

"""
It can also plot the plane-image of a plane, that is what the source galaxy looks like without lensing (e.g. 
for `plane_index=1` this is the source-plane image)
"""
fit_imaging_plotter.figure_plane_image_of_plane(plane_index=0)
fit_imaging_plotter.figure_plane_image_of_plane(plane_index=1)

"""A subplot of a plane, showing the above 3 figures, can also be plotted."""
fit_imaging_plotter.subplot_of_plane(plane_index=1)

"""`
`FitImaging` contains the following attributes which can be plotted automatically via the `Include2D` object.
"""

include_2d = aplt.Include2D(
    origin=True,
    mask=True,
    border=True,
    light_profile_centres=True,
    mass_profile_centres=True,
    critical_curves=True,
    caustics=True,
)
fit_plotter = aplt.FitImagingPlotter(fit=fit, include_2d=include_2d)
fit_plotter.subplot_fit_imaging()
fit_plotter.subplot_of_plane(plane_index=0)
fit_plotter.subplot_of_plane(plane_index=1)
