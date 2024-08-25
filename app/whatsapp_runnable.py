from PyQt5.QtCore import QRunnable, QObject, pyqtSignal

class WhatsAppRunnableSignals(QObject):
    finished = pyqtSignal(str)

class WhatsAppRunnable(QRunnable):
    def __init__(self, whatsapp, message, phone, user_data_dir, profile):
        super().__init__()
        self.whatsapp = whatsapp
        self.message = message
        self.phone = phone
        self.user_data_dir = user_data_dir
        self.profile = profile
        self.signals = WhatsAppRunnableSignals()

    def run(self):
        status = self.whatsapp.send_message(self.message, self.phone, self.user_data_dir, self.profile)
        self.signals.finished.emit(status)