====================
sdphost - User Guide
====================

This document describes the usage of *Serial Download Procotol* Host (*sdphost*), a PC host application. 

The *sdphost* tool is a useful tool in thefactory programming and manufacturing process. It can be used to test and develop the automation software and test setups. It can be invoked from other applications too. 

This document introduces the serial download protocol, typical factory programming setup, and usage of the tool and description of its command line interface. It also provides a set of example usages of *sdphost* tool and its command line arguments with a device.

-----------------------
Communication - sdphost
-----------------------

The *sdphost* tool provides a command line interface to send *serial download protocol* commands to NXP’s i.MX RT devices enumerated on the host PC via USB-HID or UART device. 

ROM code is running on the device in serial download mode. 

------------------------
Serial Download Protocol
------------------------

*Serial Download Protocol* is a set of commands supported by NXP’s i.MX RT devices in the Boot ROM application’s serial download mode. 

See Section 8.9.9 i.MX RT1050 Processor Reference Manual for protocol details. 

The *sdphost* tool provides the user with a simple and user-friendly command-line interface. The purpose of *serial download protocol* is to provide means to download bootable images from a PC to the device’s internal or external RAM memory. There are a set of commands to read and write to a memory/register unit, read status of the last command, download images to a given address in internal/external memory, and provide the address to jump and execute the downloaded image.

-------------
Typical setup
-------------

The *sdphost* tool is used in the development phase of the device firmware application, manufacturing, and factory programming process. The release package consists of all three binaries in the respective Operating System folders. Test setup would typically be the device connected to PC Host via USB or UART. The *sdphost* tool would run on the PC host, and the device would run in *Boot ROM serial download mode*. The MCU has BOOT_MODE pins that can be used to boot the device in *serial downloader mode*. The device’s reference manual provides the documentation on booting the device in *serial downloader mode*. 

See Section 8.9 i.MX RT1050 Processor ReferenceManual for setup details

------------------
Commands - sdphost
------------------

.. click:: spsdk.apps.sdphost:main
    :prog: sdphost

.. click:: spsdk.apps.sdphost:read_register
    :prog: read-register

.. click:: spsdk.apps.sdphost:write_register
    :prog: write-register

.. click:: spsdk.apps.sdphost:write_file
    :prog: write-file

.. click:: spsdk.apps.sdphost:error_status
    :prog: error-status

.. click:: spsdk.apps.sdphost:jump_address
    :prog: jump-address


