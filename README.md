# Theia Technologies motor control board interface
Theia Technologies offers a [MCR600 motor control board](https://www.theiatech.com/lenses/accessories/mcr/) for interfacing with Theia's motorized lenses.  This board controls focus, zoom, iris, and IRC filter motors.  It can be connected to a host comptuer by USB, UART, or I2C connection.  This module allows the user to easily convert from engineering units (meters, degrees) to motor steps and automatically control the lens motors.  For the motor functionality be sure to install *TheiaMCR*.  

# Features
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> The MCR600 board has a proprietary command protocol to control and get information from the board.  The protocol is a customized string of up to 12 bytes which can be deciphered in the MCR600 documentation.  However for ease of use, Theia has developed this Python module to format the custom byte strings and send them to the board.  

# Quick start


# Functions
## Initialization functions


# License
Theia Technologies proprietary and confidential license
Copyright 2023 Theia Technologies

# Contact information
For more information contact: 
Mark Peterson at Theia Technologies
[mpeterson@theiatech.com](mailto://mpeterson@theiatech.com)

# Revision
v.1.0.19