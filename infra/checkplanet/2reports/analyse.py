#!/usr/bin/python
# -*- coding: utf-8 -*-
# Daniel Bruno - dbruno@fedoraproject.org
# Read the report after check who still broken
import json
import os
import sys

report1 = open(sys.argv[1], 'r').readlines()
report2 = open(sys.argv[2], 'r').readlines()

users1 = []
users2 = []

# Reading the JSON reports
for u1 in report1:
    user = json.loads(u1.replace('\n', ''))
    users1.append({'user': user['user'], 'error': user['error']})

for u2 in report2:
    user = json.loads(u2.replace('\n', ''))
    users2.append({'user': user['user'], 'error': user['error']})

stillbroken = []
fixed = []
newones = []

for i in users1:
	check = 0
	for x in users2:
		if i['user'] == x['user']:
			#stillbroken.append(i['user'])
			check = 1
	if check == 1:
		stillbroken.append(i['user'])
	else:
		fixed.append(i['user'])

for i in users2:
	check = 0
	for x in users1:
		if i['user'] == x['user']:
			check = 1
	if check == 0:
		newones.append(i['user'])


print "Still broken: "
for x in stillbroken:
	print x,
print ""
print "Fixed: "
for x in fixed:
	print x,
print ""
print "New ones: "
for x in newones:
	print x,
