#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020-2023 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module for working with Protected Flash Region."""

import os

from spsdk import SPSDK_DATA_FOLDER

PFR_DATA_FOLDER: str = os.path.join(SPSDK_DATA_FOLDER, "pfr")

from .exceptions import (
    SPSDKPfrcMissingConfigError,
    SPSDKPfrConfigError,
    SPSDKPfrConfigReadError,
    SPSDKPfrError,
    SPSDKPfrRotkhIsNotPresent,
)
from .pfr import CFPA, CMPA, ROMCFG, PfrConfiguration
from .processor import Processor
from .translator import Translator
