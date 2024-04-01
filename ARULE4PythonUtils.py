# ========================================================================
"""               UTILITIES FOR ARULE IN PYTHON DEMO                   """
"""        © 2023 Ridgetop Group, Inc., All Rights Reserved            """
# ========================================================================

# Import Libraries and Functions
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
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
    sdefpath = f'ARULE\\DEFS\\SDEF\\{sdefname}.txt'  # Replace 'path_to_your_file.txt' with the actual file path
    with open(sdefpath, 'r') as sdeffile:
        sdeftext = sdeffile.read()
    ndefnames = re.findall(r"NDFNAME\s*=\s*'([^']+)'", sdeftext)
    ndefparams = []
    for ndefname in ndefnames:
        # Read the contents from NDEF
        ndefpath = f'ARULE\\DEFS\\NDEF\\{ndefname}.txt'
        ndefidmain = ndefname.split('_')[1]
        ndefid = [ndefid for ndefid in ndefidmain][-1]
        with open(ndefpath, 'r') as ndeffile:
            ndeftext = ndeffile.read()
        parameters = []
        parameters.append(ndefid)
        parameters.append(ndefname)
        matches = re.findall(r'(\w+)\s*=\s*([\w.]+);', ndeftext)
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
        f, ax = plt.subplots(4,2, figsize=(20,10), sharex=True)
        title_font = font_manager.FontProperties(family= 'Sans Serif', weight='bold', style='normal', size=20)
        label_font = font_manager.FontProperties(family= 'Sans Serif', weight='bold', style='normal', size=16)
        legend_font = font_manager.FontProperties(family= 'Sans Serif', weight='bold', style='normal', size=12)
        title = f"{ndefname} ARULE Output"
        titletext = plt.suptitle(title, fontproperties=title_font)
        titletext.set_color('blue')
        ax[0,0].plot(dt, da, 'r-', lw = 2, label=f'Data Amplitude')
        ax[0,0].set_ylabel(r'DA [AU]', fontproperties=label_font)
        ax[1,0].plot(dt, fd, 'r-', lw = 2, label=f'Feature Data')
        ax[1,0].set_ylabel(r'FD [AU]', fontproperties=label_font)
        ax[2,0].plot(dt, soh, 'r-', lw = 2, label=f'State-of-Health')
        ax[2,0].set_ylabel(r'SoH [%]', fontproperties=label_font)
        ax[3,0].plot(dt, rul, 'm-', lw = 2, label=f'Remaining Useful Life')
        ax[3,0].plot(dt, ph, 'c-', lw = 2, label=f'Prognostic Horizon')
        ax[3,0].set_ylabel(r'RUL/PH [AU]', fontproperties=label_font)
        ax[3,0].set_xlabel(r'Time [AU]', fontproperties=label_font)
        ax[0,1].plot(dt, ffp, 'r-', lw = 2, label=f'FFP Signature')
        ax[0,1].set_ylabel(r'FFP [AU]', fontproperties=label_font)
        ax[1,1].plot(dt, dps, 'r-', lw = 2, label=f'DPS Signature')
        ax[1,1].set_ylabel(r'DPS [AU]', fontproperties=label_font)
        ax[2,1].plot(dt, ffs, 'r-', lw = 2, label=f'FFS Signature')
        ax[2,1].set_ylabel(r'FFS [AU]', fontproperties=label_font)
        ax[3,1].plot(dt, ffin, 'r-', lw = 2, label=f'Functional Failure Input')
        ax[3,1].set_ylabel(r'FFIN [AU]', fontproperties=label_font)
        ax[3,1].set_xlabel(r'Time [AU]', fontproperties=label_font)
        #ax.fill_between(fft_data.index, fft_data[col], alpha=0.2, label='')
        for a in ax.flat:
            a.grid("on")
            a.legend(loc='upper right', prop=legend_font)
            a.xaxis.set_minor_locator(AutoMinorLocator())
            a.yaxis.set_minor_locator(AutoMinorLocator())
        plt.gcf().autofmt_xdate()
        f.tight_layout(h_pad=1, w_pad=3)
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
        print("##### ARULEinPython:", colored(f'{output_filename} can be located in ARULE4Python\{save_directory}.', 'yellow'))
        return None