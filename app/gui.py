import os
import re
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QThreadPool


from .whatsapp import WhatsApp
from .whatsapp_runnable import WhatsAppRunnable
from .login_runnable import LoginRunnable
from .api import Api
from PyQt5.QtGui import QIcon

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, 'app_icon.png')
        else:
            icon_path = 'app_icon.png'
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("WhatsApp Broadcast")
        self.setMaximumSize(500, 300)
        self.setMinimumSize(300, 300)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Login section
        self.login_section = QWidget()
        login_layout = QVBoxLayout()
        self.login_section.setLayout(login_layout)
        self.login_section.setContentsMargins(20, 20, 20, 20)
       
        self.image_edit = QTextEdit()
        self.image_edit.setStyleSheet("background-color: transparent; border: none; padding: 5px;")
        self.image_edit.setDisabled(True)
        login_layout.addWidget(self.image_edit)
        
        username_label = QLabel("Username")
        username_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText(r"example@nomail.com")
        self.username_entry.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        login_layout.addWidget(username_label)
        login_layout.addWidget(self.username_entry)

        password_label = QLabel("Password")
        password_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText(r"XXX@xxx")
        self.password_entry.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        login_layout.addWidget(password_label)
        login_layout.addWidget(self.password_entry)
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(
            "background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
        )
        login_layout.addWidget(self.login_button)
        self.main_layout.addWidget(self.login_section)
        self.login_button.clicked.connect(self.onLoginClick)
        self.setLayout(self.main_layout)

    def onLoginClick(self):
        if self.validate_login_input():
            self.startLogin()
        else:
            print("Invalid input")

    def startLogin(self):
        self.login_button.setEnabled(False)
        self.login_button.setText("Loading...")
        self.login_button.setStyleSheet(
            "background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
            "cursor: wait;"  # Change the cursor to a wait cursor
        )

        username = self.username_entry.text()
        password = self.password_entry.text()
        api = Api()
        self.thread_api = QThreadPool.globalInstance()
        login_runnable = LoginRunnable(api, username, password)
        login_runnable.signals.finished.connect(self.on_login_runnable_finished)
        self.thread_api.start(login_runnable)

    def on_login_runnable_finished(self, response):
        print(response)
        if response['statusCode'] == 200:
            self.login_section.hide()
            self.show_main_gui()
        else:
            error_message = response['message']
            QMessageBox.critical(self, "Error", error_message)

        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
        self.login_button.setStyleSheet(
            "background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
        )

    def show_main_gui(self):
        self.setMaximumSize(1920, 1080)
        self.setMinimumSize(900, 700)
        main_widgets_section = QWidget()
        main_widgets_layout = QVBoxLayout()
        main_widgets_section.setLayout(main_widgets_layout)

        # Chrome Profile field
        user_data_dir_label = QLabel("Chrome Profile:")
        user_data_dir_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.user_data_dir_edit = QLineEdit()
        self.user_data_dir_edit.setPlaceholderText(r"EX: C:\Users\User\AppData\Local\Google\Chrome\User Data")
        self.user_data_dir_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        user_data_dir_layout = QVBoxLayout()
        user_data_dir_layout.addWidget(user_data_dir_label)
        user_data_dir_layout.addWidget(self.user_data_dir_edit)

        # Message/Hours field
        message_interval_label = QLabel("Message/Hours:")
        message_interval_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.message_interval_edit = QLineEdit()
        self.message_interval_edit.setPlaceholderText(r"EX: Minimum 15 second/message")
        self.message_interval_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        message_interval_layout = QVBoxLayout()
        message_interval_layout.addWidget(message_interval_label)
        message_interval_layout.addWidget(self.message_interval_edit)

        # Create a single horizontal layout for both fields
        row_layout = QHBoxLayout()
        row_layout.addLayout(user_data_dir_layout)
        row_layout.addLayout(message_interval_layout)

        # Add the row layout to the main layout
        main_widgets_layout.addLayout(row_layout)

        # Profile field
        profile_label = QLabel("Profile:")
        profile_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger

        self.profile_edit = QLineEdit()
        self.profile_edit.setPlaceholderText("EX: Profile 1")  # Add a placeholder text
        self.profile_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        self.profile_edit2 = QLineEdit()
        self.profile_edit2.setPlaceholderText("EX: Profile 2")  # Add a placeholder text
        self.profile_edit2.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        self.profile_edit3 = QLineEdit()
        self.profile_edit3.setPlaceholderText("EX: Profile 3")  # Add a placeholder text
        self.profile_edit3.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        self.profile_edit4 = QLineEdit()
        self.profile_edit4.setPlaceholderText("EX: Profile 4")  # Add a placeholder text
        self.profile_edit4.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        # Create a QHBoxLayout to hold the two QLineEdit widgets
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(self.profile_edit)
        profile_layout.addWidget(self.profile_edit2)
        profile_layout.addWidget(self.profile_edit3)
        profile_layout.addWidget(self.profile_edit4)

        # Add the profile_layout to the main_widgets_layout
        main_widgets_layout.addWidget(profile_label)
        main_widgets_layout.addLayout(profile_layout)

        # Phone Number field
        phone_label = QLabel("Phone Numbers:")
        phone_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.phone_edit = QTextEdit()
        self.phone_edit.setPlaceholderText("EX:\n +855xxxxxx\n +855xxxxxx\n +855xxxxxx\n +855xxxxxx")
        self.phone_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        main_widgets_layout.addWidget(phone_label)
        main_widgets_layout.addWidget(self.phone_edit)

        # Message field
        message_label = QLabel("Template 1:")
        message_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.message_edit = QTextEdit()
        self.message_edit.setPlaceholderText("Message Template 1")  # Add a placeholder text
        self.message_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        message_layout_1 = QVBoxLayout()
        message_layout_1.addWidget(message_label)
        message_layout_1.addWidget(self.message_edit)

        message_label_2 = QLabel("Template 2:")
        message_label_2.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.message_edit_2 = QTextEdit()
        self.message_edit_2.setPlaceholderText("Message Template 2")  # Add a placeholder text
        self.message_edit_2.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        message_layout_2 = QVBoxLayout()
        message_layout_2.addWidget(message_label_2)
        message_layout_2.addWidget(self.message_edit_2)

        # Create a horizontal layout for the first two message fields
        message_row_layout_1 = QHBoxLayout()
        message_row_layout_1.addLayout(message_layout_1)
        message_row_layout_1.addLayout(message_layout_2)

        # Message 3 field
        message_label_3 = QLabel("Template 3:")
        message_label_3.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.message_edit_3 = QTextEdit()
        self.message_edit_3.setPlaceholderText("Message Template 3")  # Add a placeholder text
        self.message_edit_3.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        message_layout_3 = QVBoxLayout()
        message_layout_3.addWidget(message_label_3)
        message_layout_3.addWidget(self.message_edit_3)

        # Message 4 field
        message_label_4 = QLabel("Template 4:")
        message_label_4.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.message_edit_4 = QTextEdit()
        self.message_edit_4.setPlaceholderText("Message Template 4")  # Add a placeholder text
        self.message_edit_4.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field

        message_layout_4 = QVBoxLayout()
        message_layout_4.addWidget(message_label_4)
        message_layout_4.addWidget(self.message_edit_4)

        # Create a horizontal layout for the last two message fields
        message_row_layout_2 = QHBoxLayout()
        message_row_layout_2.addLayout(message_layout_3)
        message_row_layout_2.addLayout(message_layout_4)

        # Add the row layouts to the main layout
        main_widgets_layout.addLayout(message_row_layout_1)
        main_widgets_layout.addLayout(message_row_layout_2)
        
        # Start broadcast button
        self.start_button = QPushButton("Start Broadcast")
        self.start_button.setStyleSheet(
            "background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
        )
        self.start_button.clicked.connect(self.onStartButtonClick)
        main_widgets_layout.addWidget(self.start_button)

        self.main_layout.addWidget(main_widgets_section)

    def onStartButtonClick(self):
        if self.validate_input():
            self.startBroadcast()
        else:
            print("Invalid input")

    def startBroadcast(self):
        
        # Get the user input
        self.start_button.setEnabled(False)
        self.start_button.setText("Loading...")
        self.start_button.setStyleSheet(
            "background-color: #007bff; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
            "cursor: wait;"  # Change the cursor to a wait cursor
        )

        # message = self.message_edit.toPlainText()
        # message2 = self.message_edit_2.toPlainText()
        # message3 = self.message_edit_3.toPlainText()
        # message4 = self.message_edit_4.toPlainText()
        messages = []
        for edit in [self.message_edit, self.message_edit_2, self.message_edit_3, self.message_edit_4]:
            text = edit.toPlainText()
            if text: messages.append(text)

        profiles = []
        for profile in [self.profile_edit, self.profile_edit2, self.profile_edit3, self.profile_edit4]:
            text = profile.text()
            if text: profiles.append(text)

        phone_numbers = self.phone_edit.toPlainText()
        phone_number_list = [phone_number.strip() for phone_number in phone_numbers.replace(',', '\n').split()]
        interval = int(self.message_interval_edit.text())
        user_data_dir = self.user_data_dir_edit.text()
        # profile = self.profile_edit.text()
        # Create a WhatsApp instance
        whatsapp = WhatsApp()

        self.thread_pool = QThreadPool.globalInstance()
        whatsapp_runnable = WhatsAppRunnable(whatsapp, messages, phone_number_list, user_data_dir, profiles, interval)
        whatsapp_runnable.signals.finished.connect(self.on_whatsapp_runnable_finished)
        self.thread_pool.start(whatsapp_runnable)

    def on_whatsapp_runnable_finished(self, status):
        print("WhatsAppRunnable thread finished")
        if status == "success":
            QMessageBox.information(self, "Broadcast Status", "Message sent successfully")
        else:
            QMessageBox.information(self, "Broadcast Status", str(status))
        self.start_button.setEnabled(True)
        self.start_button.setText("Start Broadcast")
        self.start_button.setStyleSheet(
            "background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
            "cursor: wait;"  # Change the cursor to a wait cursor
        )

    def validate_login_input(self):
        # username
        username = self.username_entry.text()
        print(username)
        if not re.match(r"^.{3,50}$", username):
            QMessageBox.critical(self, "Error", "Invalid Username. Username should be between 3 and 50 characters.")
            return False
        
        # password
        password = self.password_entry.text()
        print(password)
        if not re.match(r"^.{8,50}$", password):
            QMessageBox.critical(self, "Error", "Invalid Password. Password should be between 8 and 50 characters.")
            return False
        return True
        
    def validate_input(self):
        # Chrome Profile field
        user_data_dir = self.user_data_dir_edit.text()
        if not re.match(r"^C:\\.*$", user_data_dir):
            QMessageBox.critical(self, "Error", "Invalid Chrome Profile path")
            return False

        message_interval = self.message_interval_edit.text()
        if not re.match(r"^[0-9]+$", message_interval) or int(message_interval) < 15:
            QMessageBox.critical(self, "Error", "Invalid Message interval. Robot speed sent message using 15 second per message.")
            return False
        
        # Profile field
        profile = self.profile_edit.text()
        if not re.match(r"^[a-zA-Z0-9\s]+$", profile):
            QMessageBox.critical(self, "Error", "Invalid Profile name")
            return False

        phone_numbers = self.phone_edit.toPlainText()
        phone_number_pattern = r"^((\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})(,|\s|\n|$))+$"
        if not re.match(phone_number_pattern, phone_numbers):
            QMessageBox.critical(self, "Error", "Invalid Phone Number(s)")
            return False

        # Message field
        message = self.message_edit.toPlainText()
        if not message:
            QMessageBox.critical(self, "Error", "Message cannot be empty")
            return False

        return True