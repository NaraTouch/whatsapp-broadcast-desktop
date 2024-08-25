Project: WhatApp BroadCast

Description: This project is a Python application that provides a command-line interface for managing WhatApp BroadCast.

+ Generate requirements.txt
    # pip freeze > requirements.txt

Requirements:
 + Python 3.6 or higher
 + The following packages, which can be installed using 
    # pip install -r requirements.txt

Run as dev:

    # python run.py

Make .exe
# pyinstaller run.py --onefile --windowed

OPTION Rebuild
# pyinstaller run.spec

OPTION Error

Open CMD -> cd: C:\Users\User\AppData\Local\Programs\Python\Python312
         ->pip install PyQt5
         ->pip install selenium
         ->pip install pyperclip
         ->pip install webdriver-manager

         >>python
         >>import pyperclip
         >>pyperclip.__version__
         >>import PyQt5
         >>PyQt5.__version__
         >>import selenium
         >>selenium.__version__
         >>import webdriver_manager
         >>webdriver_manager.__version__
Go to Project Directory
Open CD:
# pyinstaller --onefile --windowed --hidden-import=webdriver_manager --hidden-import=selenium --hidden-import=pyperclip --hidden-import=PyQt5 run.py
