Installing abcted (development version)
=======================================

Install Python3
---------------

To just run abcted:

Under Linux Mint::

   $ sudo apt install python3 python3-venv python3-tk

Under Fedora (26)::

   $ sudo dnf install python3 python3-tkinter

Install FluidSynth and sound fonts
----------------------------------

::

   $ sudo apt install fluidsynth fluid-soundfont-gm fluid-soundfont-gs

Under Fedora::

   $ sudo dnf install fluidsynth fluid-soundfont-gm fluid-soundfont-gs

Build libfluidsynth development version
---------------------------------------

abcted requires libfluidsynth new tempo API which is not available with Ubuntu 20.04.

Get the code::

    $ mkdir -p ~/code/third-party/
    $ cd ~/code/third-party/
    $ git clone https://github.com/FluidSynth/fluidsynth.git
    $ cd fluidsynth
    $ git reset --hard b8fb6c81e1ca27c0bba2f6a0168832214f91d497

Install build dependencies (Ubuntu 20.04)::

  $ sudo apt install cmake libglib2.0-dev libasound2-dev \
        libreadline-dev libsndfile-dev

Build::

    $ mkdir build
    $ cd build
    $ cmake ..
    $ make
    $ make check

Build the docs::

    $ sudo apt install doxygen
    $ cmake ..
    $ make doxygen

Create a venv and install abcted pip dependencies
-------------------------------------------------

::

   $ python3 -m venv --system-site-packages ~/.tmp/venv/abcted/
   $ source ~/.tmp/venv/abcted/bin/activate
   $ pip install py-getch sphinx sphinx-rtd-theme

Install pyfluidsynth3 (in the venv)
-----------------------------------

::

   $ cd ~/code
   $ git clone https://github.com/glm35/pyfluidsynth3.git
   $ cd ~/code/pyfluidsynth3
   $ git checkout --track origin/gl-devel-new-tempo-api
   $ python setup.py install

Get abcted source code
----------------------

::

   $ cd ~/code
   $ git clone https://github.com/glm35/abcted.git

Start abcted
------------

::

   $ cd ~/code/abcted
   $ python abcted/main.py  -l ~/code/third-party/fluidsynth/build/src/libfluidsynth.so.3.0.0
