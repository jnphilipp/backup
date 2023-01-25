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


class ScriptTests(unittest.TestCase):
    def test_is_valid(self):
        p = Popen(
            [
                "./backup",
                "--is-valid",
                "-v",
                "./tests/scripts.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout, "XML file ./tests/scripts.xml is valid.\n")
        self.assertEqual(stderr, "")

        p = Popen(
            [
                "./backup",
                "--is-valid",
                "./tests/scripts.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "")

    def test_backup(self):
        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/scripts.xml"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(
            "Running script 3.\nBacking up source /.\nRunning script 4.\nDry run done.\n",
            stdout,
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n", stderr
        )

        p = Popen(
            ["./backup", "--dry-run", "-vvv", "./tests/scripts.xml"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertIsNotNone(
            re.fullmatch(
                r"Loading XML file \"\./tests/scripts.xml\"\.\nLoading XML schema \".*?backup\.xsd\"\.\nXML file \./tests/scripts.xml is valid\.\nParsing XML element <Element {https://github.com/jnphilipp/backup/}source at 0x[\w\d]+> for source\.\nRunning script 3\.\nCommand: \"echo\" \"Hello World\"\nBacking up source /\.\nCommand: \"rsync\" \"--delete\" \"--delete-excluded\" \"--stats\" \"--backup-dir=/mnt/BACKUPS/.+?/backup\" \"-abuchvz\" \"--exclude=\*\.pyc\" \"--exclude=\*\*/\.cache\" \"--exclude=\*\*/venv\" \"--exclude=\*\*/\.venv\" \"--exclude=\*\*/__pycache__\" \"--exclude=\*\*/\.mypy_cache\" \"--exclude=\*\*/\.local/share/Trash\" \"--include=/boot/\*\*\*\" \"--include=/etc/\*\*\*\" \"--exclude=/home\" \"--exclude=/opt\" \"--exclude=/proc\" \"--include=/root/\*\*\*\" \"--exclude=/run\" \"--include=/srv/\*\*\*\" \"--exclude=/tmp\" \"--exclude=/var/\*\*/logs\" \"--exclude=/var/cache\" \"--exclude=/var/crash\" \"--exclude=/var/log\" \"--exclude=/var/lock\" \"--exclude=/var/run\" \"--exclude=/var/spool\" \"--exclude=/var/tmp\" \"--include=/var/\*\*\*\" \"--include=/var/cache/pacman/\*\*\*\" \"--exclude=\*\" \"//\" \"/mnt/BACKUPS/.+?/files\"\nEnv: None\nCwd: None\nRunning script 4.\nCommand: \"echo\" \"Goodbye!\"\nDry run done\.\n",
                stdout,
            )
        )
        self.assertEqual(
            "[WARNING] Performing dry run, no changes will be done.\n", stderr
        )


if __name__ == "__main__":
    unittest.main()
