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
                r"Using '[^\']+/BACKUPS' as backup target\.\nBacking up source /\.\nDry run done\.\n",
                stdout,
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                r"\[WARNING\] Performing dry run, no changes will be done\.\n\[WARNING\] The given target path does not exists\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files, initializing it\.\n",
                stderr,
            )
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/borg.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '[^\']+/BACKUPS' as backup target\.\nLoading XML file \"\./tests/borg\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/borg\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/yoga-c940/files\"\nEnv: None\nCwd: None\nBacking up source /\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--filter=AMUCE\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \"--exclude=\*\.pyc\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \"--pattern=\+boot\" \"--pattern=\+etc\" \"--pattern=\+home\" \"--pattern=\+opt\" \"--pattern=!proc\" \"--pattern=\+root\" \"--pattern=\+srv\" \"--pattern=!tmp\" \"--pattern=-var/\*\*/logs\" \"--pattern=-pp:var/cache\" \"--pattern=-pp:var/crash\" \"--pattern=-pp:var/log\" \"--pattern=-pp:var/lock\" \"--pattern=-pp:var/run\" \"--pattern=-pp:var/spool\" \"--pattern=-pp:var/tmp\" \"--pattern=\+var\" \"--pattern=\+var/cache/pacman\" \"--pattern=-\*\*\" \".+?/BACKUPS/.+?/files::{hostname}-{now}\" \"/\"\nEnv: None\nCwd: None\nDry run done.\n",
                stdout,
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                r"\[WARNING\] Performing dry run, no changes will be done\.\n\[WARNING\] The given target path does not exists\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files, initializing it\.\n",
                stderr,
            )
        )

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
                r"Using '[^\']+/BACKUPS' as backup target\.\nBacking up source /boot\.\nBacking up source /etc\.\nBacking up source /home\.\nBacking up source /opt\.\nBacking up source /root\.\nBacking up source /srv\.\nBacking up source /var\.\nDry run done\.\n",
                stdout,
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                r"\[WARNING\] Performing dry run, no changes will be done\.\n\[WARNING\] The given target path does not exists\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/boot, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/etc, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/home, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/opt, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/root, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/srv, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/var, initializing it\.\n",
                stderr,
            )
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/borg2.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using \'.+?/BACKUPS\' as backup target\.\nLoading XML file \"\./tests/borg2\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/borg2\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/boot\"\nEnv: None\nCwd: None\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/etc\"\nEnv: None\nCwd: None\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/home\"\nEnv: None\nCwd: None\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/opt\"\nEnv: None\nCwd: None\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/root\"\nEnv: None\nCwd: None\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/srv\"\nEnv: None\nCwd: None\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/.+?/files/var\"\nEnv: None\nCwd: None\nBacking up source /boot\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \".+?/BACKUPS/.+?/files/boot::{hostname}:boot-{now}\" \"/boot\"\nEnv: None\nCwd: None\nBacking up source /etc\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \".+?/BACKUPS/.+?/files/etc::{hostname}:etc-{now}\" \"/etc\"\nEnv: None\nCwd: None\nBacking up source /home\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \"--exclude=\*\.pyc\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \".+?/BACKUPS/.+?/files/home::{hostname}:home-{now}\" \"/home\"\nEnv: None\nCwd: None\nBacking up source /opt\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \".+?/BACKUPS/.+?/files/opt::{hostname}:opt-{now}\" \"/opt\"\nEnv: None\nCwd: None\nBacking up source /root\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \".+?/BACKUPS/.+?/files/root::{hostname}:root-{now}\" \"/root\"\nEnv: None\nCwd: None\nBacking up source /srv\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \".+?/BACKUPS/.+?/files/srv::{hostname}:srv-{now}\" \"/srv\"\nEnv: None\nCwd: None\nBacking up source /var\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \"--exclude=var/\*\*/logs\" \"--exclude=pp:var/cache\" \"--exclude=pp:var/crash\" \"--exclude=pp:var/log\" \"--exclude=pp:var/lock\" \"--exclude=pp:var/run\" \"--exclude=pp:var/spool\" \"--exclude=pp:var/tmp\" \"--pattern=\+var/cache/pacman\" \".+?/BACKUPS/.+?/files/var::{hostname}:var-{now}\" \"/var\"\nEnv: None\nCwd: None\nDry run done\.\n",
                stdout,
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                r"\[WARNING\] Performing dry run, no changes will be done\.\n\[WARNING\] The given target path does not exists\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/boot, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/etc, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/home, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/opt, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/root, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/srv, initializing it\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/.+?/files/var, initializing it\.\n",
                stderr,
            )
        )

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
                r"Using '[^\']+/BACKUPS' as backup target\.\nBacking up source / mounted from USER@SERVER\.\nDry run done\.\n",
                stdout,
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                r"\[WARNING\] Performing dry run, no changes will be done\.\n\[WARNING\] The given target path does not exists\.\n\[WARNING\] No borg repository found in .+?/backup/BACKUPS/SERVER/files, initializing it\.\n",
                stderr,
            )
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/borg-remote.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Using '.+?/BACKUPS' as backup target\.\nLoading XML file \"\./tests/borg-remote\.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/borg-remote\.xml is valid\.\nParsing XML element <Element {https://github\.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nCommand: \"borg\" \"init\" \"--encryption\" \"repokey\" \".+?/BACKUPS/SERVER/files\"\nEnv: None\nCwd: None\nBacking up source / mounted from USER@SERVER\.\nCommand: \"borg\" \"create\" \"--verbose\" \"--list\" \"--stats\" \"--show-rc\" \"--compression\" \"zstd,11\" \"--exclude-caches\" \"--exclude=\*\.pyc\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \"--pattern=\+boot\" \"--pattern=\+etc\" \"--pattern=\+home\" \"--pattern=\+opt\" \"--pattern=!pp:proc\" \"--pattern=\+root\" \"--pattern=\+srv\" \"--pattern=!pp:tmp\" \"--pattern=!pp:usr\" \"--pattern=-var/\*\*/logs\" \"--pattern=-pp:var/cache\" \"--pattern=-pp:var/crash\" \"--pattern=-pp:var/log\" \"--pattern=-pp:var/lock\" \"--pattern=-pp:var/run\" \"--pattern=-pp:var/spool\" \"--pattern=-pp:var/tmp\" \"--pattern=\+var\" \"--pattern=\+var/cache/debconf\" \"--pattern=-\*\*\" \".+?/BACKUPS/SERVER/files::SERVER-{now}\" \"\.\"\nEnv: None\nCwd: TEMPDIR\nDry run done\.\n",
                stdout,
            )
        )
        self.assertIsNotNone(
            re.fullmatch(
                r"\[WARNING\] Performing dry run, no changes will be done\.\n\[WARNING\] The given target path does not exists\.\n\[WARNING\] No borg repository found in .+?/BACKUPS/SERVER/files, initializing it\.\n",
                stderr,
            )
        )


if __name__ == "__main__":
    unittest.main()
