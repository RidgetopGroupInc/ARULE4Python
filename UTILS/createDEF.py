# ========================================================================
"""    PYTHON SYSTEM/NODE DEFINITION (SDEF/NDEF) CREATOR FOR ARULE     """
"""        © 2024 Ridgetop Group, Inc., All Rights Reserved            """
# ========================================================================
### Import Libraries
import os

### createSDEF Function
def createSDEF(system_node_list, directory, filename, sdefname):
    """
    Create a .txt SDEF File to be input to ARULE Windows CLI.

    system_node_list: List of (NDNUMID, NDFNAME, ENDDEF)
    directory: Central Directory to store SDEF
    filename: Desired Filename for SDEF
    sdefname: Name of the SDEF
    @returns: A .txt SDEF File in a "SDEF" subdirectory within the central directory
    """
    filepath = os.path.join(directory, f"{filename}")
    content = "%**************************************************************************\n"
    content += "% {} System Definition (SDEF)\n".format(sdefname)
    content += "% Each line is a maximum of eighty (80) characters!\n"
    content += "%**************************************************************************\n"
    for NDNUMID, NDFNAME, ENDDEF in system_node_list:
        content += "NDNUMID = {};\t\t\t % Node Definition Number\n".format(NDNUMID)
        content += "NDFNAME = '{}';\t % Node Definition Filename\n".format(NDFNAME)
    content += "%**************************************************************************\n"
    content += "ENDDEF = {};\t\t\t\t % End of Node Definition\n".format(ENDDEF)
    with open(filepath, 'w') as file:
        file.write(content)
    return None

### createNDEF Function
def createNDEF(node_params, directory, filename, ndefname):
    """
    Create a .txt NDEF File to be used within a SDEF File.

    node_params: List of (FDC, FDZ, FDNM, FDCPTS, FDPTS, FDNV, FFPFAIL, PITTFF, PIFFSMOD, INFILE, INTYPE, OUTTYPE, ENDDEF) for a given node
    directory: Central Directory to store NDEF
    filename: Desired Filename for NDEF
    ndefname: Name of the NDEF
    @returns: A .txt SDEF File in a "SDEF" subdirectory within the central directory
    """
    FDC, FDZ, FDNM, FDCPTS, FDPTS, FDNV, FFPFAIL, PITTFF, PIFFSMOD, INFILE, INTYPE, OUTTYPE, ENDDEF = node_params
    filepath = os.path.join(directory, f"{filename}")
    content = "%********************************************************************************************************\n"
    content += "% {} Node Definition (NDEF)\n".format(ndefname)
    content += "%********************************************************************************************************\n"
    content += "%**Feature Data: FD = FDZ*(dP/P)^FDNV + DC + NOISE\n"
    content += "FDC = {};\t\t\t % Feature Data, DC\n".format(FDC)
    content += "FDZ = {};\t\t\t % Nominal FD0 value for AC coefficient: 0=use FDC\n".format(FDZ)
    content += "FDNM = {};\t\t\t % Percent Noise Margin\n".format(FDNM)
    content += "FDCPTS = {};\t\t\t % Data points to average for FDC: up to 25\n".format(FDCPTS)
    content += "FDPTS = {};\t\t\t % Data points to average for FD: up to 5\n".format(FDPTS)
    content += "FDNV = {};\t\t\t % Degradation Power n\n".format(FDNV)
    content += "FFPFAIL = {};\t\t\t % Functional Failure Margin - percent above nominal\n".format(FFPFAIL)
    content += "%**Prognostic Modeling\n"
    content += "PITTFF = {};\t\t\t % Default RUL = TTFF value\n".format(PITTFF)
    content += "PIFFSMOD = {};\t\t\t % Model (1=Convex, 2=Linear, 3=Concave, 4=Convex-Concave, 5=Concave-Convex)\n".format(PIFFSMOD)
    content += "%**File Dependent Parameters\n"
    content += "INFILE = {};\t\t % Input Filename (_OUT appended for Output)\n".format(INFILE)
    content += "INTYPE = {};\t\t\t % Input File Type (.csv/.txt)\n".format(INTYPE)
    content += "OUTTYPE = {};\t\t\t % Output File Type (.csv/.txt)\n".format(OUTTYPE)
    content += "%********************************************************************************************************\n"
    content += "ENDDEF = {};\t\t\t % End of Node Definition\n".format(ENDDEF)
    with open(filepath, 'w') as file:
        file.write(content)
    return None