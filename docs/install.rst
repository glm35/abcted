Installing abcde (development version)
======================================

Install Python3
---------------

To just run abcde:

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


Create a venv and install abcde pip dependencies
------------------------------------------------

::

   $ python3 -m venv ~/.tmp/venv-devel-abcde/
   $ source ~/.tmp/venv-devel-abcde/bin/activate
   $ pip install py-getch sphinx

Install pyfluidsynth3 (in the venv)
-----------------------------------

::

   $ cd ~/code
   $ git clone https://github.com/glm35/pyfluidsynth3.git
   $ cd ~/code/pyfluidsynth3
   $ git checkout --track origin/gl-devel
   $ python setup.py install

Get abcde source code
---------------------

::

   $ cd ~/code
   $ git clone https://github.com/glm35/abcde.git

Start abcde
-----------

::

   $ cd ~/code/abcde
   $ python abcde/main.py
