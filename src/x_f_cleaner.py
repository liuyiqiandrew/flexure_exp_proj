import pandas as pd
import numpy as np


def read_data(caliper_path, scale_path):
    """ Read caliper and scale data """
    caliper = pd.read_csv(
        caliper_path, 
        sep='|',
        header=0,
        dtype={
            'displacement': np.float64,
            'delay': np.float64
        },
        parse_dates=['time']
    )

    caliper.loc[:, 'derr'] = caliper.displacement.diff().abs() / 2
    caliper.loc[0, 'derr'] = caliper.loc[0, 'derr']
    caliper.derr = 0.001 + caliper.derr

    scale = pd.read_csv(
        scale_path,
        sep='|',
        header=0,
        dtype={
            'weight': np.float64,
            'unit': str,
            'flag': str
        },
        parse_dates=['time']
    )
    scale.loc[:, 'ferr'] = scale.weight.diff().abs() / 2
    scale.loc[0, 'ferr'] = scale.loc[1, 'ferr']
    scale.ferr += 0.5
    
    return caliper, scale


def clean_raw_data(caliper:pd.DataFrame, scale:pd.DataFrame):
    """ Clean raw data heads and tails for data matching later """
    scale_start_ind = 0
    while (caliper.time < scale.time.iloc[scale_start_ind]).sum() == 0:
        scale_start_ind += 1
    caliper_start_ind = caliper.index[caliper.time < scale.time.iloc[scale_start_ind]].max()

    scale_end_ind = scale.index.max()
    while (caliper.time > scale.time.iloc[scale_end_ind]).sum() == 0:
        scale_end_ind -= 1
    caliper_end_index = caliper.index[caliper.time > scale.time.iloc[scale_end_ind]].min()
    clean_scale = scale.iloc[scale_start_ind:scale_end_ind + 1]
    clean_caliper = caliper.iloc[caliper_start_ind:caliper_end_index + 1]

    return clean_caliper.reset_index(drop=True), clean_scale.reset_index(drop=True)


def interpolate_displacement(caliper:pd.DataFrame, scale:pd.DataFrame):
    """ 
    Interpolate displacement data to match weight readings.
    Assuming slow change in displacement, the interpolation should be decently accurate.
    """
    clpr = np.zeros(scale.shape[0])
    clpr_err = np.zeros(scale.shape[0])
    row_iter = scale.iterrows()
    for row in row_iter:
        # get index for interpolate
        target_time = row[1].time
        clwr_ind = caliper.index[caliper.time < target_time].max()
        cupr_ind = clwr_ind + 1
        # interpolate
        dt_range = (caliper.time.iloc[cupr_ind] - caliper.time.iloc[clwr_ind]).total_seconds()
        dt = (target_time - caliper.time.iloc[clwr_ind]).total_seconds()
        dx_range = caliper.displacement.iloc[cupr_ind] - caliper.displacement.iloc[clwr_ind]
        dx_range_err = caliper.derr.iloc[cupr_ind] + caliper.derr.iloc[clwr_ind]
        clpr[row[0]] = dt / dt_range * dx_range + caliper.displacement.iloc[clwr_ind]
        clpr_err[row[0]] = dt / dt_range * dx_range_err
    return clpr, clpr_err, scale.weight.to_numpy(), scale.ferr.to_numpy()


def main():
    data_dir = "../data/bending_stiffness"
    annotation = "6in_332_3"
    caliper_path = f'{data_dir}/caliper_{annotation}.txt'
    scale_path = f"{data_dir}/scale_{annotation}.txt"
    caliper, scale = read_data(caliper_path=caliper_path, scale_path=scale_path)
    ccaliper, cscale = clean_raw_data(caliper=caliper, scale=scale)
    x_arr, xerr, f_arr, ferr = interpolate_displacement(caliper=ccaliper, scale=cscale)
    np.savez(f'{data_dir}/x_f_{annotation}.npz', displacement=x_arr, force=f_arr, derr=xerr, ferr=ferr)


if __name__ == "__main__":
    main()