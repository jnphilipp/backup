#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Copyright (C) 2019-2023 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
# backup: Easily configure and reproducibly run complex backups.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import unittest

from subprocess import Popen, PIPE


class TarBackupTests(unittest.TestCase):
    def test_is_valid(self):
        p = Popen(
            [
                "./backup",
                "--is-valid",
                "-v",
                "./tests/tar.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout, "XML file ./tests/tar.xml is valid.\n")
        self.assertEqual(stderr, "")

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "./tests/data.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "./tests/invalid.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 1)
        self.assertEqual(stdout, "")
        self.assertIsNotNone(
            re.fullmatch(
                r"\[CRITICAL\] XML file \./tests/invalid\.xml is not valid.\n\[CRITICAL\] "
                + r".+?/invalid\.xml:9:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element "
                + r"'{https://github\.com/jnphilipp/backup/}exclude': This element is not "
                + r"expected\. Expected is \( {https://github\.com/jnphilipp/backup/}path "
                + r"\).\n",
                stderr,
            )
        )

    def test_backup(self):
        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/tar.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nBacking up source /boot\.\n"
                + r"Backing up source /etc\.\nBacking up source /root\.\nBacking up source "
                + r"/var\.\nBacking up source /srv\.\nBacking up source /run/media/DATA\.\n"
                + r"Dry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n[WARNING] The "
            + "given target path does not exists.\n",
            stderr,
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/tar.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nLoading XML file \"\./tests/tar\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/tar\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nLoading XML file \"tests/data\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file tests/data\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nBacking up source /boot\.\nCommand: \"tar\" \"--create\" \"--gzip\" \"--listed-incremental=.+?/BACKUPS/.+?/files/boot/boot\.snapshot\" \"--verbose\" \"--file\" \".+?/BACKUPS/.+?/files/boot/boot\.0\.tar\.gz\" \"/boot\"\nEnv: None\nCwd: None\nBacking up source /etc\.\nCommand: \"tar\" \"--create\" \"--gzip\" \"--listed-incremental=.+?/BACKUPS/.+?/files/etc/etc\.snapshot\" \"--verbose\" \"--file\" \".+?/BACKUPS/.+?/files/etc/etc\.0\.tar\.gz\" \"/etc\"\nEnv: None\nCwd: None\nBacking up source /root\.\nCommand: \"tar\" \"--create\" \"--gzip\" \"--listed-incremental=.+?/BACKUPS/.+?/files/root/root\.snapshot\" \"--verbose\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/\.dbus\" \"--exclude=\*\*/\.gvfs\" \"--file\" \".+?/BACKUPS/.+?/files/root/root\.0\.tar\.gz\" \"/root\"\nEnv: None\nCwd: None\nBacking up source /var\.\nCommand: \"tar\" \"--create\" \"--gzip\" \"--listed-incremental=.+?/BACKUPS/.+?/files/var/var\.snapshot\" \"--verbose\" \"--exclude=/crash\" \"--exclude=/tmp\" \"--exclude=/log\" \"--exclude=/spool\" \"--file\" \".+?/BACKUPS/.+?/files/var/var\.0\.tar\.gz\" \"/var\"\nEnv: None\nCwd: None\nBacking up source /srv\.\nCommand: \"tar\" \"--create\" \"--gzip\" \"--listed-incremental=.+?/BACKUPS/.+?/files/srv/srv\.snapshot\" \"--verbose\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \"--file\" \".+?/BACKUPS/.+?/files/srv/srv\.0\.tar\.gz\" \"/srv\"\nEnv: None\nCwd: None\nBacking up source /run/media/DATA\.\nCommand: \"tar\" \"--create\" \"--gzip\" \"--listed-incremental=.+?/BACKUPS/.+?/files/run/media/DATA/DATA\.snapshot\" \"--verbose\" \"--exclude=/\.Trash-1000\" \"--file\" \".+?/BACKUPS/.+?/files/run/media/DATA/DATA\.0\.tar\.gz\" \"/run/media/DATA\"\nEnv: None\nCwd: None\nDry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n[WARNING] The "
            + "given target path does not exists.\n",
            stderr,
        )


if __name__ == "__main__":
    unittest.main()
