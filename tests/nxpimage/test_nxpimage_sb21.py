#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2022-2023 NXP
#
# SPDX-License-Identifier: BSD-3-Clause

import os
from binascii import unhexlify
from itertools import zip_longest

import pytest
from click.testing import CliRunner

import spsdk.apps.nxpimage as nxpimage
from spsdk import SPSDKError
from spsdk.sbfile.sb2.images import BootImageV21
from spsdk.utils.misc import use_working_directory


@pytest.mark.parametrize(
    "bd_file,legacy_sb,external",
    [
        (
            "sb_sources/BD_files/real_example1.bd",
            "sb_sources/SB_files/legacy_real_example1.sb",
            [],
        ),
        (
            "sb_sources/BD_files/real_example2.bd",
            "sb_sources/SB_files/legacy_real_example2.sb",
            [
                "sb_sources/output_images/tmdData.bin",
                "sb_sources/output_images/bootloaderImage.bin",
                "sb_sources/output_images/tmdImage.bin",
                "sb_sources/output_images/audioImage.bin",
            ],
        ),
        (
            "sb_sources/BD_files/simpleExample_no_sha.bd",
            "sb_sources/SB_files/legacy_elftosb_no_sha.bin",
            [],
        ),
        (
            "sb_sources/BD_files/simpleExample_sha.bd",
            "sb_sources/SB_files/legacy_elftosb_sha.bin",
            [],
        ),
    ],
)
def test_nxpimage_sb21(bd_file, legacy_sb, external, elftosb_data_dir, tmpdir):
    runner = CliRunner()
    with use_working_directory(elftosb_data_dir):
        bd_file_path = os.path.join(elftosb_data_dir, bd_file)
        out_file_path_new = os.path.join(tmpdir, "new_elf2sb.bin")
        kek_key_path = os.path.join(elftosb_data_dir, "sb_sources/keys/SBkek_PUF.txt")
        priv_key_path = os.path.join(
            elftosb_data_dir, "sb_sources/keys_and_certs/k0_cert0_2048.pem"
        )
        certificate_path = os.path.join(
            elftosb_data_dir, "sb_sources/keys_and_certs/root_k0_signed_cert0_noca.der.cert"
        )
        root_key_certificate0_path = os.path.join(
            elftosb_data_dir, "sb_sources/keys_and_certs/root_k0_signed_cert0_noca.der.cert"
        )
        root_key_certificate1_path = os.path.join(
            elftosb_data_dir, "sb_sources/keys_and_certs/root_k1_signed_cert0_noca.der.cert"
        )
        root_key_certificate2_path = os.path.join(
            elftosb_data_dir, "sb_sources/keys_and_certs/root_k2_signed_cert0_noca.der.cert"
        )
        root_key_certificate3_path = os.path.join(
            elftosb_data_dir, "sb_sources/keys_and_certs/root_k3_signed_cert0_noca.der.cert"
        )
        hash_of_hashes_output_path = os.path.join(tmpdir, "hash.bin")

        out_file_path_legacy = os.path.join(elftosb_data_dir, legacy_sb)

        cmd = f"sb21 export \
            -c {bd_file_path} \
            -o {out_file_path_new}\
            -k {kek_key_path}\
            -s {priv_key_path}\
            -S {certificate_path}\
            -R {root_key_certificate0_path}\
            -R {root_key_certificate1_path}\
            -R {root_key_certificate2_path}\
            -R {root_key_certificate3_path}\
            -h {hash_of_hashes_output_path}"
        for entry in external:
            cmd += " " + entry
        result = runner.invoke(nxpimage.main, cmd.split())
        assert result.exit_code == 0
        assert os.path.isfile(out_file_path_new)

        with open(kek_key_path) as f:
            # transform text-based KEK into bytes
            sb_kek = unhexlify(f.read())

        # read generated secure binary image (created with new elf2sb)
        with open(out_file_path_new, "rb") as f:
            sb_file_data_new = f.read()

        sb_new = BootImageV21.parse(data=sb_file_data_new, kek=sb_kek)

        # dump the info of the secure binary image generated with new elf2sb
        # Left for debugging purposes
        # with open(os.path.join(elftosb_data_dir, "SB_files/new_elf2sb_sb21_file.txt"), 'w') as sb_file_content:
        #     sb_file_content.write(sb_new.__str__())

        # read SB file generated using legacy elftosb
        with open(out_file_path_legacy, "rb") as f:
            sb_file_data_old = f.read()

        # we assume that SB File version is 2.1
        sb_old = BootImageV21.parse(data=sb_file_data_old, kek=sb_kek)

        # dump the info of the secure binary image generated with legacy elftosb
        # Left for debugging purposes
        # with open(os.path.join(elftosb_data_dir, "SB_files/old_elf2sb_sb21_file.txt"), 'w') as f:
        #     f.write(sb_old.info())

        sb_new_lines = sb_new.info().split("\n")
        sb_old_lines = sb_old.info().split("\n")

        DIGEST_LINE = 4
        TIMESTAMP_LINE = 14
        # Remove lines containing digest and timestamp, as these will always differ
        # -1 for indexing starting from 0
        del sb_new_lines[DIGEST_LINE - 1]
        # -1 for indexing starting from 0, -1 for previously removed line => -2
        del sb_new_lines[TIMESTAMP_LINE - 2]

        # -1 for indexing starting from 0
        del sb_old_lines[DIGEST_LINE - 1]
        # -1 for indexing starting from 0, -1 for previously removed line => -2
        del sb_old_lines[TIMESTAMP_LINE - 2]

        for i in zip_longest(sb_new_lines, sb_old_lines, fillvalue=None):
            assert i[0] == i[1]


def test_sb_21_invalid_parse():
    with pytest.raises(SPSDKError, match="kek cannot be empty"):
        BootImageV21.parse(data=bytes(232), kek=None)


def test_nxpimage_sbkek_cli(tmpdir):
    runner = CliRunner()
    cmd = "sb21 get-sbkek"
    result = runner.invoke(nxpimage.main, cmd.split())
    assert result.exit_code == 0

    cmd = f"sb21 get-sbkek -o {tmpdir}"
    result = runner.invoke(nxpimage.main, cmd.split())
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(tmpdir, "sbkek.bin"))
    assert os.path.isfile(os.path.join(tmpdir, "sbkek.txt"))

    test_key = "858A4A83D07C78656165CDDD3B7AF4BB20E534392E7AF99EF7C296F95205E680"

    cmd = f"sb21 get-sbkek -k {test_key} -o {tmpdir}"
    result = runner.invoke(nxpimage.main, cmd.split())
    assert result.exit_code == 0
    assert os.path.isfile(os.path.join(tmpdir, "sbkek.bin"))
    assert os.path.isfile(os.path.join(tmpdir, "sbkek.txt"))
