# spin

A small utility to assist in setting usage modes of hybrid devices.

## Quick start

### Setup

- spin
    - Download [spin.py](https://raw.github.com/danielwe/spin/master/spin.py),
      or clone this repository.
- docopt
    - spin is dependent on the module [```docopt```](http://docopt.org/).
      Place [docopt.py](https://raw.github.com/danielwe/spin/master/docopt.py)
      in the same directory as spin.py, or install the module: ```pip install
      docopt```

This utility has been tested on a Lenovo ThinkPad Yoga running Ubuntu 13.10.

### Run

To run spin, cd to the directory where spin.py (and possibly docopt.py) are
located, make spin.py executable, and run it:

    spin.py

This will start spin in its default mode, with a graphical user interface
(GUI). Optionally, spin can be run without a GUI by using the command line
argument ```--nogui```:

    spin.py --nogui

Note that, written in PyQt, the utility will NOT respond to keyboard interrupts
such as Ctrl+C (see
[this](http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg13757.html)
for an explanation). To terminate it in non-GUI mode, use Ctrl+\ instead.

The utility implements two different usage modes: laptop and tablet. In laptop
mode all input devices are enabled, while in tablet mode the touchpad and
nipple are disabled. In both modes the screen is normally oriented. Laptop mode
is enabled on startup. Each time the device toggles between the laptop and
tablet states, the utility will switch modes. NOTE: spin does NOT detect the
state of the device upon startup, so it has to be started while the device is
in its laptop state to stay in sync with reality.

In graphical mode, spin also provides separate controls for each of the tasks
it is able to perform: change display orientation (with touchscreen and stylus
mapping following consistently), enable/disable touchscreen, enable/disable
touchpad, and enable/disable nipple. Controls are also provided to to switch
on/off the device state monitoring and to manually set laptop or tablet mode.
Finally, stylus proximity monitoring (disabling the touchscreen when the stylus
is active) can be enabled. This functionality is however disabled by default,
since Ubuntu now provides satisfactory palm rejection.
