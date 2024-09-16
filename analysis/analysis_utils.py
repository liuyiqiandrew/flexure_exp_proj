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
    fls = []
    for i in iter:
        displace_data = np.load(path.format(i + 1))
        x_raw, f_raw = displace_data['displacement'], -displace_data['force']
        x, f = clean_zero_offset(x_raw, f_raw, fmin, fit_min, fit_max)
        plt.scatter(x, f, s=3, label=f'Trial {i + 1}')
        xls.append(x)
        fls.append(f)
    plt.xlabel('Displacement (mm)')
    plt.ylabel('Force (lbf)')
    if legend:
        plt.legend()
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    return np.concatenate(xls), np.concatenate(fls)

def get_raw(path, iter=range(3)):
    xls = []
    fls = []
    for i in iter:
        displace_data = np.load(path.format(i + 1))
        x_raw, f_raw = displace_data['displacement'], -displace_data['force']
        xls.append(x_raw)
        fls.append(f_raw)
    return np.concatenate(xls), np.concatenate(fls)