SHELL:=/bin/bash

BASH_COMPLETION_DIR?=/usr/share/bash-completion.d
BIN_DIR?=/usr/bin
DOC_DIR?=/usr/share/doc
ICON_DIR?=/usr/share/icons
MAN_DIR?=/usr/share/man
SHARE_DIR?=/usr/share
DEST_DIR?=

ifdef VERBOSE
  Q :=
else
  Q := @
endif

test:
	python -m unittest

install: backup backup.xsd backup.bash-completion build/copyright build/changelog.Debian.gz build/backup.1.gz
	$(Q)install -Dm 0755 backup "${DEST_DIR}/${BIN_DIR}"/backup
	$(Q)install -Dm 0644 backup.xsd "${DEST_DIR}/${SHARE_DIR}"/backup/backup.xsd
	$(Q)install -Dm 0644 backup.bash-completion "${DEST_DIR}/${BASH_COMPLETION_DIR}"/backup.bash-completion
	$(Q)install -Dm 0644 build/changelog.Debian.gz "${DEST_DIR}/${DOC_DIR}"/backup/changelog.Debian.gz
	$(Q)install -Dm 0644 build/copyright "${DEST_DIR}/${DOC_DIR}"/backup/copyright
	$(Q)install -Dm 0644 build/backup.1.gz "${DEST_DIR}/${MAN_DIR}"/man1/backup.1.gz
	$(Q)install -Dm 0644 backup.svg "${DEST_DIR}/${ICON_DIR}"/hicolor/scalable/apps/backup.svg

	@echo "backup install completed."

uninstall:
	$(Q)rm "${BIN_DIR}"/backup
	$(Q)rm "${BASH_COMPLETION_DIR}"/backup.bash-completion
	$(Q)rm "${MAN_DIR}"/man1/backup.1.gz
	$(Q)rm -r "${SHARE_DIR}"/backup
	$(Q)rm -r "${DOC_DIR}"/backup

	@echo "backup uninstall completed."

clean:
	$(Q)rm -rf ./build

deb: test build/package/DEBIAN/control
	$(Q)fakeroot dpkg-deb -b build/package build/backup.deb
	$(Q)lintian -Ivi build/backup.deb
	@echo "backup.deb completed."

deb-sig: deb
	$(Q)dpkg-sig -s builder build/backup.deb

build:
	$(Q)mkdir -p build

build/copyright: build
	$(Q)echo "Upstream-Name: backup" > build/copyright
	$(Q)echo "Source: https://github.com/jnphilipp/backup" >> build/copyright
	$(Q)echo "Files: *" >> build/copyright
	$(Q)echo "Copyright: 2019-2022 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>" >> build/copyright
	$(Q)echo "License: GPL-3+" >> build/copyright
	$(Q)echo " This program is free software: you can redistribute it and/or modify" >> build/copyright
	$(Q)echo " it under the terms of the GNU General Public License as published by" >> build/copyright
	$(Q)echo " the Free Software Foundation, either version 3 of the License, or" >> build/copyright
	$(Q)echo " any later version." >> build/copyright
	$(Q)echo "" >> build/copyright
	$(Q)echo " This program is distributed in the hope that it will be useful," >> build/copyright
	$(Q)echo " but WITHOUT ANY WARRANTY; without even the implied warranty of" >> build/copyright
	$(Q)echo " MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the" >> build/copyright
	$(Q)echo " GNU General Public License for more details." >> build/copyright
	$(Q)echo "" >> build/copyright
	$(Q)echo " You should have received a copy of the GNU General Public License" >> build/copyright
	$(Q)echo " along with this program. If not, see <http://www.gnu.org/licenses/>." >> build/copyright
	$(Q)echo " On Debian systems, the full text of the GNU General Public" >> build/copyright
	$(Q)echo " License version 3 can be found in the file" >> build/copyright
	$(Q)echo " '/usr/share/common-licenses/GPL-3'." >> build/copyright

build/copyright.h2m: build
	$(Q)echo "[COPYRIGHT]" > build/copyright.h2m
	$(Q)echo "This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version." >> build/copyright.h2m
	$(Q)echo "" >> build/copyright.h2m
	$(Q)echo "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details." >> build/copyright.h2m
	$(Q)echo "" >> build/copyright.h2m
	$(Q)echo "You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/." >> build/copyright.h2m

build/changelog.Debian.gz: build
	$(Q)( \
		declare TAGS=(`git tag`); \
		for ((i=$${#TAGS[@]};i>=0;i--)); do \
			if [ $$i -eq 0 ]; then \
				echo -e "bibliothek ($${TAGS[$$i]}) unstable; urgency=medium" >> build/changelog; \
				git log $${TAGS[$$i]} --no-merges --format="  * %h %s"  >> build/changelog; \
				git log $${TAGS[$$i]} -n 1 --format=" -- %an <%ae>  %aD" >> build/changelog; \
			elif [ $$i -eq $${#TAGS[@]} ] && [ $$(git log $${TAGS[$$i-1]}..HEAD --oneline | wc -l) -ne 0 ]; then \
				echo -e "bibliothek ($${TAGS[$$i-1]}-$$(git log -n 1 --format='%h')) unstable; urgency=medium" >> build/changelog; \
				git log $${TAGS[$$i-1]}..HEAD --no-merges --format="  * %h %s"  >> build/changelog; \
				git log HEAD -n 1 --format=" -- %an <%ae>  %aD" >> build/changelog; \
			elif [ $$i -lt $${#TAGS[@]} ]; then \
				echo -e "bibliothek ($${TAGS[$$i]}) unstable; urgency=medium" >> build/changelog; \
				git log $${TAGS[$$i-1]}..$${TAGS[$$i]} --no-merges --format="  * %h %s"  >> build/changelog; \
				git log $${TAGS[$$i]} -n 1 --format=" -- %an <%ae>  %aD" >> build/changelog; \
			fi; \
		done \
	)
	$(Q)cat build/changelog | gzip -n9 > build/changelog.Debian.gz

build/backup.1.gz: build build/copyright.h2m
	$(Q)help2man ./backup -i build/copyright.h2m -n "Python wrapper for rsync." | gzip -n9 > build/backup.1.gz
	$(Q)LC_ALL=en_US.UTF-8 MANROFFSEQ='' MANWIDTH=80 man --warnings -E UTF-8 -l -Tutf8 -Z ./build/backup.1.gz > /dev/null

build/package/DEBIAN/md5sums: backup backup.xsd backup.bash-completion backup.svg build/copyright build/changelog.Debian.gz build/backup.1.gz
	$(Q)make install DEST_DIR=build/package
	$(Q)mkdir -p build/package/DEBIAN
	$(Q)find build/package -type f -not -path "*DEBIAN*" -exec md5sum {} \; > build/md5sums
	$(Q)sed -e "s/build\/package\///" build/md5sums > build/package/DEBIAN/md5sums
	$(Q)chmod 0644 build/package/DEBIAN/md5sums

build/package/DEBIAN/control: build/package/DEBIAN/md5sums
	$(Q)echo "Package: backup" > build/package/DEBIAN/control
	$(Q)echo "Version: `git describe --tags`-`git log --format=%h -1`" >> build/package/DEBIAN/control
	$(Q)echo "Section: utils" >> build/package/DEBIAN/control
	$(Q)echo "Priority: optional" >> build/package/DEBIAN/control
	$(Q)echo "Architecture: all" >> build/package/DEBIAN/control
	$(Q)echo "Depends: python3 (>= 3.7), python3-lxml, rsync" >> build/package/DEBIAN/control
	$(Q)echo "Recommends: pass, python-notify2" >> build/package/DEBIAN/control
	$(Q)echo "Installed-Size: `du -sk build/package/usr | grep -oE "[0-9]+"`" >> build/package/DEBIAN/control
	$(Q)echo "Maintainer: J. Nathanael Philipp <nathanael@philipp.land>" >> build/package/DEBIAN/control
	$(Q)echo "Homepage: https://github.com/jnphilipp/backup" >> build/package/DEBIAN/control
	$(Q)echo "Description: Easily configure and reproducibly run complex backups" >> build/package/DEBIAN/control
	$(Q)echo " This tool is to easly manage and configure complex backups. With XML" >> build/package/DEBIAN/control
	$(Q)echo " configure complex backups. Supports rsync and tar as backup tools." >> build/package/DEBIAN/control
	$(Q)echo " Additionally configure database dumps (MySQL and PostgreSQL) or" >> build/package/DEBIAN/control
	$(Q)echo " arbitrary scripts that should be run during backup." >> build/package/DEBIAN/control
