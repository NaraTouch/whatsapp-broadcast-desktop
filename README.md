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
pyinstaller.exe --onefile --windowed --icon=C:\python\whatsapp-broadcast-desktop\resources\icons\app_icon.ico --debug C:\python\whatsapp-broadcast-desktop\run.py

pyinstaller.exe --onefile --windowed --icon=resources\icons\app_icon.ico run.py