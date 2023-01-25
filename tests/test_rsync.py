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


class RsyncBackupTests(unittest.TestCase):
    def test_is_valid(self):
        p = Popen(
            [
                "./backup",
                "--is-valid",
                "-v",
                "./tests/rsync.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout, "XML file ./tests/rsync.xml is valid.\n")
        self.assertEqual(stderr, "")

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "-vvv",
                "./tests/rsync2.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Loading XML file \"\./tests/rsync2\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/rsync2\.xml is valid\.\nXML file \./tests/rsync2\.xml is valid\.\n",
                stdout,
            )
        )
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
            ["./backup", "--dry-run", "-v", "./tests/rsync.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nBacking up source /boot\.\nBacking up source /etc\.\nBacking up source /root\.\nBacking up source /var\.\nBacking up source /srv\.\nBacking up source /run/media/DATA\.\nDry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n[WARNING] The given target path does not exists.\n",
            stderr,
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/rsync.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nLoading XML file \"\./tests/rsync\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/rsync\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nLoading XML file \"tests/data\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file tests/data\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nBacking up source /boot\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup/boot\" \"-abuchvz\" \"/boot/\" \".+?/BACKUPS/.+?/files/boot\"\nEnv: None\nCwd: None\nBacking up source /etc\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup/etc\" \"-abuchvz\" \"/etc/\" \".+?/BACKUPS/.+?/files/etc\"\nEnv: None\nCwd: None\nBacking up source /root\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup/root\" \"-abuchvz\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/\.dbus\" \"--exclude=\*\*/\.gvfs\" \"/root/\" \".+?/BACKUPS/.+?/files/root\"\nEnv: None\nCwd: None\nBacking up source /var\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup/var\" \"-abuchvz\" \"--exclude=/crash\" \"--exclude=/tmp\" \"--exclude=/log\" \"--exclude=/spool\" \"/var/\" \".+?/BACKUPS/.+?/files/var\"\nEnv: None\nCwd: None\nBacking up source /srv\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup/srv\" \"-abuchvz\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \"/srv/\" \".+?/BACKUPS/.+?/files/srv\"\nEnv: None\nCwd: None\nBacking up source /run/media/DATA\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup/run/media/DATA\" \"-abuchvz\" \"--exclude=/.Trash-1000\" \"/run/media/DATA/\" \".+?/BACKUPS/.+?/files/run/media/DATA\"\nEnv: None\nCwd: None\nDry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n[WARNING] The given target path does not exists.\n",
            stderr,
        )

        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/rsync2.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nBacking up source /\.\nDry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n[WARNING] The given target path does not exists.\n",
            stderr,
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/rsync2.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nLoading XML file \"\./tests/rsync2\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/rsync2\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nBacking up source /\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=.+?/BACKUPS/.+?/backup\" \"-abuchvz\" \"--exclude=\*\.pyc\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \"--exclude=\*\*/\.local/share/Trash\" \"--include=/boot/\*\*\*\" \"--include=/etc/\*\*\*\" \"--exclude=/home\" \"--exclude=/opt\" \"--exclude=/proc\" \"--include=/root/\*\*\*\" \"--exclude=/run\" \"--include=/srv/\*\*\*\" \"--exclude=/tmp\" \"--exclude=/var/\*\*/logs\" \"--exclude=/var/cache\" \"--exclude=/var/crash\" \"--exclude=/var/log\" \"--exclude=/var/lock\" \"--exclude=/var/run\" \"--exclude=/var/spool\" \"--exclude=/var/tmp\" \"--include=/var/\*\*\*\" \"--include=/var/cache/pacman/\*\*\*\" \"--exclude=\*\" \"//\" \".+?/BACKUPS/.+?/files\"\nEnv: None\nCwd: None\nDry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n[WARNING] The "
            "given target path does not exists.\n",
            stderr,
        )


if __name__ == "__main__":
    unittest.main()
