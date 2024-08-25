
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
        self.setGeometry(300, 300, 400, 350)  # Increased height to accommodate larger widgets

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add some padding around the layout

        # Phone Number field
        phone_label = QLabel("Phone Number:")
        phone_label.setStyleSheet("font-weight: bold; font-size: 12pt;")  # Make the label bold and larger
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Enter phone number")  # Add a placeholder text
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
        self.start_button.clicked.connect(self.startBroadcast)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def startBroadcast(self):
        # Get the user input
        self.start_button.setEnabled(False)
        self.start_button.setText("Loading...")

        message = self.message_edit.toPlainText()
        phone = self.phone_edit.text()

        # Create a WhatsApp instance
        whatsapp = WhatsApp()

        # Create a QThread to perform the Selenium operations
        self.thread_pool = QThreadPool.globalInstance()
        whatsapp_runnable = WhatsAppRunnable(whatsapp, message, phone)
        sender = self.thread_pool.start(whatsapp_runnable)
        print(sender)
        if sender:
            QMessageBox.information(self, "Broadcast Status", sender)
            self.start_button.setEnabled(True)
            self.start_button.setText("Start Broadcast")