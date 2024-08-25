from PyQt5.QtCore import QRunnable

class WhatsAppRunnable(QRunnable):
    def __init__(self, whatsapp, message, phone):
        super().__init__()
        self.whatsapp = whatsapp
        self.message = message
        self.phone = phone

    def run(self):
        self.whatsapp.send_message(self.message, self.phone)