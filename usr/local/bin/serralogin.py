#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2009-2010 Gioacchino Mazzurco <gmazzurco89@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
#

import mechanize
import time
import os

insd = 2

loginlist = open('/etc/serralogin/loginlist', 'r')

userpass = []

for line in loginlist:
  userpass.append(line.replace("\n", "").split(" ", 1))

while True:
	if(insd%2==0):
		agentHeader = [("User agent","(X11; U; Linux x86_64; en-US; rv:1.8.1.14) Gecko/20080418 Ubuntu/8.04 (hardy) Firefox/2.0.0.14")]
	elif(insd%3==0):
		agentHeader = [("User agent","Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)")]
	elif(insd%5==0):
		agentHeader = [("User agent","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1)")]
	else: agentHeader = [("User agent","Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.9 (like Gecko) (Kubuntu)")]

	connection = mechanize.Browser()
	connection.addheaders = agentHeader
	connection.set_handle_robots(False)

	while True:
		try:
			reponse = connection.open("http://overunity.altervista.org/scrokker.html")
			if(reponse.read() == "connected"):
			  print "Connection Test OK, insd=",insd
			  break
			else:
			  print "Connection Test Failed, Trying to login, insd=",insd
			  try:
			    connection.open("https://auth1.unipi.it/auth/perfigo_weblogin.jsp")
			    connection.select_form(nr=0)
			    connection.form["username"] = userpass[insd%len(userpass)][0]
			    connection.form["password"] = userpass[insd%len(userpass)][1]
			    connection.submit()
			    reponse = connection.open("http://overunity.altervista.org/scrokker.html")
			    if(reponse.read() == "connected"):
	                          print "Connection Test OK, insd=",insd
                                  break

			    print "Login Failed 1, trying next login, insd=",insd
			    break
			  except:
			    print "Login Failed 2, retry in 5 seconds, insd=",insd
			    time.sleep(4)
		except:
			print "Serra Connection seems not working, retry in 3 seconds, isnd=",insd
			os.system('arping -c10 -q 131.114.250.101')
			os.system('arping -c10 -q 131.114.250.1')
			#time.sleep(2)
	insd += 1
	time.sleep(1)
