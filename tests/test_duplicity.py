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


class DuplicityBackupTests(unittest.TestCase):
    def test_is_valid(self):
        p = Popen(
            [
                "./backup",
                "--is-valid",
                "-v",
                "./tests/duplicity.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        self.assertEqual(stdout, "XML file ./tests/duplicity.xml is valid.\n")
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
                "./tests/duplicity-invalid.xml",
            ],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 1)
        self.assertEqual(stdout, "")
        regex = (
            r"\[CRITICAL\] XML file \./tests/duplicity-invalid\.xml is not valid\.\n"
            + r"\[CRITICAL\] .+?/duplicity-invalid\.xml:6:0:ERROR:SCHEMASV:SCHEMAV_"
            + r"ELEMENT_CONTENT: Element '{https://github\.com/jnphilipp/backup/}"
            + r"exclude': This element is not expected\. Expected is \( {https://github"
            + r"\.com/jnphilipp/backup/}path \).\n"
        )
        self.assertIsNotNone(re.fullmatch(regex, stderr))

    def test_backup(self):
        p = Popen(
            ["./backup", "--dry-run", "-v", "./tests/duplicity.xml", "./BACKUPS"],
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf8",
        )
        stdout, stderr = p.communicate()
        self.assertEqual(p.returncode, 0)
        regex = (
            r"Using \'[^\']+BACKUPS\' as backup target\.\nBackup local source /\.\n"
            + r"Backup target .+?/BACKUPS/.+?/files\.\nThe following command would be "
            + r'run:\n"duplicity" "--volsize" "1024" "--full-if-older-than" "1D" '
            + r'"--exclude=\*\*/.cache" "--exclude=\*\*/venv" "--exclude=\*\*/.venv" '
            + r'"--exclude=\*\*/__pycache__" "--exclude=\*\*/.mypy_cache" '
            + r'"--include=/var" "--exclude=/var/crash" "--exclude=/var/log" '
            + r'"--exclude=/var/lock" "--exclude=/var/run" "--exclude=/var/spool" '
            + r'"--exclude=/var/tmp" "--include=/boot" "--include=/etc" '
            + r'"--include=/srv" "--include=/opt" "--include=/root" "--include=/home" '
            + r'"--exclude=\*\*" "/" "file:///.+?/BACKUPS/.+?/files"\nwith the working '
            + r"directory: None\nBackup complete\.\n"
        )
        self.assertIsNotNone(re.fullmatch(regex, stdout))
        self.assertEqual("[WARNING] The given target path does not exists.\n", stderr)


if __name__ == "__main__":
    unittest.main()
