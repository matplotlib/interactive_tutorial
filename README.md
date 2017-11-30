# Time series exploration with matplotlib

## setup

To set up an enviroment for this tutorial use

    $ conda env create -f environment.yml

or

    $ conda create -n mpl-tutorial -c  anaconda matplotlib pandas pytables h5py ipython scipy python=3.6


for *nix

    $ source activate mpl-tutorial

for windows

    $ activate mpl-tutorial

### Troubleshooting

Try updating conda in case you are encountering a bug that has been fixed.

    $ conda update conda

Try this command (UNIX and OSX only) to ensure that the shell has not cached an
old reference to IPython. Do this after the `activate` step.

    $ hash -r

### for 99-get_data

    $ conda install -c conda-forge cartopy proj4

## Running

All of the examples should be run from IPython as

   %run -i NN-FILE.py

and should each be self-contained.
