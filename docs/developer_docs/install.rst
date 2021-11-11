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


Create a venv and install abcted pip dependencies
-------------------------------------------------

::

   $ python3 -m venv --system-site-packages ~/.tmp/venv-devel-abcted/
   $ source ~/.tmp/venv-devel-abcted/bin/activate
   $ pip install py-getch sphinx sphinx-rtd-theme

Install pyfluidsynth3 (in the venv)
-----------------------------------

::

   $ cd ~/code
   $ git clone https://github.com/glm35/pyfluidsynth3.git
   $ cd ~/code/pyfluidsynth3
   $ git checkout --track origin/gl-devel
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
   $ python abcted/main.py
