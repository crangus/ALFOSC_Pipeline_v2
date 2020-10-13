Update to Luca Izzo's quick data reduction code for ALFOSC spectra

Version 2 - now includes fitting an improved wavlength solution to the 2D spectra. 

General description:

Code reduces ALFOSC NOT spectra, obtained with the grism #4 and provides a flux-calibrated spectrum (calibration based on archive data). To run this script the entire set of files and directories must be pulled.

The pipeline uses pyraf (a python wrapper for iraf), which is currently maintained by stsci through a conda environment. It’s easy to install with:

conda config --add channels http://ssb.stsci.edu/astroconda

conda create -n iraf27 python=2.7.15 iraf-all pyraf-all stsci

Then you need to set up an iraf environment

mkdir /home/user/iraf
cd /home/user/iraf
mkiraf

(Answer ‘xterm’ when asked what kind terminal you want to set this up in)

NOTE: there is a bug with matplolib/pyraf which you might need to do the following for:

mkdir -p ~/.matplotlib
echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc

You can then activate this environment in any terminal with

source activate iraf27

To run the code, copy the relevant science raw files (e.g. the 2D slit images named 'ALxxxxxfits') into the directory and run

python quick_code_update.py

The will read the raw science frames, bias and flat field correct them before applying a 2D wavelength solution. When promted, 

'Dispersion axis (1=along lines, 2=along columns, 3=along z) (1:3) (2): '

Enter '2' and hit return. 

The code will then open an interactive (classical) window where you can select the trace and fit the background. Detailed instructions for the interactive use of apall can be found here: http://joshwalawender.github.io/IRAFtutorial/IRAFintro_06.html

Once extracted, the spectrum is then flux calibrated and trimmed to the observed wavelength range (4000-9000 \AA) and moved into the output folder. A text file of the 1D spectrum is also generated. The raw science files are then deleted.

I fully acknowledge Luca Izzo for producing the original version of the script and helpful discussions for updates!
