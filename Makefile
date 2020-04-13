BASH_COMPLETION_DIR?=/usr/share/bash-completion.d
BIN_DIR?=/usr/bin
DOC_DIR?=/usr/share/doc
MAN_DIR?=/usr/share/man
SHARE_DIR?=/usr/share

ifdef VERBOSE
  Q :=
else
  Q := @
endif

install: psync psync.xsd psync.bash-completion
	apt-get install python3-lxml rsync
	$(Q)install -DM 0755 psync ${BIN_DIR}/psync
	$(Q)install -Dm 0644 psync.xsd ${SHARE_DIR}/psync/psync.xsd
	$(Q)install -Dm 0644 psync.bash-completion ${BASH_COMPLETION_DIR}/psync.bash-completion
	@echo "psync install completed."

uninstall:
	$(Q)rm -r ${SHARE_DIR}psync
	$(Q)rm ${BIN_DIR}psync
	$(Q)rm ${BASH_COMPLETION_DIR}psync.bash-completion

	@echo "psync uninstall completed."

clean:
	@rm -rf ./build

deb: build/package/DEBIAN/control
	fakeroot dpkg-deb -b build/package build/psync.deb
	lintian -Ivi --suppress-tags debian-changelog-file-missing-or-wrong-name build/psync.deb

build:
	$(Q)mkdir -p build

build/copyright: build
	@echo "Upstream-Name: psync\nSource: https://github.com/jnphilipp/psync\n\nFiles: *\nCopyright: 2019-2020 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>\nLicense: GPL-3+\n This program is free software: you can redistribute it and/or modify\n it under the terms of the GNU General Public License as published by\n the Free Software Foundation, either version 3 of the License, or\n any later version.\n\n This program is distributed in the hope that it will be useful,\n but WITHOUT ANY WARRANTY; without even the implied warranty of\n MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n GNU General Public License for more details.\n\n You should have received a copy of the GNU General Public License\n along with this program. If not, see <http://www.gnu.org/licenses/>.\n On Debian systems, the full text of the GNU General Public\n License version 3 can be found in the file\n '/usr/share/common-licenses/GPL-3'." > build/copyright
	@echo "[COPYRIGHT]\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/." > build/copyright.h2m

build/changelog: build
	@git log --oneline --no-merges --format="%h %d %ai%n    %an <%ae>%n    %s" > build/changelog
	@cat build/changelog | gzip -n9 > build/changelog.gz

build/psync.1.gz: build build/copyright
	@help2man ./psync -i build/copyright.h2m -n "Python wrapper for rsync." | gzip -n9 > build/psync.1.gz

build/package/DEBIAN: build
	@mkdir -p build/package/DEBIAN

build/package/DEBIAN/md5sums: psync psync.xsd psync.bash-completion build/copyright build/changelog build/psync.1.gz build/package/DEBIAN
	$(Q)install -Dm 0755 psync build/package"${BIN_DIR}"/psync
	$(Q)install -Dm 0644 psync.xsd build/package"${SHARE_DIR}"/psync/psync.xsd
	$(Q)install -Dm 0644 psync.bash-completion build/package"${BASH_COMPLETION_DIR}"/psync.bash-completion
	$(Q)install -Dm 0644 build/changelog.gz build/package"${DOC_DIR}"/psync/changelog.gz
	$(Q)install -Dm 0644 build/copyright build/package"${DOC_DIR}"/psync/copyright
	$(Q)install -Dm 0644 build/psync.1.gz build/package"${MAN_DIR}"/man1/psync.1.gz

	$(Q)mkdir -p build/package/DEBIAN
	$(Q)md5sum `find build/package -type f -not -path "*DEBIAN*"` > build/md5sums
	$(Q)sed -e "s/build\/package\///" build/md5sums > build/package/DEBIAN/md5sums
	$(Q)chmod 644 build/package/DEBIAN/md5sums

build/package/DEBIAN/control: build/package/DEBIAN/md5sums
	@echo "Package: psync" > build/package/DEBIAN/control
	@echo "Version: `git describe --tags | awk '{print substr($$0,2)}'`-`git log --format=%h -1`" >> build/package/DEBIAN/control
	@echo "Section: utils" >> build/package/DEBIAN/control
	@echo "Priority: optional" >> build/package/DEBIAN/control
	@echo "Architecture: all" >> build/package/DEBIAN/control
	@echo "Depends: python3 (>= 3.6), python3-lxml, rsync" >> build/package/DEBIAN/control
	@echo "Recommends: pass" >> build/package/DEBIAN/control
	@echo "Installed-Size: `du -sk build/package/usr | grep -oE "[0-9]+"`" >> build/package/DEBIAN/control
	@echo "Maintainer: J. Nathanael Philipp <nathanael@philipp.land>" >> build/package/DEBIAN/control
	@echo "Homepage: https://github.com/jnphilipp/psync" >> build/package/DEBIAN/control
	@echo "Description: Python wrapper for rsync" >> build/package/DEBIAN/control
	@echo " This tool is to easly manage and configure complex rsync backups. Over\n XML complex configuration can be created for rsync. Additionally databases\n dumps for MySQL and PostgreSQL can be configured or scripts that should be\n run." >> build/package/DEBIAN/control
