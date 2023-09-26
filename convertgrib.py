import os
from osgeo import gdal

# Define the directory containing the .grib2 files
directory = "S:\For_Angshuman\Greenbelt\Grib_files"

# List all .grib2 files in the directory
grib_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.grib2')]

# Loop over each .grib2 file and convert it to .nc
for input_file_path in grib_files:
    # Define the output NetCDF file path based on the input file name
    output_file_path = os.path.join(directory, os.path.splitext(os.path.basename(input_file_path))[0] + '.nc')

    # Open the GRIB2 file
    grib_ds = gdal.Open(input_file_path, gdal.GA_ReadOnly)

    # Check if the GRIB2 file is opened successfully
    if grib_ds is None:
        print(f"Failed to open {input_file_path}. Skipping...")
        continue

    # Create a NetCDF file with the same structure as the GRIB2 file
    netcdf_driver = gdal.GetDriverByName('NetCDF')
    netcdf_ds = netcdf_driver.CreateCopy(output_file_path, grib_ds)

    # Close datasets
    grib_ds = None
    netcdf_ds = None

    print(f"Conversion completed: {output_file_path} created.")
