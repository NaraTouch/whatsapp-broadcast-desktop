from PyQt5.QtCore import QRunnable, QObject, pyqtSignal

class LoginRunnableSignals(QObject):
    finished = pyqtSignal(object)

class LoginRunnable(QRunnable):
    def __init__(self, api, username, password):
        super().__init__()
        self.api = api
        self.username = username
        self.password = password
        self.signals = LoginRunnableSignals()
        self.api.finished.connect(self.on_api_finished)  # Connect the signal to a slot

    def run(self):
        self.api.api_login(self.username, self.password)

    def on_api_finished(self, response):
        self.signals.finished.emit(response)  # Emit the signal