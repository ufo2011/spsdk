#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2021-2023 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module for NXP device description classes."""


from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

from libusbsio.libusbsio import LIBUSBSIO

from spsdk.mboot.interfaces.usb import USB_DEVICES as MB_USB_DEVICES
from spsdk.sdp.interfaces.usb import USB_DEVICES as SDP_USB_DEVICES
from spsdk.utils.misc import get_hash

# for backward-compatibility
from spsdk.utils.usbfilter import NXPUSBDeviceFilter

convert_usb_path = NXPUSBDeviceFilter.convert_usb_path


class DeviceDescription(ABC):
    """Base class for all logical devices.

    The intent is to have a generic container for providing info about devices
    of any type. Thus the class is named as 'logical', because it doesn't
    allow you to control the device in any way.

    This is just a base class and as such shouldn't be used. If you want to
    use it, create your own class inheriting from this class and redefining
    the methods listed in this class!
    """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def __str__(self) -> str:
        """Should return the string from info function."""
        return self.info()

    @abstractmethod  # pragma: no cover
    def info(self) -> str:
        """Shall return a string describing the device, e.g. Name: <name>; ID: <id>."""


class UartDeviceDescription(DeviceDescription):
    """Simple container holding information about UART device.

    This container should be used instead of any USB API related objects, as
    this container will be the same all the time compared to specific UART API
    implementations.
    """

    def __init__(self, name: Optional[str] = None, dev_type: Optional[str] = None) -> None:
        """Constructor.

        The 'dev_type' can be in general any string identifying the device type.

        :param name: COM port name
        :param dev_type: 'mboot device' or 'SDP device'
        """
        self.name = name or "Unknown port"
        self.dev_type = dev_type or "Unknown device type"

    def info(self) -> str:
        """Returns a formatted device description string.

        :return: Text information about UART device.
        """
        return f"Port: {self.name}\nType: {self.dev_type}"


class USBDeviceDescription(DeviceDescription):
    """Simple container holding information about USB device.

    This container should be used instead of any USB API related objects, as
    this container will be the same all the time compared to specific USB API
    implementations.
    """

    def __init__(
        self,
        vid: int,
        pid: int,
        path: str,
        product_string: str,
        manufacturer_string: str,
        name: str,
        serial: str,
        original_path: Optional[Union[str, bytes]] = None,
    ) -> None:
        """Constructor.

        :param vid: Vendor ID
        :param pid: Product ID
        :param product_string: Product string
        :param manufacturer_string: Manufacturer string
        :param name: Name(s) of NXP devices as defined under spsdk.mboot.interfaces.usb or spsdk.sdp.interfaces.usb
        :param serial: The serial number of device.

        See :py:func:`get_usb_device_name` function to get the name from
        VID and PID.
        See :py:func:`convert_usb_path` function to provide a proper path string.
        """
        self.vid = vid
        self.pid = pid
        self.path = path
        self.product_string = product_string
        self.manufacturer_string = manufacturer_string
        self.name = name
        self.serial = serial
        self.path_hash = get_hash(original_path) if original_path else "N/A"

    def info(self) -> str:
        """Returns a formatted device description string.

        :return: Text information of USB device.
        """
        return (
            f"{self.product_string} - {self.manufacturer_string}\n"
            f"Vendor ID: 0x{self.vid:04x}\n"
            f"Product ID: 0x{self.pid:04x}\n"
            f"Path: {self.path}\n"
            f"Path Hash: {self.path_hash}\n"
            f"Name: {self.name}\n"
            f"Serial number: {self.serial}"
        )


class SIODeviceDescription(DeviceDescription):
    """Simple container holding information about LIBUSBSIO device.

    This container contains information about LIBUSBSIOdevice.
    """

    def __init__(self, info: LIBUSBSIO.HIDAPI_DEVICE_INFO_T) -> None:
        """Constructor.

        :param info: LIBUSBSIO device information class.
        """
        self._info = info
        self.pid = self._info.product_id
        self.vid = self._info.vendor_id
        self.manufacturer_string = self._info.manufacturer_string
        self.product_string = self._info.product_string
        self.path = convert_usb_path(self._info.path)
        self.serial_number = self._info.serial_number
        self.interface_number = self._info.interface_number
        self.release_number = self._info.release_number
        self.path_hash = get_hash(self._info.path)

    def info(self) -> str:
        """Returns a formatted device description string.

        :return: Text description of SIO device.
        """
        return (
            f"LIBUSBSIO - {self.manufacturer_string}, {self.product_string}\n"
            f"Vendor ID: 0x{self.vid:04x}\n"
            f"Product ID: 0x{self.pid:04x}\n"
            f"Path: {self.path}\n"
            f"Path Hash: {self.path_hash or 'N/A'}\n"
            f"Serial number: {self.serial_number}\n"
            f"Interface number: {self.interface_number}\n"
            f"Release number: {self.release_number}"
        )


def get_usb_device_name(
    vid: int, pid: int, device_names: Optional[Dict[str, Tuple[int, int]]] = None
) -> List[str]:
    """Returns 'name' device identifier based on VID/PID, from dicts.

    Searches provided dictionary for device name based on VID/PID. If the dict
    is None, the search happens on USB_DEVICES under mboot/interfaces/usb.py and
    sdphost/interfaces/usb.py

    DESIGN REMARK: this function is not part of the USBLogicalDevice, as the
    class intention is to be just a simple container. But to help the class
    to get the required inputs, this helper method has been provided.

    :param vid: Vendor ID we are interested in
    :param pid: Product ID we are interested in
    :param device_names: dict where str is device name, first int vid, second int pid

    :return: list containing device names with corresponding VID/PID
    """
    nxp_device_names = []
    if device_names is None:
        for dname, vid_pid in MB_USB_DEVICES.items():
            if vid_pid[0] == vid and vid_pid[1] == pid:
                nxp_device_names.append(dname)

        for dname, vid_pid in SDP_USB_DEVICES.items():
            if vid_pid[0] == vid and vid_pid[1] == pid:
                nxp_device_names.append(dname)
    else:
        for dname, vid_pid in device_names.items():
            if vid_pid[0] == vid and vid_pid[1] == pid:
                nxp_device_names.append(dname)

    return nxp_device_names
