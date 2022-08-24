#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# Copyright (C) 2019-2022 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>
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

from pathlib import Path
from subprocess import Popen, PIPE


class RsyncBackupTests(unittest.TestCase):
    def test_is_valid(self):
        p = Popen(
            [
                "./backup",
                "--is-valid",
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
        Path("./BACKUPS").mkdir()
        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/rsync.xml", "./BACKUPS"],
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
            + r"Backup target .*?/BACKUPS/.*?/files/boot\.\n\d{4}-\d\d-\d\d "
            + r'\d\d:\d\d:\d\d,\d{3} \[INFO\] "sudo" "rsync" "--delete" '
            + r'"--delete-excluded" "--stats" "--backup-dir=.*?/BACKUPS/.*?/backup/'
            + r'boot" "-abuchPpzz" "/boot/" ".*?/BACKUPS/.*?/files/boot"\n'
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n\d{4}-\d\d-\d\d"
            + r" \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local source /etc\.\n"
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup target "
            + r".*?/BACKUPS/.*?/files/etc\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} "
            + r'\[INFO\] "sudo" "rsync" "--delete" "--delete-excluded" "--stats" '
            + r'"--backup-dir=.*?/BACKUPS/.*?/backup/etc" "-abuchPpzz" "/etc/" '
            + r'".*?/BACKUPS/.*?/files/etc"\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} '
            + r"\[INFO\] cwd=None\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup"
            + r" local source /root\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "
            + r"Backup target .*?/BACKUPS/.*?/files/root\.\n\d{4}-\d\d-\d\d "
            + r'\d\d:\d\d:\d\d,\d{3} \[INFO\] "sudo" "rsync" "--delete" '
            + r'"--delete-excluded" "--stats" "--backup-dir=.*?/BACKUPS/.*?/backup/'
            + r'root" "-abuchPpzz" ("--exclude=\*\*/\.gvfs" |"--exclude=\*\*/\.cache" '
            + r'|"--exclude=\*\*/\.dbus" )+"/root/" ".*?/BACKUPS/.*?/files/root"\n'
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n\d{4}-\d\d-\d\d"
            + r" \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local source /var\.\n"
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup target "
            + r".*?/BACKUPS/.*?/files/var\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} "
            + r'\[INFO\] "sudo" "rsync" "--delete" "--delete-excluded" "--stats" '
            + r'"--backup-dir=.*?/BACKUPS/.*?/backup/var" "-abuchPpzz" '
            + r'("--exclude=/tmp" |"--exclude=/spool" |"--exclude=/log" |'
            + r'"--exclude=/crash" )+"/var/" ".*?/BACKUPS/.*?/files/var"\n'
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] cwd=None\n\d{4}-\d\d-\d\d"
            + r" \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup local source /srv\.\n"
            + r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup target "
            + r".*?/BACKUPS/.*?/files/srv\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} "
            + r'\[INFO\] "sudo" "rsync" "--delete" "--delete-excluded" "--stats" '
            + r'"--backup-dir=.*?/BACKUPS/.*?/backup/srv" "-abuchPpzz" '
            + r'("--exclude=\*\*/\.mypy_cache" |"--exclude=\*\*/venv" |'
            + r'"--exclude=\*\*/\.venv" |"--exclude=\*\*/__pycache__" )+"/srv/" '
            + r'".*?/BACKUPS/.*?/files/srv"\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} '
            + r"\[INFO\] cwd=None\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] Backup"
            + r" local source /run/media/DATA\.\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} "
            + r"\[INFO\] Backup target .+?/BACKUPS/.+?/files/run/media\.\n"
            + r'\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "sudo" "rsync" "--delete"'
            + r' "--delete-excluded" "--stats" "--backup-dir=.+?/BACKUPS/.+?/backup/'
            + r'run/media" "-abuchPpzz" "--exclude=/\.Trash-1000" "/run/media/DATA" '
            + r'".+?/BACKUPS/.+?/files/run/media"\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3}'
            + r" \[INFO\] cwd=None\n\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d{3} \[INFO\] "
            + r"Backup complete\.\n"
        )
        self.assertIsNotNone(re.fullmatch(regex, stdout))
        self.assertEqual("", stderr)


if __name__ == "__main__":
    unittest.main()
