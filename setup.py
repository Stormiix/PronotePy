# -*- coding: utf-8 -*-
# @Author: Anas Mazouni
# @Date:   2017-02-18 16:38:33
# @Last modified by:   Stormix
# @Last modified time: 2017-06-03T17:21:49+01:00
import sys
from cx_Freeze import setup, Executable
# How to run : python setup.py build
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["idna","pronoteV3","os","requests","inspect","sys","time","clint","selenium","getpass"], "excludes": ["readline"], "include_files": [("Drivers/chromedriver.exe","Drivers/chromedriver.exe")]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Console'
setup(  name='Pronote',
    	version='3.9',
        description='Pronote file downloader.',
	    author='Anas Mazouni - Stormix.co',
	    author_email='madadj4@gmail.com',
	    url='https://github.com/Stormiix/PronotePy',
        options = {"build_exe": build_exe_options},
        executables = [Executable("pronote.py", base=base,icon="Pronote.ico",copyright="© 2014-2017 All rights reserved. Made by Anas Mazouni",shortcutName="Pronote Downloader V3.9")])
