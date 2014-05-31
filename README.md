# spin

A convenience utility for laptop/tablet devices running Linux.

## Features

- Automatic disabling/enabling of touchpad and nipple when device is toggled
  between its laptop and tablet states
- Automatic palm rejection when using stylus
- Manual control of display orientation and enabled input devices

## Setup

- spin
    - Download [spin.py](https://raw.github.com/danielwe/spin/master/spin.py),
      or clone this repository.
- docopt
    - spin is dependent on the module [```docopt```](http://docopt.org/).
      Place [docopt.py](https://raw.github.com/danielwe/spin/master/docopt.py)
      in the same directory as spin.py, or install the module: ```pip install
      docopt```

This utility has been tested on a Lenovo ThinkPad Yoga running Ubuntu 13.10 and
14.04.

## Run

To run spin, cd to the directory where spin.py (and possibly docopt.py) is
located, make spin.py executable, and run it:

    spin.py

This will start spin in its default mode, with a GUI. To run it without the
GUI, use the command line argument ```--nogui```:

    spin.py --nogui

You might want to add a symbolic link to spin.py somewhwere in your PATH (e.g.
```~/bin```) in order to make it available as a command. This way, it can
easily be configured to run automatically on startup etc.

Note that, written in PyQt, spin will NOT respond to keyboard interrupts such
as Ctrl+C (see
[this](http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg13757.html)
for more information). To terminate it in non-GUI mode, use Ctrl+\ instead.

## Details

By default, spin toggles between two different usage modes, laptop and tablet,
based on the physical state of the device. In laptop mode all input devices are
enabled, while in tablet mode the touchpad and nipple are disabled. NOTE: spin
only detects when the physical state changes, not the actual state of the
device, and it always starts in laptop mode. Hence, it should be started when
the device is in its laptop state.

Palm rejection disables the touchscreen when a stylus is active in order to
avoid conflicts between pen and touch input.

In graphical mode, controls are provided for the following tasks:
- enabling/disabling device state monitoring and palm rejection
- manually activating laptop or tablet mode.
- changing display orientation (with touchscreen and stylus mapping following
  consistently),
- enabling/disabling touchscreen, touchpad, and nipple,
