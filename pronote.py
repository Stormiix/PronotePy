# -*- coding: utf-8 -*-

# @Author: Stormix - Anas Mazouni
# @Date:   2017-02-12 23:04:51
# @Email:  madadj4@gmail.com
# @Project: Pronote V3.9
# @Last modified by:   Stormix
# @Last modified time: 2017-06-03T17:37:25+01:00
# @Website: https://stormix.co

import pronoteV3 as pr
import getpass


url = 'https://e212073y.index-education.net/pronote/eleve.html'
lastname = input("Name : ")
password = getpass.getpass('Password : ')
delay = (20 - int(input("How fast is your internet [0 - 20] ? : ")))//2
print("The delay was set to : {0}s".format(delay))
pronote = pr.Pronote(url,lastname,password)
pronote.delay = delay
pronote.limit = 10 # For testing purposes I only download 1 subject
print(pronote)
pronote.setOutput('PronoteFiles')
pronote.launchBrowser()
pronote.login()
pronote.Download()
