#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import os
import sys
import time
import subprocess
import pynotify

bdir=''
method=''
pgdump=''


def send_notification(message):
	"""send feed updates to notify-osd"""   
	pynotify.init('Backup')
	n = pynotify.Notification('Backup', message, 'deja-dup')
	n.set_hint_string('x-canonical-append','')
	n.show()


def main(argv):
	global bdir
	global method
	global pgdump

	try:
		opts, args = getopt.getopt(argv,"hd:m:p",["dir=", "method=", "pg_dump="])
	except getopt.GetoptError:
		print 'backup.py -d <backup dir> -m <backup method>'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print 'backup.py -d <backup dir> -m <backup method>'
			sys.exit()
		elif opt in ("-d", "--dir"):
			bdir = arg
		elif opt in ("-m", "--method"):
			method = arg
		elif opt in ("-p", "--pg_dump"):
			pgdump='dump'

	if bdir == '' and pgdump == '':
		print 'backup.py -d <backup dir>'
		sys.exit(1)
		

def get_sources():
	sources = set()

	sources.add(('/var/www',))
	sources.add(('/home/USER', 'exclude1', 'exclude2', '...'))

	return sources

def backup():
	#print 'start backup...'
	sources = get_sources()

	for source in sources:
		print source[0]
		send_notification('Start backup of \'' + source[0] + '\'.')
		print 'Start backup of \'' + source[0] + '\'.'
		if not os.path.exists(os.path.dirname(bdir + source[0])):
			os.makedirs(os.path.dirname(bdir + source[0]))

		exclude=''
		for ex in source[1:]:
			print 'exclude: ' + ex
			exclude = exclude + ' --exclude=' + ex

		os.system('rsync --delete -aucPz' + exclude + ' ' + source[0] + '/ ' + bdir + source[0])

	#print 'finnished backup'

def postgres_dump():
	#print 'start postgres backup'
	send_notification('Start backup of PostgreSQL databases.')
	print 'Start backup of PostgreSQL databases.'

	timestamp = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime())
	os.putenv('PGPASSWORD', 'PASSWORD')
	os.system('pg_dump --username=USER -Fp DB | gzip -c > PATH/DB_' + timestamp + '.sql.gz')

	#print 'finished postgres backup'
	#send_notification('Finished backup of PostgreSQL databases.')

if __name__ == "__main__":
	main(sys.argv[1:])

	if not pgdump == '':
		postgres_dump()

	if not bdir == '':
		backup()

	send_notification('Backup complete.')
