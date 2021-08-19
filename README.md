# pysolvation

Python package for calculating solution thermochemical parameters. Includes a
limited wrapper for COSMOtherm that can handle GSOLV, henry and flashpoint jobs and tools for fitting Abraham solvent and solute parameters.

To use the COSMOtherm wrapper users should define the environment variables:


COSMOTHERM corresponding to the COSMOtherm executable
ex: /home/gridsan/groups/RMG/Software/COSMOtherm2021/COSMOtherm/BIN-LINUX/cosmotherm


COSMOTHERMPATH corresponding to the COSMOtherm directory
ex: /home/gridsan/groups/RMG/Software/COSMOtherm2021
