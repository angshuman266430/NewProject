import os
import xarray as xr
import pandas as pd
import glob

base_dir = r"Z:\GLO\TC_related\NewShift"
events = ['MostLikely_Shifted']

# Function to shift the data by given hours
def shift_data(in_dir, out_dir, hours_shift):
    os.makedirs(out_dir, exist_ok=True)
    nc_files = glob.glob(os.path.join(in_dir, '*.nc'))

    for file in nc_files:
        ds = xr.open_dataset(file)

        # Shift time dimension by the given number of hours
        new_time = pd.date_range(start=f"1970-01-01 00:30", periods=len(ds['time']), freq='H') + pd.Timedelta(hours=hours_shift)
        ds = ds.assign_coords(time=new_time)

        # Generate new output file path
        base = os.path.basename(file).replace("_shift1970", "")  # Remove "_shift1970" from filename
        new_file = os.path.join(out_dir, base.rsplit(".", 1)[0] + f"_shift{hours_shift}h.nc")

        ds.to_netcdf(new_file)

for event in events:
    in_dir = os.path.join(base_dir, event)

    # For +6 hours
    out_dir_plus6 = os.path.join(base_dir, f'{event}_plus6')
    shift_data(in_dir, out_dir_plus6, 6)

    # For -6 hours
    out_dir_minus6 = os.path.join(base_dir, f'{event}_minus6')
    shift_data(in_dir, out_dir_minus6, -6)
