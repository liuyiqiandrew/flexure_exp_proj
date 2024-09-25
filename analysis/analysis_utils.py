import numpy as np
import scipy.stats as stt
import matplotlib.pyplot as plt


def clean_zero_offset(x, f, fmin=20, fit_min=100, fit_max=400):
    x = x[f > fmin]
    f = f[f > fmin]
    fit_msk = (f > fit_min) * (f < fit_max)
    res = stt.linregress(f[fit_msk], x[fit_msk])
    return x - res.intercept, f

def plot_offset_corrected_raw(path, iter=range(3), save_path=None, legend=False, 
                              fmin=20, fit_min=100, fit_max=400):
    plt.figure(dpi=300)
    xls = []
    xerrls = []
    fls = []
    ferrls = []
    for i in iter:
        displace_data = np.load(path.format(i + 1))
        x_raw, f_raw = displace_data['displacement'], -displace_data['force']
        x_err, f_err = displace_data['derr'][f_raw > fmin], displace_data['ferr'][f_raw > fmin]
        x, f = clean_zero_offset(x_raw, f_raw, fmin, fit_min, fit_max)
        plt.scatter(x, f, s=3, label=f'Trial {i + 1}')
        xls.append(x)
        xerrls.append(x_err)
        fls.append(f)
        ferrls.append(f_err)
    plt.xlabel('Displacement (mm)')
    plt.ylabel('Force (lbf)')
    if legend:
        plt.legend()
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    return np.concatenate(xls), np.concatenate(fls), np.concatenate(xerrls), np.concatenate(ferrls)

def get_raw(path, iter=range(3)):
    xls = []
    xerrls = []
    fls = []
    ferrls = []
    for i in iter:
        displace_data = np.load(path.format(i + 1))
        x_raw, f_raw = displace_data['displacement'], -displace_data['force']
        x_err, f_err = displace_data['derr'], displace_data['ferr']
        xls.append(x_raw)
        xerrls.append(x_err)
        fls.append(f_raw)
        ferrls.append(f_err)
    return np.concatenate(xls), np.concatenate(fls), np.concatenate(xerrls), np.concatenate(ferrls)