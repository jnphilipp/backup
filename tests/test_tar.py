#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Copyright (C) 2019-2022 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
# backup: Python wrapper for rsync.
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
        self.assertEqual(stdout, "XML file ./tests/data.xml is valid.\n")
        self.assertEqual(stderr, "")

    def test_backup(self):
        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/tar.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        regex = (
            r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Override backup target "
            + r".*?/BACKUPS\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup "
            + r"local source /boot\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "
            + r"Backup target .*?/BACKUPS/.*?/files\.\n\d{4}-\d\d-\d\d "
            + r'\d\d:\d\d:\d\d,\d{3} \[INFO\] "sudo" "tar" "--create" "--gzip" '
            + r'"--listed-incremental=.*?/BACKUPS/.*?/files/boot\.snapshot" "--verbose"'
            + r' "--file" ".*?/BACKUPS/.*?/files/boot\.0\.tar\.gz" "/boot"\n'
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n"
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local source "
            + r"/etc\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup target "
            + r".*?/BACKUPS/.*?/files\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "
            + r'"sudo" "tar" "--create" "--gzip" "--listed-incremental=.*?/BACKUPS/.*?/'
            + r'files/etc\.snapshot" "--verbose" "--file" ".*?/BACKUPS/.*?/files/'
            + r'etc\.0\.tar\.gz" "/etc"\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] '
            + r"cwd=None\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local "
            + r"source /root\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup "
            + r"target .*?/BACKUPS/.*?/files\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} "
            + r'\[INFO\] "sudo" "tar" "--create" "--gzip" "--listed-incremental=.*?/'
            + r'BACKUPS/.*?/files/root\.snapshot" "--verbose" ("--exclude=\*\*/\.gvfs" '
            + r'|"--exclude=\*\*/\.cache" |"--exclude=\*\*/\.dbus" )+"--file" '
            + r'".*?/BACKUPS/.*?/files/root\.0\.tar\.gz" "/root"\n\d{4}-\d\d-\d\d '
            + r"\d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n\d{4}-\d\d-\d\d "
            + r"\d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local source /var\.\n"
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup target "
            + r".*?/BACKUPS/.*?/files\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "
            + r'"sudo" "tar" "--create" "--gzip" "--listed-incremental=.*?/BACKUPS/.*?'
            + r'/files/var\.snapshot" "--verbose" ("--exclude=/crash" |"--exclude=/tmp"'
            + r' |"--exclude=/spool" |"--exclude=/log" )+"--file" ".*?/BACKUPS/.*?/'
            + r'files/var\.0\.tar\.gz" "/var"\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} '
            + r"\[INFO\] cwd=None\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "
            + r"Backup local source /srv\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} "
            + r"\[INFO\] Backup target .*?/BACKUPS/.*?/files\.\n\d{4}-\d\d-\d\d "
            + r'\d\d:\d\d:\d\d,\d{3} \[INFO\] "sudo" "tar" "--create" "--gzip" '
            + r'"--listed-incremental=.*?/BACKUPS/.*?/files/srv\.snapshot" "--verbose" '
            + r'("--exclude=\*\*/venv" |"--exclude=\*\*/__pycache__" |'
            + r'"--exclude=\*\*/\.mypy_cache" |"--exclude=\*\*/\.venv" )+"--file" '
            + r'".*?/BACKUPS/.*?/files/srv\.0\.tar\.gz" "/srv"\n\d{4}-\d\d-\d\d '
            + r"\d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n\d{4}-\d\d-\d\d "
            + r"\d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local source /run/media/DATA\.\n"
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup target .+?/BACKUPS"
            + r'/.+?/files/run\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "sudo" '
            + r'"tar" "--create" "--gzip" "--listed-incremental=.+?/BACKUPS/.+?/files/'
            + r'run/media\.snapshot" "--verbose" "--exclude=/\.Trash-1000" "--file" '
            + r'".+?/BACKUPS/.+?/files/run/media\.0\.tar\.gz" "/run/media/DATA"\n'
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n\d{4}-\d\d-\d\d"
            + r" \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup complete\.\n"
        )
        self.assertIsNotNone(re.fullmatch(regex, stdout))
        self.assertEqual("", stderr)


if __name__ == "__main__":
    unittest.main()
