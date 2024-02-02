#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2021-2024 NXP
#
# SPDX-License-Identifier: BSD-3-Clause
""" Tests for Debug Probe utilities."""
import pytest

import spsdk.debuggers.debug_probe as DP
from spsdk.debuggers.debug_probe import DebugProbes, ProbeDescription, SPSDKProbeNotFoundError
from spsdk.debuggers.utils import get_connected_probes, select_probe
from tests.debuggers.debug_probe_virtual import DebugProbeVirtual


def test_debugprobes_discovery():
    """Test of Debug Probe Utilities - Discovery probes."""
    probe_list = get_connected_probes("virtual", DebugProbeVirtual.UNIQUE_SERIAL)

    assert probe_list.pop().description == "Special virtual debug probe used for product testing"

    probe_list = get_connected_probes("virtual", DebugProbeVirtual.UNIQUE_SERIAL, {"exc": None})
    assert len(probe_list) == 0


def test_debugprobes_get_probe():
    """Test of Debug Probe Utilities - Get probe."""
    probe_list = get_connected_probes("virtual", DebugProbeVirtual.UNIQUE_SERIAL)

    probe = select_probe(probe_list).get_probe()
    assert isinstance(probe, DebugProbeVirtual)

    with pytest.raises(DP.SPSDKDebugProbeError):
        assert select_probe(probe_list).get_probe({"exc": None}) is None


def test_debugprobes_select_probe():
    """Test of Debug Probe Utilities - Select probe."""
    probe_list = DebugProbes()

    with pytest.raises(SPSDKProbeNotFoundError):
        select_probe(probe_list, silent=True)

    with pytest.raises(SPSDKProbeNotFoundError):
        select_probe(probe_list, silent=False)

    probe_description = ProbeDescription(
        "virtual", DebugProbeVirtual.UNIQUE_SERIAL, "Virtual Probe", DebugProbeVirtual
    )
    probe_list.append(probe_description)

    assert select_probe(probe_list, silent=True) == probe_description
    assert select_probe(probe_list, silent=False) == probe_description
