# backup

Easily configure and reproducibly run complex backups.

[![Tests](https://github.com/jnphilipp/backup/actions/workflows/tests.yml/badge.svg)](https://github.com/jnphilipp/backup/actions/workflows/tests.yml)

## Features
 * Configure complex backups with XML
 * XML schema validation
 * Configurable scripts to run during backup
 * Support for rsync and tar
 * Database dumps for MySQL and PostgreSQL
 * Configurable pipeline
 * Snapshots


## Requirements

* Python 3.7 or newer
* python-lxml
* rsync or tar as backup tool


## Install

* from Source: ```make install```
* deb-Package: ```make deb```
* [AUR](https://aur.archlinux.org/packages/backup)

## Usage

For options see `$ backup -h`. For example XML configuration have a look at `/tests/rsync.xml` or `/tests/tar.xml`.

### Icon

Icon made from [Icon Fonts](http://www.onlinewebfonts.com/icon) licensed by CC BY 3.0.
