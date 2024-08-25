
import re
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
                             QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QThreadPool
from .whatsapp import WhatsApp
from .whatsapp_runnable import WhatsAppRunnable
from PyQt5.QtGui import QIcon

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WhatsApp Broadcast")
        self.setWindowIcon(QIcon("resources/icons/app_icon.png"))
        # self.setGeometry(300, 300, 400, 350)  # Increased height to accommodate larger widgets
        self.setMaximumSize(1600, 1200)
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add some padding around the layout

        # Chrome Profile field
        user_data_dir_label = QLabel("Chrome Profile:")
        user_data_dir_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.user_data_dir_edit = QLineEdit()
        self.user_data_dir_edit.setPlaceholderText(r"EX: C:\Users\User\AppData\Local\Google\Chrome\User Data")
        self.user_data_dir_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        layout.addWidget(user_data_dir_label)
        layout.addWidget(self.user_data_dir_edit)

        # Profile field
        profile_label = QLabel("Profile:")
        profile_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.profile_edit = QLineEdit()
        self.profile_edit.setPlaceholderText("EX: Profile 3")  # Add a placeholder text
        self.profile_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        layout.addWidget(profile_label)
        layout.addWidget(self.profile_edit)

        # Message field
        phone_label = QLabel("Phone Numbers:")
        phone_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.phone_edit = QTextEdit()
        self.phone_edit.setPlaceholderText("EX:\n +855xxxxxx\n +855xxxxxx\n +855xxxxxx\n +855xxxxxx")
        self.phone_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        layout.addWidget(phone_label)
        layout.addWidget(self.phone_edit)

        # Message field
        message_label = QLabel("Message:")
        message_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.message_edit = QTextEdit()
        self.message_edit.setPlaceholderText("Enter message")  # Add a placeholder text
        self.message_edit.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 5px;")  # Add some styling to the edit field
        layout.addWidget(message_label)
        layout.addWidget(self.message_edit)
        
        # Start broadcast button
        self.start_button = QPushButton("Start Broadcast")
        self.start_button.setStyleSheet(
            "background-color: #4CAF50; color: #fff; padding: 10px 20px; border: none; border-radius: 5px;"
        )
        # self.start_button.clicked.connect(self.startBroadcast)
        self.start_button.clicked.connect(self.onStartButtonClick)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def onStartButtonClick(self):
        if self.validate_input():
            self.startBroadcast()
        else:
            print("Invalid input")

    def startBroadcast(self):
        
        # Get the user input
        self.start_button.setEnabled(False)
        self.start_button.setText("Loading...")

        message = self.message_edit.toPlainText()
        # phone = self.phone_edit.text()
        phone_numbers = self.phone_edit.toPlainText()
        phone_number_list = [phone_number.strip() for phone_number in phone_numbers.replace(',', '\n').split()]
        
        user_data_dir = self.user_data_dir_edit.text()
        profile = self.profile_edit.text()
        # Create a WhatsApp instance
        whatsapp = WhatsApp()

        self.thread_pool = QThreadPool.globalInstance()
        whatsapp_runnable = WhatsAppRunnable(whatsapp, message, phone_number_list, user_data_dir, profile)
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

    def validate_input(self):
        # Chrome Profile field
        user_data_dir = self.user_data_dir_edit.text()
        if not re.match(r"^C:\\.*$", user_data_dir):
            QMessageBox.critical(self, "Error", "Invalid Chrome Profile path")
            return False

        # Profile field
        profile = self.profile_edit.text()
        if not re.match(r"^[a-zA-Z0-9\s]+$", profile):
            QMessageBox.critical(self, "Error", "Invalid Profile name")
            return False

        # # Phone Number field
        # phone_number = self.phone_edit.text()
        # if not re.match(r"^(\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9})$", phone_number):
        #     QMessageBox.critical(self, "Error", "Invalid Phone Number")
        #     return False
        # Phone Number field
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