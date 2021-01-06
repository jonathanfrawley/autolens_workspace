from os import path
import autolens as al
import autolens.plot as aplt

"""
This example illustrates how to plot an `Interferometer` dataset using an `InterferometerPlotter`.

First, lets load example interferometer of of a strong lens as an `Interferometer` object.
"""
dataset_name = "mass_sie__source_sersic"
dataset_path = path.join("dataset", "interferometer", dataset_name)

interferometer = al.Interferometer.from_fits(
    visibilities_path=path.join(dataset_path, "visibilities.fits"),
    noise_map_path=path.join(dataset_path, "noise_map.fits"),
    uv_wavelengths_path=path.join(dataset_path, "uv_wavelengths.fits"),
)

"""We now pass the interferometer to an `InterferometerPlotter` and call various `figure_*` methods to plot different attributes."""
interferometer_plotter = aplt.InterferometerPlotter(interferometer=interferometer)
interferometer_plotter.figure_visibilities()
interferometer_plotter.figure_noise_map()
interferometer_plotter.figure_u_wavelengths()
interferometer_plotter.figure_v_wavelengths()
interferometer_plotter.figure_uv_wavelengths()
interferometer_plotter.figure_amplitudes_vs_uv_distances()
interferometer_plotter.figure_phases_vs_uv_distances()

"""The `InterferometerPlotter` may also plot a subplot of all of these attributes."""
interferometer_plotter.subplot_interferometer()

"""`Interferometer` contains the following attributes which can be plotted automatically via the `Include2D` object."""
include_2d = aplt.Include2D()
interferometer_plotter = aplt.InterferometerPlotter(
    interferometer=interferometer, include_2d=include_2d
)
interferometer_plotter.subplot_interferometer()
