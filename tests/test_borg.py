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


class BorgBackupTests(unittest.TestCase):
    def test_is_valid(self):
        p = Popen(
            [
                "./backup",
                "--is-valid",
                "-v",
                "./tests/borg.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual("XML file ./tests/borg.xml is valid.\n", stdout)
        self.assertEqual("", stderr)

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "./tests/borg2.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual("", stdout)
        self.assertEqual("", stderr)

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "./tests/borg-remote.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual("", stdout)
        self.assertEqual("", stderr)

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "./tests/borg-invalid.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 1)
        self.assertEqual("", stdout)
        self.assertEqual(
            "[CRITICAL] XML file ./tests/borg-invalid.xml is not valid.\n[CRITICAL] "
            + "Borg does not support include, use pattern.\n",
            stderr,
        )

    def test_backup(self):
        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/borg.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using \'[^\']+/BACKUPS\' as backup target\.\nBackup local source /\.\n"
                + r"Backup target .+?/BACKUPS/.+?/files\.\nThe following command would be "
                + r'run:\n"borg" "create" "--verbose" "--filter=AMUCE" "--list" "--stats" '
                + r'"--show-rc" "--compression" "zstd,11" "--exclude-caches" '
                + r'"--exclude=\*\.pyc" "--exclude=\*\*/\.cache" "--exclude=\*\*/venv" '
                + r'"--exclude=\*\*/\.venv" "--exclude=\*\*/__pycache__" '
                + r'"--exclude=\*\*/\.mypy_cache" "--pattern=\+boot" "--pattern=\+etc" '
                + r'"--pattern=\+home" "--pattern=\+opt" "--pattern=!proc" '
                + r'"--pattern=\+root" "--pattern=\+srv" "--pattern=!tmp" '
                + r'"--pattern=-var/\*\*/logs" "--pattern=-pp:var/cache" '
                + r'"--pattern=-pp:var/crash" "--pattern=-pp:var/log" '
                + r'"--pattern=-pp:var/lock" "--pattern=-pp:var/run" '
                + r'"--pattern=-pp:var/spool" "--pattern=-pp:var/tmp" "--pattern=\+var" '
                + r'"--pattern=\+var/cache/pacman" "--pattern=-\*\*" '
                + r'".+?/BACKUPS/.+?/files::{hostname}-{now}" "/"\nwith the working '
                + r"directory: None\nBackup complete.\n",
                stdout,
            )
        )
        self.assertEqual("[WARNING] The given target path does not exists.\n", stderr)

        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/borg2.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using \'[^\']+/BACKUPS\' as backup target\.\nBackup local source /boot\."
                + r"\nBackup target .+?/BACKUPS/.+?/files\.\nThe following command would be"
                + r' run:\n"borg" "create" "--verbose" "--list" "--stats" "--show-rc" '
                + r'"--compression" "zstd,11" "--exclude-caches" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:boot-{now}" "/boot"\nwith the '
                + r"working directory: None\nBackup local source /etc\.\nBackup target "
                + r'.+?/BACKUPS/.+?/files\.\nThe following command would be run:\n"borg" '
                + r'"create" "--verbose" "--list" "--stats" "--show-rc" "--compression" '
                + r'"zstd,11" "--exclude-caches" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:etc-{now}" "/etc"\nwith the working '
                + r"directory: None\nBackup local source /home\.\nBackup target "
                + r'.+?/BACKUPS/.+?/files\.\nThe following command would be run:\n"borg" '
                + r'"create" "--verbose" "--list" "--stats" "--show-rc" "--compression" '
                + r'"zstd,11" "--exclude-caches" "--exclude=\*\.pyc" '
                + r'"--exclude=\*\*/\.cache" "--exclude=\*\*/venv" "--exclude=\*\*/\.venv" '
                + r'"--exclude=\*\*/__pycache__" "--exclude=\*\*/\.mypy_cache" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:home-{now}" "/home"\nwith the '
                + r"working directory: None\nBackup local source /opt\.\nBackup target "
                + r'.+?/BACKUPS/.+?/files\.\nThe following command would be run:\n"borg" '
                + r'"create" "--verbose" "--list" "--stats" "--show-rc" "--compression" '
                + r'"zstd,11" "--exclude-caches" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:opt-{now}" "/opt"\nwith the working '
                + r"directory: None\nBackup local source /root\.\nBackup target "
                + r'.+?/BACKUPS/.+?/files\.\nThe following command would be run:\n"borg" '
                + r'"create" "--verbose" "--list" "--stats" "--show-rc" "--compression" '
                + r'"zstd,11" "--exclude-caches" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:root-{now}" "/root"\nwith the '
                + r"working directory: None\nBackup local source /srv\.\nBackup target "
                + r'.+?/BACKUPS/.+?/files\.\nThe following command would be run:\n"borg" '
                + r'"create" "--verbose" "--list" "--stats" "--show-rc" "--compression" '
                + r'"zstd,11" "--exclude-caches" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:srv-{now}" "/srv"\nwith the working '
                + r"directory: None\nBackup local source /var\.\nBackup target "
                + r'.+?/BACKUPS/.+?/files\.\nThe following command would be run:\n"borg" '
                + r'"create" "--verbose" "--list" "--stats" "--show-rc" "--compression" '
                + r'"zstd,11" "--exclude-caches" "--exclude=var/\*\*/logs" '
                + r'"--exclude=pp:var/cache" "--exclude=pp:var/crash" '
                + r'"--exclude=pp:var/log" "--exclude=pp:var/lock" "--exclude=pp:var/run" '
                + r'"--exclude=pp:var/spool" "--exclude=pp:var/tmp" '
                + r'"--pattern=\+var/cache/pacman" '
                + r'".+?/BACKUPS/.+?/files::{hostname}:var-{now}" "/var"\nwith the working '
                + r"directory: None\nBackup complete\.\n",
                stdout,
            )
        )
        self.assertEqual("[WARNING] The given target path does not exists.\n", stderr)

        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/borg-remote.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using \'[^\']+/BACKUPS\' as backup target\.\nMounting USER@SERVER:/ into "
                + r'/tmp/backup-[\w_]+\.\nThe following command would be run:\n"sshfs" "-F"'
                + r' "/home/USER/\.ssh/config" "USER@SERVER:/" "/tmp/backup-[\w_]+"\nwith '
                + r"the working directory: None\nBackup sshfs source USER@SERVER:/\.\n"
                + r"Backup target .+?/BACKUPS/USER@SERVER/files\.\nThe following command "
                + r'would be run:\n"borg" "create" "--verbose" "--list" "--stats" '
                + r'"--show-rc" "--compression" "zstd,11" "--exclude-caches" '
                + r'"--exclude=\*\.pyc" "--exclude=\*\*/\.cache" "--exclude=\*\*/venv" '
                + r'"--exclude=\*\*/\.venv" "--exclude=\*\*/__pycache__" '
                + r'"--exclude=\*\*/\.mypy_cache" "--pattern=\+boot" "--pattern=\+etc" '
                + r'"--pattern=\+home" "--pattern=\+opt" "--pattern=!pp:proc" '
                + r'"--pattern=\+root" "--pattern=\+srv" "--pattern=!pp:tmp" '
                + r'"--pattern=!pp:usr" "--pattern=-var/\*\*/logs" '
                + r'"--pattern=-pp:var/cache" "--pattern=-pp:var/crash" '
                + r'"--pattern=-pp:var/log" "--pattern=-pp:var/lock" '
                + r'"--pattern=-pp:var/run" "--pattern=-pp:var/spool" '
                + r'"--pattern=-pp:var/tmp" "--pattern=\+var" '
                + r'"--pattern=\+var/cache/debconf" "--pattern=-\*\*" '
                + r'".+?/BACKUPS/USER@SERVER/files::USER@SERVER-{now}" "\."\nwith the '
                + r"working directory: /tmp/backup-[\w_]+\nDismounting /tmp/backup-[\w]+\."
                + r'\nThe following command would be run:\n"fusermount3" "-u" '
                + r'"/tmp/backup-[\w_]+"\nwith the working directory: None\nBackup complete'
                + r"\.\n",
                stdout,
            )
        )
        self.assertEqual("[WARNING] The given target path does not exists.\n", stderr)


if __name__ == "__main__":
    unittest.main()
