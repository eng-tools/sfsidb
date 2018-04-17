import engformat as ef
import matplotlib.pyplot as plt
import numpy as np
import eqsig
from sfsidb import deprecated_load as load
from bwplot import cbox, lsbox
import bwplot


# THIS FILE HAS DEPRECATED

def add_ylabel(fname):
    if "PPT" in fname:
        return "Pore pressure [Pa]"
    elif "ACC" in fname:
        return "Acceleration [m/s2]"
    return fname


def basic(sub_plot, folder_path, fname, dbset, label=None, ccbox=None, lls=None, quiet=False):
    if quiet:
        series, time = load.load_record(folder_path + fname, dbset, quiet=True)
        if series is None:  # Could not find file
            return
    else:
        series, time = load.load_record(folder_path + fname, dbset)
    if series is None:
        raise FileNotFoundError
    if label is None:
        label = fname

    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)

    sub_plot.plot(time, series, label=label, **kwargs)
    ef.time_series(sub_plot)
    ef.revamp_legend(sub_plot)

    plt.xlabel('Time [s]')
    plt.ylabel(add_ylabel(fname))


def fourier_spectrum(sub_plot, folder_path, fname, dbset, label=None, ccbox=None, lls=None, quiet=False):
    if quiet:
        series0, time = load.load_record(folder_path + fname, dbset, quiet=True)
        if series0 is None:  # Could not find file
            return
    else:
        series0, time = load.load_record(folder_path + fname, dbset)

    dt = time[1] - time[0]
    if label is None:
        label = fname

    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)

    acc0 = eqsig.AccSignal(series0, dt)
    sub_plot.loglog(acc0.fa_frequencies, np.abs(acc0.fa_spectrum), label=label, **kwargs)
    sub_plot.loglog(acc0.smooth_fa_frequencies, acc0.smooth_fa_spectrum, label=label + "-smooth", **kwargs)



def transfer_function(sub_plot, folder_path, fname0, fname1, dbset, label=None, significant=True, quiet=False,
                      ccbox=False, lls=False):
    if quiet:
        series0, time = load.load_record(folder_path + fname0, dbset, quiet=True)
        series1, time = load.load_record(folder_path + fname1, dbset, quiet=True)
        if series0 is None or series1 is None:
            print("Could not find file")
            return
    else:
        series0, time = load.load_record(folder_path + fname0, dbset)
        series1, time = load.load_record(folder_path + fname1, dbset)
    dt = time[1] - time[0]
    if label is None:
        label = fname1

    acc0 = eqsig.AccSignal(series0, dt)
    fas0_smooth = np.abs(acc0.smooth_fa_spectrum)
    ffs_smooth = acc0.smooth_fa_frequencies

    acc1 = eqsig.AccSignal(series1, dt)
    fas1_smooth = np.abs(acc1.smooth_fa_spectrum)

    h_smooth = fas1_smooth / fas0_smooth

    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)

    if significant:
        # Only plot range of frequencies that are high
        min_freq_i, max_freq_i = eqsig.significant_range(fas1_smooth)
        sub_plot.semilogx(ffs_smooth[min_freq_i:max_freq_i], h_smooth[min_freq_i:max_freq_i], label=label, **kwargs)
    else:
        sub_plot.semilogx(ffs_smooth, h_smooth, label=label, **kwargs)
    sub_plot.set_ylabel("H: " + fname0)


def pore_pressure_series(sub_plot, folder_path, fname, dbset, label=None, ccbox=None, lls=None, quiet=False):
    if quiet:
        series, time = load.load_record(folder_path + fname, dbset, quiet=True)
        if series is None:  # Could not find file
            return
    else:
        series, time = load.load_record(folder_path + fname, dbset)
    if "PPT" not in fname:
        raise ValueError("PPT record required for pore_pressure view")

    if label is None:
        label = fname

    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)

    sub_plot.plot(time, series, label=label, **kwargs)
    ef.time_series(sub_plot)
    ef.revamp_legend(sub_plot)

    plt.xlabel('Time [s]')
    plt.ylabel("Pore pressure [Pa]")


def total_stress(sub_plot, folder_path, esigy_fname, ppt_fname, dbset, label=None, ccbox=None, lls=None, quiet=False):
    if quiet:
        esigy_series, time = load.load_record(folder_path + esigy_fname, dbset, quiet=True)
        ppt_series, time = load.load_record(folder_path + ppt_fname, dbset, quiet=True)
        if esigy_series is None or ppt_series is None:  # Could not find file
            return
    else:
        esigy_series, time = load.load_record(folder_path + esigy_fname, dbset, quiet=False)
        ppt_series, time = load.load_record(folder_path + ppt_fname, dbset, quiet=False)
    if label is None:
        label = ppt_fname

    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)
    del kwargs['ls']
    del kwargs['c']

    sub_plot.fill_between(time, -esigy_series + ppt_series, 0, label="Total stress", **kwargs)
    # sub_plot.plot(time, -esigy_series + ppt_series, 0, label="Total stress", **kwargs)
    sub_plot.fill_between(time, -esigy_series, label="Effective stress", **kwargs)
    # sub_plot.plot(time, ppt_series, label="Pore-pressure", **kwargs)
    ef.time_series(sub_plot)
    ef.revamp_legend(sub_plot)

    plt.xlabel('Time [s]')
    #plt.ylabel(add_ylabel(fname))


def ru_series(sub_plot, folder_path, fname, dbset, label=None, ccbox=None, lls=None, quiet=False):
    if quiet:
        series, time = load.load_record(folder_path + fname, dbset, quiet=True)
        if series is None:  # Could not find file
            return
    else:
        series, time = load.load_record(folder_path + fname, dbset)
    if "ESIG" not in fname:
        raise ValueError("ESIG record required for ru view")

    esigy = series[0]  # initial effective vertical stress
    # calculating ru (ru=1-(esigy/esigy_initial)
    ru_vals = 1 - (series / esigy)

    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)
    # plotting time vs ru
    sub_plot.plot(time, ru_vals, label=label, **kwargs)

    sub_plot.xlabel('Time [s]')
    sub_plot.ylabel('Ru')


def gamma_v_tau(sub_plot, folder_path, strs_fname, tau_fname, dbset, label=None, ccbox=None, lls=None, quiet=False):
    if quiet:
        strs, time = load.load_record(folder_path + strs_fname, dbset, quiet=True)
        tau, time = load.load_record(folder_path + tau_fname, dbset, quiet=True)
        if strs is None or tau is None:
            print("Could not find file")
            return
    else:
        strs, time = load.load_record(folder_path + strs_fname, dbset)
        tau, time = load.load_record(folder_path + tau_fname, dbset)

    if label is None:
        label = tau_fname
    kwargs = bwplot.pack_plotting_kwargs(ccbox, lls)
    sub_plot.plot(strs, tau, label=label, **kwargs)
    sub_plot.set_xlabel('Shear strain [%]')
    sub_plot.set_ylabel('Shear stress [kPa]')
