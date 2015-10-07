#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Process json with broken planet URLs and send a message to the
user to fix it.
Daniel Bruno <dbruno@fedoraproject.org>
"""

from fedora.client import AccountSystem
import getpass
import json
import sys
import os
import smtplib
import ast

try:
	json_in = open(sys.argv[1], 'r').readlines()
	if os.path.isfile(sys.argv[1]) == False:
	 	print "[Error] - Please check the file name and/or path."
 		exit()
except IndexError, error:
	print "[Error] - File name is missing on the first parameter"
	exit()

senderAddr = "admin@fedoraproject.org"
senderName = "Fedora Infrastructure"

username = raw_input('FAS Username: ')
password = getpass.getpass()

# Connecting to FAS
fas2 = AccountSystem(username=username, password=password)

# Reading the JSON report and get the information data
for item in json_in:
	report = json.loads(item.replace('\n', ''))

	user = report['user']
	url = report['url']
	error = report['error']

	user_data = fas2.person_by_username(user)
	user_realname = user_data.human_name
	user_email = user_data.email

	if user_realname == None:
		# Some users don't set the real name on FAS
		user_realname = report['user']

	message = """From: %s <%s>
To: %s <%s>
MIME-Version: 1.0
Content-type: text/plain
Subject: Fedora Planet Warning\n
Hello %s,

The URL you have configured for the Fedora Planet is not working. 

URL: %s
Problem: %s

Please fix this issue as soon as you can.

Your feed may be completely removed if not fixed. 

See: https://fedoraproject.org/wiki/Planet
For more information. 
	
Fedora Infrastructure
	""" % ( senderName, senderAddr, user_realname, user_email, user_realname, url, error)
	
	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(senderAddr, user_email, message)
	except:
		print "Failed to send the notification to: %s" % user_email
