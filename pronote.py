# @Author: Anas Mazouni <Stormix>
# @Date:   2017-05-05T13:24:23+01:00
# @Email:  madadj4@gmail.com
# @Project: PluralSight Scrapper
# @Last modified by:   Stormix
# @Last modified time: 2017-05-20T01:05:25+01:00



# -*- coding: utf-8 -*-
import pronoteV3 as pr
import getpass


url = 'https://e212073y.index-education.net/pronote/eleve.html'
lastname = "Mazouni"
password = "AnasStormix12344321ximrotSsanA"
delay = 5
print("The delay was set to : {0}s".format(delay))
pronote = pr.Pronote(url,lastname,password)
pronote.delay = delay
print(pronote)
pronote.setOutput('PronoteFichiers')
pronote.launchBrowser()
pronote.login()
pronote.goToSubjects()
pronote.Download()
