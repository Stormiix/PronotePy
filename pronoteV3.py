# -*- coding: utf-8 -*-

# @Author: Stormix - Anas Mazouni
# @Date:   2017-02-12 23:04:51
# @Email:  madadj4@gmail.com
# @Project: Pronote V3.9
# @Last modified by:   Stormix
# @Last modified time: 2017-06-03T17:19:03+01:00
# @Website: https://stormix.co

# Import Some Python Modules

import inspect, sys
import os
import time
import urllib
import urllib.request
from sys import platform
import re

# Import Browser modules

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# V4
from clint.textui import progress
import requests
from multiprocessing import Queue

class Pronote:
    '''
        Pronote Class
    '''
    # Pronote Class Attributes
    limit = 10
    counter = 0
    delay = 5
    url = None
    id_code = "140"
    user_input = "GInterface.Instances[0].idIdentification.bouton_Edit"
    password_input = "GInterface.Instances[0]_password"
    connect_button = "GInterface.Instances[0].idBtnConnexion"
    shared_files = "GInterface.Instances[0].Instances[7]_Combo0"
    browser = None
    Output = "PronoteFichiers"
    thankyou = """
          -----------------------------------------------------
          All Done ! Thanks for using PronoteDownloader !
          -----------------------------------------------------
          By Anas Mazouni -  Stormix (https://stormix.co)
          """

    def __init__(self,url,last_name,password):
        self.url = url
        self.username = last_name
        self.password = password

    def __str__(self):
        '''
		Object Representation
        '''
        return """
         _____                 _          ____                _           _
        |  _  |___ ___ ___ ___| |_ ___   |    \ ___ _ _ _ ___| |___ ___ _| |___ ___
        |   __|  _| . |   | . |  _| -_|  |  |  | . | | | |   | | . | .'| . | -_|  _|
        |__|  |_| |___|_|_|___|_| |___|  |____/|___|_____|_|_|_|___|__,|___|___|_|
         _____            __          _
        |   __|___ ___   |  |   _ _ _| |___ _ _ ___ ___ ___
        |   __| . |  _|  |  |__| | | . | -_|_'_| -_|  _|_ -|
        |__|  |___|_|    |_____|_  |___|___|_,_|___|_| |___|
                               |___|
        ---------------------------------------------------------------------------
        Connected to : %s
        As :
            -> Last Name : %s
            -> Password : %s
        """ % (self.url,self.username,"*"*len(self.password))

    def changeID(self,id):
        assert type(id) and 100 < int(id) < 999 , "Invalid ID"
        self.id_code = id

    def launchBrowser(self):
        assert not self.browser, "Browser already set !"
        # Initiate the Browser webdriver
        currentfolder = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
        # Check which operating system is being used !
        if platform == "linux" or platform == "linux2":
            # linux
            chrome_driver = currentfolder+"/Drivers/chromedriver"
        elif platform == "win32":
            # Windows
            chrome_driver = currentfolder+"/Drivers/chromedriver.exe"
        self.browser = webdriver.Chrome(chrome_driver)
        Browser = self.browser
        Website = self.url
        # Open Pronote
        Browser.get(Website)
        print("Browser Initiated !")
        print("Loading .. " + Website, end =' ')
        time.sleep(self.delay)
        print('[DONE]')

    def setOutput(self,folder):
        assert type(folder) == str , "Invalide Folder Name"
        print('Changing output folder to /'+ folder)
        if not os.path.isdir(folder):
            # If not , make a new one
            os.makedirs(folder)
            print("Creating "+folder +"...",'[DONE]')
            self.Output = folder
            print("Download folder changed !")
        else:
            self.Output = folder

    def scroll(self):
        Browser = self.browser
        Browser.execute_script("document.getElementById('GInterface.Instances[1].Instances[3]_Zone_0').scrollTop += 220;")

    def login(self):
        """A procedure used to login into Pronote using the students credentials
        """
        Browser = self.browser
        Username = self.username
        Password = self.password
        # Fill in the login form
        username_log = Browser.find_element_by_id(self.user_input)
        password_log = Browser.find_element_by_id(self.password_input)
        username_log.send_keys(Username)
        password_log.send_keys(Password)
        # Click the connect buttun
        print("Logging in ...",end=" ")
        Browser.find_element_by_id(self.connect_button).click()
        time.sleep(self.delay)
        print('[DONE]')

    def goToSubjects(self):
        # Go to the files/contenu de cour section
        self.browser.find_element_by_id(self.shared_files).click()
        time.sleep(self.delay)
        print("Opened > 'Ressources pédagogiques' ....")

    def checkExists(self,id):
        try:
            self.browser.find_element_by_id("id_"+str(id)+"_mat_0_-1")
        except NoSuchElementException:
            return False
        return True

    def autoIdSet(self,verbose = False):
        Browser = self.browser
        found = False
        for i in range(100,500):
            if self.checkExists(i):
                found = True
                if verbose:
                    print("Found the correct ID :" + str(i))
                self.changeID(i)
                break
        if not found:
            raise ValueError("Couldn't find the correct ID")

    def fetchSubjects(self):
        assert type(self.limit) == int, "Invalid Limit"
        Browser = self.browser
        limit = self.limit
        subjects = dict()
        print("Look for the diffrent subjects , please wait ...")
        self.goToSubjects()
        self.autoIdSet()
        for i in range(limit):
            subject_id = "id_"+str(self.id_code)+"_mat_"+str(i)+"_-1"
            # Alright , now that we got the id , let's get into work
            subject = Browser.find_element_by_id(subject_id)
            subject_name  = subject.text # Fetch the subject name !
            subjects[subject_id] = subject_name
        print("Fetched all subject !")
        return subjects

    def fetchFiles(self,subject,subjectPage = True):
        """
        Params:
            subject (tuple) :  Contains subject name and id
        """
        Browser = self.browser
        subject_name = subject[1]
        subject_id = subject[0]
        if not subjectPage:
            self.goToSubjects()
        print('Opened : ' + subject_name)
        print("Searching for files to download",end=" ... ")
        try:
            subject_elt = Browser.find_element_by_id(subject_id)
        except NoSuchElementException:
            self.autoIdSet()
            subject_id = "id_"+str(self.id_code)+subject_id[6:]
            subject_elt = Browser.find_element_by_id(subject_id)
        Hover = ActionChains(Browser).move_to_element(subject_elt) # Pronote has this 'nice' animation when u try to open a certain subject
        # It's a page flip animation , and I needed to simulate a mouse hovering on the subject to trigger this animation
        # So I did just that
        Hover.click().perform()
        time.sleep(self.delay/2)
        subject_elt.click()
        time.sleep(self.delay)
        files_list = Browser.find_elements_by_xpath("//a[@class='Texte10 Maigre SouligneSurvol SouligneSurvol AvecMenuContextuel']")
        time.sleep(3)
        Files = []
        for File in files_list:
            File_name = File.text
            File_link = File.get_attribute("href")
            if File_name == "":
                self.scroll()
                time.sleep(2)
            else:
                Files += [(subject_name,File_name,File_link)]
        print('Found ['+str(len(Files))+']')
        self.goToSubjects()
        self.autoIdSet() # Must update the ID each time!
        return Files

    def downloadFiles(self,Files):
        assert type(Files) == list and len(Files) != 0, "Empty File List !"
        counter = 0
        for File in Files:
            download_folder = self.Output
            File_subject = File[0]
            File_name = File[1]
            File_link = File[2]
            Folder = File_subject.replace("/", "-") # Escaping the folder names ! (TP GE/GM => TP GE-GM)
            Folder = download_folder+'/'+Folder
            File_path = Folder + "/" + File_name
            if not os.path.isdir(Folder):
                # If not , make a new one
                os.makedirs(Folder)
            # Check if the file already exists , if not download it
            if not os.path.exists(File_path):
                size = urllib.request.urlopen(File_link).info()['Content-Length']
                print("-> Downloading "+File_name+" ",end=" ")
                self.downloadUrl(File_link, File_path)
                print('[DONE]')
                counter += 1
        print("-"*30,str(counter) + " files were downloaded !",sep=" \n")

    def downloadUrl(self,url,path):
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def resetConnection(self):
        """
        Refreshes the visited website and logs in
        ! THIS FUNCTION WILL BE REMOVED IN FUTURE VERISONS !
        """
        Browser = self.browser
        print("Going back  ....")
        # Refreshs the website
        Browser.refresh();
        self.login()
        time.sleep(delay)
        # Let's go back to Ressources pédagogiques
        self.goToSubjects()

    def fetchDownloadedFiles(self):
        path = './' +self.Output+ '/'
        subjects = os.listdir(path)
        Files = []
        for subject in subjects:
            Files += [(subject,File) for File in os.listdir(path+subject+'/')]
        return Files

    def fetchNewFiles(self):
        """
        Return :
            returns a list of downloadable files
        """
        Files = []
        Subjects = [subject_name for subject_name in self.fetchSubjects().items()]
        for subject in Subjects:
            Files += self.fetchFiles(subject)
        DownloadedFiles = self.fetchDownloadedFiles()
        # Compare LISTS
        print("Comparing results :")
        j = len(Files)
        while j >= 0:
            j -= 1
            if (Files[j][0],Files[j][1]) in DownloadedFiles:
                j += 1
                Files.remove(Files[j])
        return Files

    def Update(self):
        NewFiles = self.fetchNewFiles()
        self.downloadFiles(NewFiles)
        print(self.thankyou)

    def Download(self):
        Files = []
        Subjects = [subject_name for subject_name in self.fetchSubjects().items()]
        for subject in Subjects:
            Files += self.fetchFiles(subject)
        self.downloadFiles(Files)
        print(self.thankyou)

    def latestMarks(self,count):
        assert type(count) == int and 6 > count > 0 , "Invalid Count"
        Notes = []
        Browser = self.browser
        print("Fetching your latest marks , please wait ...")
        time.sleep(self.delay)
        for i in range(count):
            Note_id = "GInterface.Instances[1]_notes_"+str(i)
            Note = Browser.find_element_by_id(Note_id).get_attribute("aria-label")
            details = Note.split()
            single = ['INFORMATIQUE','FRANCAIS','MATHEMATIQUES']
            if not details[0] in single:
                details = details[0]+" "+details[1]+" just posted a new mark , you got : "+details[2]+". Moyenne de classe : "+details[8]
            elif details[0] == 'INFORMATIQUE':
            	details = details[0]+" just posted a new mark , you got : "+details[1]+". Moyenne de classe : " + details[8]
            elif details[0] == 'FRANCAIS' :
                details = details[0]+" just posted a new mark , you got : "+details[1]+". Moyenne de classe : " + details[7]
            Notes += [details]
        return Notes

    def showGrades(self):
        count = int(input('How many marks do you want to see ? '))
        Notes = self.latestMarks(count)
        for note in Notes:
            print(note)
