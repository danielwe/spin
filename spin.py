#!/usr/bin/env python

"""spin, a convenience utility for laptop/tablet devices running Linux.

Usage:
    spin.py
    spin.py -h | --help
    spin.py --nogui
Options:
    -h, --help     : show this help message
    --nogui        : non-GUI mode

"""


###############################################################################
#                                                                             #
# spin                                                                        #
#                                                                             #
# version: 2014-05-31T0608                                                    #
#                                                                             #
###############################################################################
#                                                                             #
# LICENSE INFORMATION                                                         #
#                                                                             #
# The program spin provides an interface for control of the usage modes of    #
# laptop-tablet and similar hybrid computer devices.                          #
#                                                                             #
# Copyright (C) 2014 Daniel Wennberg                                          #
# Copyright (C) 2013, 2014 William Breaden Madden                             #
#                                                                             #
# This software is released under the terms of the GNU General Public License #
# version 3 (GPLv3).                                                          #
#                                                                             #
# This program is free software: you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)   #
# any later version.                                                          #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for   #
# more details.                                                               #
#                                                                             #
# For a copy of the GNU General Public License, see                           #
# <http://www.gnu.org/licenses/>.                                             #
#                                                                             #
###############################################################################


from docopt import docopt
import os
import sys
import subprocess
from multiprocessing import Process
import socket
import time
from PyQt4 import QtGui
import logging

# Disable selected pylint error messages
#C0103: Invalid %s name "%s"
#C0111: Missing %s docstring
#R0904: Too many public methods (%s/%s)
#R0915: Too many statements (%s/%s)
#pylint: disable=C0103,C0111,R0904,R0915

# Enable logging
LOGGER = logging.getLogger(__name__)
logging.basicConfig()
LOGGER.level = logging.INFO


class Interface(QtGui.QWidget):
    def __init__(self, args=None):
        self.args = args
        super(Interface, self).__init__()
        LOGGER.info("running spin")
        # Prepare palm rejection
        self.stylusProximity = None
        self.previousStylusProximity = None
        self.processPalmRejection = Process(target=self.palmRejection)
        # Enable palm rejection by default
        self.palmRejectionOn()
        # Prepare device state monitoring
        self.deviceState = "laptop"
        self.processDeviceStateMonitoring = Process(
            target=self.deviceStateMonitoring)
        # Enable device state monitoring by default
        self.deviceStateMonitoringOn()
        if args["--nogui"]:
            LOGGER.info("non-GUI mode")
        else:
            self.createGUI()

    def closeEvent(self, event):
        LOGGER.info("stopping spin")
        self.palmRejectionOff()
        self.deviceStateMonitoringOff()
        self.deleteLater()

    def createGUI(self):
        # create buttons
        buttonsList = []
        # button: device state monitoring on
        newbutton = QtGui.QPushButton(
            'device state monitoring on', self)
        newbutton.clicked.connect(
            self.engageDeviceStateMonitoringOn)
        buttonsList.append(newbutton)
        # button: device state monitoring off
        newbutton = QtGui.QPushButton(
            'device state monitoring off', self)
        newbutton.clicked.connect(
            self.engageDeviceStateMonitoringOff)
        buttonsList.append(newbutton)
        # button: palm rejection on
        newbutton = QtGui.QPushButton(
            'palm rejection on', self)
        newbutton.clicked.connect(
            self.engagePalmRejectionOn)
        buttonsList.append(newbutton)
        # button: palm rejection off
        newbutton = QtGui.QPushButton(
            'palm rejection off', self)
        newbutton.clicked.connect(
            self.engagePalmRejectionOff)
        buttonsList.append(newbutton)
        # button: laptop mode
        newbutton = QtGui.QPushButton('laptop mode', self)
        newbutton.clicked.connect(self.engageModeLaptop)
        buttonsList.append(newbutton)
        # button: tablet mode
        newbutton = QtGui.QPushButton('tablet mode', self)
        newbutton.clicked.connect(self.engageModeTablet)
        buttonsList.append(newbutton)
        # button: orientation normal
        newbutton = QtGui.QPushButton('orientation normal', self)
        newbutton.clicked.connect(self.engageNormal)
        buttonsList.append(newbutton)
        # button: orientation inverted
        newbutton = QtGui.QPushButton('orientation inverted', self)
        newbutton.clicked.connect(self.engageInverted)
        buttonsList.append(newbutton)
        # button: orientation left
        newbutton = QtGui.QPushButton('orientation left', self)
        newbutton.clicked.connect(self.engageLeft)
        buttonsList.append(newbutton)
        # button: orientation right
        newbutton = QtGui.QPushButton('orientation right', self)
        newbutton.clicked.connect(self.engageRight)
        buttonsList.append(newbutton)
        # button: touchscreen on
        newbutton = QtGui.QPushButton('touchscreen on', self)
        newbutton.clicked.connect(self.engageTouchscreenOn)
        buttonsList.append(newbutton)
        # button: touchscreen off
        newbutton = QtGui.QPushButton('touchscreen off', self)
        newbutton.clicked.connect(self.engageTouchscreenOff)
        buttonsList.append(newbutton)
        # button: touchpad on
        newbutton = QtGui.QPushButton('touchpad on', self)
        newbutton.clicked.connect(self.engageTouchpadOn)
        buttonsList.append(newbutton)
        # button: touchpad off
        newbutton = QtGui.QPushButton('touchpad off', self)
        newbutton.clicked.connect(self.engageTouchpadOff)
        buttonsList.append(newbutton)
        # button: nipple on
        newbutton = QtGui.QPushButton('nipple on', self)
        newbutton.clicked.connect(self.engageNippleOn)
        buttonsList.append(newbutton)
        # button: nipple off
        newbutton = QtGui.QPushButton('nipple off', self)
        newbutton.clicked.connect(self.engageNippleOff)
        buttonsList.append(newbutton)
        # set button dimensions
        buttonsWidth = 250
        buttonsHeight = 50
        for button in buttonsList:
            button.setFixedSize(buttonsWidth, buttonsHeight)
        # set layout
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        for button in buttonsList:
            vbox.addWidget(button)
            vbox.addStretch(1)
        self.setLayout(vbox)
        # window
        self.setWindowTitle('spin')
        # set window position
        #self.move(0, 0)
        self.move(QtGui.QDesktopWidget().screenGeometry().width(), 0)
        self.show()

    def engageDeviceStateMonitoringOn(self):
        self.deviceStateMonitoringOn()

    def engageDeviceStateMonitoringOff(self):
        self.deviceStateMonitoringOff()

    def engagePalmRejectionOn(self):
        self.palmRejectionOn()

    def engagePalmRejectionOff(self):
        self.palmRejectionOff()

    def engageModeLaptop(self):
        self.deviceState = "laptop"
        self.displayNormal()
        self.touchscreenNormal()
        self.touchscreenOn()
        self.touchpadOn()
        self.nippleOn()

    def engageModeTablet(self):
        self.deviceState = "tablet"
        self.displayNormal()
        self.touchscreenNormal()
        self.touchscreenOn()
        self.touchpadOff()
        self.nippleOff()

    def engageNormal(self):
        self.displayNormal()
        self.touchscreenNormal()

    def engageInverted(self):
        self.displayInverted()
        self.touchscreenInverted()

    def engageLeft(self):
        self.displayLeft()
        self.touchscreenLeft()

    def engageRight(self):
        self.displayRight()
        self.touchscreenRight()

    def engageTouchscreenOn(self):
        self.touchscreenOn()

    def engageTouchscreenOff(self):
        self.touchscreenOff()

    def engageTouchpadOn(self):
        self.touchpadOn()

    def engageTouchpadOff(self):
        self.touchpadOff()

    def engageNippleOn(self):
        self.nippleOn()

    def engageNippleOff(self):
        self.nippleOff()

    def deviceStateMonitoring(self):
        acpi_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        acpi_socket.connect("/var/run/acpid.socket")
        acpi_triggerevents = ['ibm/hotkey HKEY 00000080 000060c0\n',
                              'ibm/hotkey LEN0068:00 00000080 000060c0\n']
        LOGGER.info("device state is {a1}".format(a1=self.deviceState))
        while True:
            acpi_event = acpi_socket.recv(4096)
            if acpi_event in acpi_triggerevents:
                LOGGER.info("device state change")
                if self.deviceState == "laptop":
                    self.engageModeTablet()
                elif self.deviceState == "tablet":
                    self.engageModeLaptop()
                LOGGER.info("device state is {a1}".format(a1=self.deviceState))
            time.sleep(0.25)

    def deviceStateMonitoringOn(self):
        if not self.processDeviceStateMonitoring.is_alive():
            LOGGER.info("changing device state monitoring to on")
            self.processDeviceStateMonitoring.start()

    def deviceStateMonitoringOff(self):
        if self.processDeviceStateMonitoring.is_alive():
            LOGGER.info("changing device state monitoring to off")
            self.processDeviceStateMonitoring.terminate()
            self.processDeviceStateMonitoring = Process(
                target=self.deviceStateMonitoring)

    def palmRejection(self):
        while True:
            stylusProximityCommand = ('xinput query-state '
                                      '"Wacom ISDv4 EC Pen stylus" | '
                                      'grep Proximity | cut -d " " -f3 | '
                                      'cut -d "=" -f2')
            self.stylusProximity = subprocess.check_output(
                stylusProximityCommand, shell=True).lower().rstrip()
            if (self.stylusProximity == "out" and
               self.previousStylusProximity != "out"):
                LOGGER.info("stylus inactive")
                self.touchscreenOn()
            elif (self.stylusProximity == "in" and
                  self.previousStylusProximity != "in"):
                LOGGER.info("stylus active")
                self.touchscreenOff()
            self.previousStylusProximity = self.stylusProximity
            time.sleep(0.25)

    def palmRejectionOn(self):
        if not self.processPalmRejection.is_alive():
            LOGGER.info("changing palm rejection to on")
            self.processPalmRejection.start()

    def palmRejectionOff(self):
        if self.processPalmRejection.is_alive():
            LOGGER.info("changing palm rejection to off")
            self.processPalmRejection.terminate()
            self.processPalmRejection = Process(target=self.palmRejection)

    def displayNormal(self):
        LOGGER.info("changing display orientation to normal")
        os.system('xrandr -o normal')

    def displayInverted(self):
        LOGGER.info("changing display orientation to inverted")
        os.system('xrandr -o inverted')

    def displayLeft(self):
        LOGGER.info("changing display orientation to left")
        os.system('xrandr -o left')

    def displayRight(self):
        LOGGER.info("changing display orientation to right")
        os.system('xrandr -o right')

    def touchscreenNormal(self):
        LOGGER.info("changing touchscreen orientation to normal")
        os.system('xinput set-prop "ELAN Touchscreen" '
                  '"Coordinate Transformation Matrix" 1 0 0 0 1 0 0 0 1')

    def touchscreenInverted(self):
        LOGGER.info("changing touchscreen orientation to inverted")
        os.system('xinput set-prop "ELAN Touchscreen" '
                  '"Coordinate Transformation Matrix" -1 0 1 0 -1 1 0 0 1')

    def touchscreenLeft(self):
        LOGGER.info("changing touchscreen orientation to left")
        os.system('xinput set-prop "ELAN Touchscreen" '
                  '"Coordinate Transformation Matrix" 0 -1 1 1 0 0 0 0 1')

    def touchscreenRight(self):
        LOGGER.info("changing touchscreen orientation to right")
        os.system('xinput set-prop "ELAN Touchscreen" '
                  '"Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1')

    def touchscreenOn(self):
        LOGGER.info("changing touchscreen to on")
        os.system('xinput enable "ELAN Touchscreen"')

    def touchscreenOff(self):
        LOGGER.info("changing touchscreen to off")
        os.system('xinput disable "ELAN Touchscreen"')

    def touchpadOn(self):
        LOGGER.info("changing touchpad to on")
        os.system('xinput enable "SynPS/2 Synaptics TouchPad"')

    def touchpadOff(self):
        LOGGER.info("changing touchpad to off")
        os.system('xinput disable "SynPS/2 Synaptics TouchPad"')

    def nippleOn(self):
        LOGGER.info("changing nipple to on")
        os.system('xinput enable "TPPS/2 IBM TrackPoint"')

    def nippleOff(self):
        LOGGER.info("changing nipple to off")
        os.system('xinput disable "TPPS/2 IBM TrackPoint"')


def main(args):
    application = QtGui.QApplication(sys.argv)
    Interface(args)
    sys.exit(application.exec_())


if __name__ == '__main__':
    main(docopt(__doc__))
