# ========================================================================
"""               UTILITIES FOR ARULE IN PYTHON DEMO                   """
"""        © 2024 Ridgetop Group, Inc., All Rights Reserved            """
# ========================================================================

# Import Libraries and Functions
import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import matplotlib.patches as patches
from matplotlib.transforms import Bbox
from termcolor import colored

### FUNCTIONS
# readlog Function
def readlog(sdefname):
    """
    Read and display log file generated after each ARULE Run.

    sdefname: Name of the SDEF
    @returns: None
    """
    log_file_path = f"ARULE\\DATA\\LOG\\UD_ARULE_LOG_{sdefname}.txt"  # Update this with the actual path to your log file
    with open(log_file_path, 'r') as file:
        # Read the contents of the file
        log_contents = file.read()
        # Print the contents of the log file
    print("##### ARULEinPython:", colored(f'UD_ARULE_LOG_{sdefname}:', 'green'))
    print(colored(f'{log_contents}', 'magenta'))
    return None

# readDEFcontents Function
def readDEFcontents(sdefname):
    """
    Read contents of the SDEF & NDEF files for a particular ARULE Run.

    sdefname: Name of the SDEF
    @returns: A list of the contents in the NDEF for all nodes
    """
    # Read the contents from SDEF
    sdefpath = f'ARULE\\DEFS\\SDEF\\{sdefname}.txt'  
    with open(sdefpath, 'r') as sdeffile:
        sdeftext = sdeffile.read()
    ndefnames = re.findall(r"NDFNAME\s*=\s*'([^']+)", sdeftext)
    ndefids = re.findall(r"NDNUMID\s*=\s*(\d+)", sdeftext)
    ndefparams = []
    for ndefname, ndefid in zip(ndefnames, ndefids):
        # Read the contents from NDEF
        ndefpath = f'ARULE\\DEFS\\NDEF\\{ndefname}.txt'
        with open(ndefpath, 'r') as ndeffile:
            ndeftext = ndeffile.read()
        parameters = []
        parameters.append(ndefid)
        parameters.append(ndefname)
        matches = re.findall(r'(\w+)\s*=\s*([\w.-]+);', ndeftext)
        for match in matches:
            parameters.append(match[1])
        ndefparams.append(parameters)
    return ndefparams

# readARULEOutput Function 
def readARULEOutput(filepath):
    """
    Read contents of the ARULE .csv output for a particular run.

    filepath: Path to the ARULE .csv output file
    @returns: FLAG, DT, DA, RUL, PH, SOH, BD, EOL, FDNOM, FD, FFP, DPS, FFS, FFIN, RC0, RS0, RS0
    """
    output_data = pd.read_csv(filepath)
    flag = output_data['FLAG']    # Flag for internal program operation
    dt = output_data['DT']        # Data Time
    da = output_data['DA']        # Data Amplitude
    rul = output_data['RUL']      # Remaining Useful Life
    ph = output_data['PH']        # Prognostic Horizon
    soh = output_data['SOH']      # State of Health
    bd = output_data['BD']        # Begin of Degradation
    eol = output_data['EOL']      # End of Life
    fdnom = output_data['FDNOM']  # FD Nominal Value (Set by FDZ or calculated by FDC & FDCPTS)
    fd = output_data['FD']        # Feature Data
    ffp = output_data['FFP']      # FFP Signature Data
    dps = output_data['DPS']      # DPS signature Data
    ffs = output_data['FFS']      # FFS Signature Data
    ffin = output_data['FFIN']    # Functional Failure Input Data to ARULE Prognosis
    rc0 = output_data['RC0']      # Highest Return Code 
    rs0 = output_data['RS0']      # Reason for RC0
    rs1 = output_data['RS0']      # Reason for indicated RC
    return flag, dt, da, rul, ph, soh, bd, eol, fdnom, fd, ffp, dps, ffs, ffin, rc0, rs0, rs1

# findBDandEOL Function
def findBDandEOL(dt,bd,eol):
    """
    Find time-indexes of Beginning of Degradation (BD) and End of Life (EOL).

    dt: Array of Time values
    bd: Array of BD values output by ARULE
    eol: Array of EOL values output by ARULE
    @returns: bd_time_index, eol_time_index
    """
    est_bd_time = bd.iloc[-1]
    bd_time_index = np.where(dt == est_bd_time)
    est_eol_time = eol.iloc[-1]
    eol_time_index = np.where(dt == est_eol_time)
    return bd_time_index, eol_time_index

# plotARULEOutput Function
def plotARULEOutput(sdefname, ndefparams, show=True):
    """
    Plot contents of the ARULE .csv output for a particular run.

    sdefname: Name of the SDEF
    ndefparams: A list of the contents in the NDEF for all nodes
    show: Show plots (True/False)
    @returns: A plot of DA, RUL, PH, SOH, FD, FFP, DPS, FFS, FFIN in the PLOTS/ directory
    """
    for params in ndefparams:
        ndefid = params[0]
        ndefname = params[1]
        fdc = params[2]
        fdz = params[3]
        fdnm = params[4]
        fdcpts = params[5]
        fdpts = params[6]
        fdnv = params[7]
        ffpfail = params[8]
        pittff = params[9]
        piffsmod = params[10]
        infile = params[11]
        intype = params[12]
        outtype = params[13]
        output_folder = 'ARULE\\DATA\\DOUT'
        output_filename = f'ND_{ndefid}_DW_{sdefname}_{infile}_OUT{outtype}'
        output_filepath = os.path.join(output_folder, output_filename)
        print("##### ARULEinPython:", colored(f'Reading ARULE Results for {ndefname} ...', 'green'))
        flag, dt, da, rul, ph, soh, bd, eol, fdnom, fd, ffp, dps, ffs, ffin, rc0, rs0, rs1 = readARULEOutput(output_filepath)
        print("##### ARULEinPython:", colored(f'Finished Reading ARULE Results for {ndefname}!', 'green'))
        print("##### ARULEinPython:", colored(f'Plotting ARULE Results for {ndefname} ...', 'green'))
        # Plot Columns
        f, ax = plt.subplots(4,2, figsize=(25,12), sharex=True)
        title_font = font_manager.FontProperties(family= 'Sans Serif', weight='bold', style='normal', size=20)
        label_font = font_manager.FontProperties(family= 'Sans Serif', weight='bold', style='normal', size=16)
        legend_font = font_manager.FontProperties(family= 'Sans Serif', weight='bold', style='normal', size=12)
        title = f"{ndefname} ARULE Output"
        titletext = plt.suptitle(title, fontproperties=title_font)
        titletext.set_color('blue')
        bd_time_index, eol_time_index = findBDandEOL(dt,bd,eol)
        # Plot FD
        ax[0,0].plot(dt, da, 'k-', lw = 2, label=f'Feature Data')
        ax[0,0].vlines(dt.iloc[bd_time_index], np.amin(da), np.amax(da), linestyle='--', lw=3, color='green', label='Beginning of Degradation')
        ax[0,0].vlines(dt.iloc[eol_time_index], np.amin(da), np.amax(da), linestyle='--', lw=3, color='red', label='End of Life')
        ax[0,0].set_ylim(np.amin(da), np.amax(da))
        ax[0,0].set_ylabel(r'FD [AU]', fontproperties=label_font)
        #Plot SoH
        ax[1,0].plot(dt, soh, 'k-', lw = 2, label=f'State-of-Health')
        ax[1,0].scatter(dt.iloc[bd_time_index], soh.iloc[bd_time_index], s=100, lw=2, color='green', edgecolor='green', facecolors='none')
        ax[1,0].scatter(dt.iloc[eol_time_index], soh.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[1,0].set_ylabel(r'SoH [%]', fontproperties=label_font)
        # Plot RUL/PH
        ax[2,0].plot(dt, rul, 'm-', lw = 2, label=f'Remaining Useful Life')
        ax[2,0].plot(dt, ph, 'c-', lw = 2, label=f'Prognostic Horizon')
        ax[2,0].scatter(dt.iloc[bd_time_index], rul.iloc[bd_time_index], s=100, lw=2, color='green', edgecolor='green', facecolors='none')
        ax[2,0].scatter(dt.iloc[eol_time_index], rul.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[2,0].scatter(dt.iloc[eol_time_index], ph.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[2,0].set_ylabel(r'RUL/PH [AU]', fontproperties=label_font)
        ax[2,0].set_xlabel(r'Time [AU]', fontproperties=label_font)
        ax[2,0].xaxis.set_tick_params(which='both', labelbottom=True)
        ax[3,0].axis('off')
        # Plot FFP
        ax[0,1].plot(dt, ffp, 'k-', lw = 2, label=f'FFP Signature')
        ax[0,1].scatter(dt.iloc[bd_time_index], ffp.iloc[bd_time_index], s=100, lw=2, color='green', edgecolor='green', facecolors='none')
        ax[0,1].scatter(dt.iloc[eol_time_index], ffp.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[0,1].set_ylabel(r'FFP [AU]', fontproperties=label_font)
        #Plot DPS
        ax[1,1].plot(dt, dps, 'k-', lw = 2, label=f'DPS Signature')
        ax[1,1].scatter(dt.iloc[bd_time_index], dps.iloc[bd_time_index], s=100, lw=2, color='green', edgecolor='green', facecolors='none')
        ax[1,1].scatter(dt.iloc[eol_time_index], dps.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[1,1].set_ylabel(r'DPS [AU]', fontproperties=label_font)
        # Plot FFS
        ax[2,1].plot(dt, ffs, 'k-', lw = 2, label=f'FFS Signature')
        ax[2,1].scatter(dt.iloc[bd_time_index], ffs.iloc[bd_time_index], s=100, lw=2, color='green', edgecolor='green', facecolors='none')
        ax[2,1].scatter(dt.iloc[eol_time_index], ffs.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[2,1].set_ylabel(r'FFS [AU]', fontproperties=label_font)
        # Plot FFIN
        ax[3,1].plot(dt, ffin, 'k-', lw = 2, label=f'Functional Failure Input')
        ax[3,1].scatter(dt.iloc[bd_time_index], ffin.iloc[bd_time_index], s=100, lw=2, color='green', edgecolor='green', facecolors='none')
        ax[3,1].scatter(dt.iloc[eol_time_index], ffin.iloc[eol_time_index], s=100, lw=2, color='red', edgecolor='red', facecolors='none')
        ax[3,1].set_ylabel(r'FFIN [AU]', fontproperties=label_font)
        ax[3,1].set_xlabel(r'Time [AU]', fontproperties=label_font)
        #ax.fill_between(fft_data.index, fft_data[col], alpha=0.2, label='')
        for a in ax.flat:
            a.grid("on")
            a.legend(loc='best', prop=legend_font)
            a.xaxis.set_minor_locator(AutoMinorLocator())
            a.yaxis.set_minor_locator(AutoMinorLocator())
        f.tight_layout(h_pad=1, w_pad=3)
        plt.subplots_adjust(hspace=0.1)
        for a in ax.flat:
            plt.setp(a.xaxis.get_majorticklabels(), size='large')
            plt.setp(a.yaxis.get_majorticklabels(), size='large')
            plt.setp(a.xaxis.get_minorticklabels(), size='large')
            plt.setp(a.yaxis.get_minorticklabels(), size='large')
        output_filename = f"{ndefname}_ARULEOut.png"
        save_directory = 'PLOTS'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        f.savefig(os.path.join(save_directory, output_filename))
        if show == True:
            plt.show()
            plt.close()
        else:
            plt.close()
        print("##### ARULEinPython:", colored(f'Finished Plotting ARULE Results for {ndefname}!', 'green'))
        print("##### ARULEinPython:", colored(f'{output_filename} can be located in ARULE4Python/{save_directory}.', 'yellow'))
    return None