from PyQt5.QtCore import QRunnable, QObject, pyqtSignal

class WhatsAppRunnableSignals(QObject):
    finished = pyqtSignal(str)

class WhatsAppRunnable(QRunnable):
    def __init__(self, whatsapp, messages, phone_number_list, user_data_dir, profiles, interval):
        super().__init__()
        self.whatsapp = whatsapp
        self.messages = messages
        self.phone_number_list = phone_number_list
        self.user_data_dir = user_data_dir
        self.profiles = profiles
        self.interval = interval
        self.signals = WhatsAppRunnableSignals()

    def run(self):
        status = self.whatsapp.send_message(self.messages, self.phone_number_list, self.user_data_dir, self.profiles, self.interval)
        self.signals.finished.emit(status)