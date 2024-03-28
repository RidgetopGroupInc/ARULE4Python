# ========================================================================
"""         ARULE IN PYTHON DEMO FOR THE "DEMO2" CASE STUDY            """
"""        © 2023 Ridgetop Group, Inc., All Rights Reserved            """
# ========================================================================
print("##### ARULEinPython: Starting Demo...")

# Import Libraries and Functions
import os
import numpy as np
import matplotlib.pyplot as plt
from createDEF import createSDEF, createNDEF
import subprocess
import sys
from termcolor import colored

print("##### ARULEinPython:", colored('Finished importing libraries and functions!', 'green'))

# Initialize SDEF & NDEF for Demo2
pre_packaged = False # Are the SDEF/NDEF pre-packaged? (True/False)

# If False was chosen above do not edit this!
### SDEF
system_node_list = [
    (1, 'DEMO2_NODE1', -9),
    (2, 'DEMO2_NODE2', -9),
    (3, 'DEMO2_NODE3', -9)
]
sdefdirectory = "ARULE\\DEFS\\SDEF"  # Specify your desired directory here
sdeffilename = "DEMO2.txt"
sdefname = os.path.splitext(sdeffilename)[0]
### NDEF
node_params = [
    (24.000, 0.000, 5.000, 10, 5, 1.265, 67.000, 220.000, 2, 'SP4000_1', '.txt', '.csv', -9), 
    (24.000, 0.000, 5.000, 10, 5, 1.285, 73.000, 220.000, 2, 'SP4000_1', '.txt', '.csv', -9),
    (24.000, 0.000, 5.000, 10, 5, 1.275, 70.000, 220.000, 2, 'SP4000_2', '.csv', '.csv', -9)
]
ndefdirectory = "ARULE\\DEFS\\NDEF"  # Specify your desired directory here
ndeffilenames = ["DEMO2_NODE1.txt", "DEMO2_NODE2.txt", "DEMO2_NODE3.txt"]
ndefnames = [os.path.splitext(filename)[0] for filename in ndeffilenames]

# Conditional for pre-packaging
if pre_packaged == True:
    pass
    print("##### ARULEinPython:", colored('SDEF & NDEF Files pre-packaged! Running UD_ARULE now.', 'yellow'))
elif pre_packaged == False:
    createSDEF(system_node_list, sdefdirectory, sdeffilename, sdefname) # Call the createSDEF function
    for i, params in enumerate(node_params):
        ndeffilename = ndeffilenames[i]
        ndefname = ndefnames[i]
        createNDEF(params, ndefdirectory, ndeffilename, ndefname) # Call the createNDEF function
    print("##### ARULEinPython:", colored('SDEF & NDEF Created! Running UD_ARULE now.', 'green'))

# Read and Display Log Function
def readlog(sdefname):
    log_file_path = f"ARULE\\DATA\\LOG\\UD_ARULE_LOG_{sdefname}.txt"  # Update this with the actual path to your log file
    with open(log_file_path, 'r') as file:
        # Read the contents of the file
        log_contents = file.read()
        # Print the contents of the log file
    print("##### ARULEinPython:", colored(f'UD_ARULE_LOG_{sdefname}:', 'green'))
    print(log_contents)
    return None

### Call ARULEforWindows.exe using subprocess
command = ['ARULE4Python.exe', "DEMO2", "./"]
subprocess.run(command, check=True)
readlog(sdefname)
print("##### ARULEinPython:", colored('ARULE Run Complete!', 'green'))