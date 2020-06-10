SHELL=/bin/bash

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

install: psync psync.xsd psync.bash-completion build/copyright build/changelog.Debian.gz build/psync.1.gz
	$(Q)apt install python3-lxml rsync

	$(Q)install -Dm 0755 psync "${BIN_DIR}"/psync
	$(Q)install -Dm 0644 psync.xsd "${SHARE_DIR}"/psync/psync.xsd
	$(Q)install -Dm 0644 psync.bash-completion "${BASH_COMPLETION_DIR}"/psync.bash-completion
	$(Q)install -Dm 0644 build/changelog.Debian.gz "${DOC_DIR}"/psync/changelog.Debian.gz
	$(Q)install -Dm 0644 build/copyright "${DOC_DIR}"/psync/copyright
	$(Q)install -Dm 0644 build/psync.1.gz "${MAN_DIR}"/man1/psync.1.gz

	@echo "psync install completed."

uninstall:
	$(Q)rm "${BIN_DIR}"/psync
	$(Q)rm "${BASH_COMPLETION_DIR}"/psync.bash-completion
	$(Q)rm "${MAN_DIR}"/man1/psync.1.gz
	$(Q)rm -r "${SHARE_DIR}"/psync
	$(Q)rm -r "${DOC_DIR}"/psync

	@echo "psync uninstall completed."

clean:
	$(Q)rm -rf ./build

deb: build/package/DEBIAN/control
	$(Q)fakeroot dpkg-deb -b build/package build/psync.deb
	$(Q)lintian -Ivi build/psync.deb

build:
	$(Q)mkdir -p build

build/copyright: build
	$(Q)echo "Upstream-Name: psync" > build/copyright
	$(Q)echo "Source: https://github.com/jnphilipp/psync" >> build/copyright
	$(Q)echo "Files: *" >> build/copyright
	$(Q)echo "Copyright: 2019-2020 J. Nathanael Philipp (jnphilipp) <nathanael@philipp.land>" >> build/copyright
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
	$(Q)declare TAGS=(`git tag`); for ((i=$${#TAGS[@]};i>=0;i--)); do if [ $$i -eq 0 ]; then git log $${TAGS[$$i]} --no-merges --format="psync ($${TAGS[$$i]}-%h) unstable; urgency=medium%n%n  * %s%n    %b%n -- %an <%ae>  %aD%n" | sed "/^\s*$$/d" >> build/changelog; elif [ $$i -eq $${#TAGS[@]} ]; then git log $${TAGS[$$i-1]}..HEAD --no-merges --format="psync ($${TAGS[$$i-1]}-%h) unstable; urgency=medium%n%n  * %s%n    %b%n -- %an <%ae>  %aD%n" | sed "/^\s*$$/d" >> build/changelog; else git log $${TAGS[$$i-1]}..$${TAGS[$$i]} --no-merges --format="psync ($${TAGS[$$i]}-%h) unstable; urgency=medium%n%n  * %s%n    %b%n -- %an <%ae>  %aD%n" | sed "/^\s*$$/d" >> build/changelog; fi; done
	$(Q)cat build/changelog | gzip -n9 > build/changelog.Debian.gz

build/psync.1.gz: build build/copyright.h2m
	$(Q)help2man ./psync -i build/copyright.h2m -n "Python wrapper for rsync." | gzip -n9 > build/psync.1.gz

build/package/DEBIAN: build
	$(Q)mkdir -p build/package/DEBIAN

build/package/DEBIAN/md5sums: psync psync.xsd psync.bash-completion build/copyright build/changelog.Debian.gz build/psync.1.gz build/package/DEBIAN
	$(Q)install -Dm 0755 psync build/package"${BIN_DIR}"/psync
	$(Q)install -Dm 0644 psync.xsd build/package"${SHARE_DIR}"/psync/psync.xsd
	$(Q)install -Dm 0644 psync.bash-completion build/package"${BASH_COMPLETION_DIR}"/psync.bash-completion
	$(Q)install -Dm 0644 build/changelog.Debian.gz build/package"${DOC_DIR}"/psync/changelog.Debian.gz
	$(Q)install -Dm 0644 build/copyright build/package"${DOC_DIR}"/psync/copyright
	$(Q)install -Dm 0644 build/psync.1.gz build/package"${MAN_DIR}"/man1/psync.1.gz

	$(Q)mkdir -p build/package/DEBIAN
	$(Q)md5sum `find build/package -type f -not -path "*DEBIAN*"` > build/md5sums
	$(Q)sed -e "s/build\/package\///" build/md5sums > build/package/DEBIAN/md5sums
	$(Q)chmod 644 build/package/DEBIAN/md5sums

build/package/DEBIAN/control: build/package/DEBIAN/md5sums
	$(Q)echo "Package: psync" > build/package/DEBIAN/control
	$(Q)echo "Version: `git describe --tags`-`git log --format=%h -1`" >> build/package/DEBIAN/control
	$(Q)echo "Section: utils" >> build/package/DEBIAN/control
	$(Q)echo "Priority: optional" >> build/package/DEBIAN/control
	$(Q)echo "Architecture: all" >> build/package/DEBIAN/control
	$(Q)echo "Depends: python3 (>= 3.6), python3-lxml, rsync" >> build/package/DEBIAN/control
	$(Q)echo "Recommends: pass" >> build/package/DEBIAN/control
	$(Q)echo "Installed-Size: `du -sk build/package/usr | grep -oE "[0-9]+"`" >> build/package/DEBIAN/control
	$(Q)echo "Maintainer: J. Nathanael Philipp <nathanael@philipp.land>" >> build/package/DEBIAN/control
	$(Q)echo "Homepage: https://github.com/jnphilipp/psync" >> build/package/DEBIAN/control
	$(Q)echo "Description: Python wrapper for rsync" >> build/package/DEBIAN/control
	$(Q)echo " This tool is to easly manage and configure complex rsync backups. Over" >> build/package/DEBIAN/control
	$(Q)echo " XML complex configuration can be created for rsync. Additionally databases" >> build/package/DEBIAN/control
	$(Q)echo " dumps for MySQL and PostgreSQL can be configured or scripts that should be run." >> build/package/DEBIAN/control
