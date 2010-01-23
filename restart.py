#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import telnetlib
import re
import time
import sys
import os

HOST = "192.168.2.1"
password = "password"

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

def drukuj(wiadomosc):
	sys.stdout.write("\r")
	sys.stdout.write("                                                    ")
	sys.stdout.flush()
	sys.stdout.write("\r")
	sys.stdout.write(wiadomosc)
	sys.stdout.flush()
	#sys.stdout.write("\r")
	

def status(komenda):
	odb = ""
	try:
		tn = telnetlib.Telnet(host=HOST,timeout=23)
	except IOError:
		print "Nie nawiązano połączenia :(\n"
	else:
		tn.read_until("Password: ")
		tn.write(password + "\n")
		if komenda=="wan adsl reset\n":
			tn.write(komenda)
			tn.write("exit\n")
			#print "Połączenie zostało z resetowane"
			drukuj(bcolors.FAIL + "Połączenie zostało z resetowane" + bcolors.ENDC)
		if komenda=="ip route status\n":
			tn.write(komenda)
			tn.write("exit\n")
			odb = tn.read_all()
		if komenda=="wan adsl status\n":
			tn.write("wan adsl status\n")
			tn.write("exit\n")
			odb = tn.read_all()
			if re.search('current modem status: down', odb):
				#print "Status: down"
				drukuj(bcolors.HEADER + "Status: down" + bcolors.ENDC)
			if re.search('current modem status: wait for initialization', odb):
				#print "Status: wait for initialization"
				drukuj(bcolors.WARNING + "Status: wait for initialization" + bcolors.ENDC)
			if re.search('current modem status: initializing', odb):
				#print "Status: initializing"
				drukuj(bcolors.WARNING + "Status: initializing" + bcolors.ENDC)
			if re.search('current modem status: up', odb):
				#print "Status: up"
				drukuj(bcolors.OKBLUE + "Status: up" + bcolors.ENDC)
	return odb

def clear():
	if os.name == "posix":
		# Unix/Linux/MacOS/BSD/etc
		os.system('clear')
	elif os.name in ("nt", "dos", "ce"):
		# DOS/Windows
		os.system('CLS')

if __name__=="__main__":
	clear()
	status("wan adsl reset\n")
	time.sleep(5)
	a = True
	while a:
		odb = status("ip route status\n")
		if re.search('\d *poe0 *\d', odb):
			#print "Modem działa"
			drukuj(bcolors.OKGREEN + "-={{Modem działa}}=-\n" + bcolors.ENDC)
			time.sleep(2)
			#clear()
			a = False
		else:
			#print "Nie działa"
			time.sleep(3)
			status("wan adsl status\n")
			time.sleep(3)
			#print a

