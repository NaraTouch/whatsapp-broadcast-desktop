from PyQt5.QtCore import QRunnable, QObject, pyqtSignal

class WhatsAppRunnableSignals(QObject):
    finished = pyqtSignal()

class WhatsAppRunnable(QRunnable):
    def __init__(self, whatsapp, message, phone):
        super().__init__()
        self.whatsapp = whatsapp
        self.message = message
        self.phone = phone
        self.signals = WhatsAppRunnableSignals()

    def run(self):
        self.whatsapp.send_message(self.message, self.phone)
        self.signals.finished.emit()