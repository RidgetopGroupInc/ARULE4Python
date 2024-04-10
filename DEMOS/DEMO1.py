# ========================================================================
"""         ARULE IN PYTHON DEMO FOR THE "DEMO1" CASE STUDY            """
"""        © 2024 Ridgetop Group, Inc., All Rights Reserved            """
# ========================================================================

# Import Libraries and Functions
import os
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
from termcolor import colored
print("##### ARULEinPython:", colored(' !!! WELCOME TO ADAPTIVE REMAINING USEFUL LIFE ESTIMATOR (ARULE) !!!', 'yellow'))
### Directory Structure
current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))
arule_directory = os.path.join(parent_directory,'ARULE\\')
plots_directory = os.path.join(parent_directory,'PLOTS\\')
utils_directory = os.path.join(parent_directory,'UTILS\\')
### Import Functions
sys.path.append(utils_directory)
from createDEF import createSDEF, createNDEF
from ARULE4PythonUtils import readlog, readDEFcontents, readARULEOutput, plotARULEOutput
os.chdir(current_directory)
print("##### ARULEinPython:", colored('Finished importing libraries and functions!', 'green'))

# Initialize SDEF & NDEF for DEMO1
pre_packaged = False # Are the SDEF/NDEF pre-packaged? (True/False)

# If False was chosen above do not edit this!
sysname = 'DEMO1' # Name of the System
nodename = 'NODE1' # Name of NODE1
### SDEF
system_node_list = [
    (1, f'{sysname}_{nodename}', -9)
]
sdefdirectory = os.path.join(arule_directory, "DEFS\\SDEF\\")
sdeffilename = f"{sysname}.txt"
sdefname = os.path.splitext(sdeffilename)[0]
### NDEF
node_params = [
    (24.000, 0.000, 5.000, 10, 5, 1.275, 70.000, 220.000, 2, 'SP4000_1', '.txt', '.csv', -9)
]
ndefdirectory = os.path.join(arule_directory, "DEFS\\NDEF\\")
ndeffilenames = [f"{sysname}_{nodename}.txt"]
ndefnames = [os.path.splitext(filename)[0] for filename in ndeffilenames]

# Conditional for pre-packaging
if pre_packaged == True:
    pass
    print("##### ARULEinPython:", colored('SDEF & NDEF Files pre-packaged! Running UD_ARULE now...', 'yellow'))
elif pre_packaged == False:
    createSDEF(system_node_list, sdefdirectory, sdeffilename, sdefname) # Call the createSDEF function
    for i, params in enumerate(node_params):
        ndeffilename = ndeffilenames[i]
        ndefname = ndefnames[i]
        createNDEF(params, ndefdirectory, ndeffilename, ndefname) # Call the createNDEF function
    print("##### ARULEinPython:", colored('SDEF & NDEF Created! Running UD_ARULE now...', 'green'))

### Call ARULEforWindows.exe using subprocess
os.chdir(parent_directory)
print("##### ARULEinPython:", colored(f'Ridgetop DLM License Check & UD_ARULE Run Commencing...', 'green'))
command = [f'{parent_directory}/UD_ARULE.exe', f'{sysname}', '2', '0', '1', f'{parent_directory}']
subprocess.run(command, check=True)
#readlog(sdefname)
print("##### ARULEinPython:", colored('UD_ARULE Run Complete!', 'green'))

### Plot ARULE Results
ndefparams = readDEFcontents(sdefname)
plotARULEOutput(sdefname, ndefparams, show=False)
print("##### ARULEinPython:", colored('Thanks for using ARULE in Python! © Ridgetop Group Inc., 2019-2024', 'red'))