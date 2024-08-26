
import requests
from PyQt5.QtCore import pyqtSignal, QObject

class Api(QObject):
    finished = pyqtSignal(object)  # Define the signal

    def __init__(self):
        super().__init__()
        self.api_url = "https://whatsapp-broadcast-api.vercel.app"
        self.api_key = "MDAzYmY2ZmY0MzAiLCJpYXQiOjE3MTUwMTEyNzEsImV4cCI6MTcxNT"

    def api_login(self, username, password):
        url = f"{self.api_url}/auth/login"  
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {"username": username, "password": password}

        try:
            api = requests.post(url, headers=headers, json=data, timeout=30)
            api.raise_for_status()  
            response = api.json()
            if response:
                self.finished.emit(response)  # Emit the signal
                return response
            else:
                response = {
                    'message': 'No response from server',
                    'statusCode': 204  
                }
                self.finished.emit(response)  # Emit the signal
                return response
        except requests.exceptions.RequestException as e:
            response = {
                'message': 'Internal server error',
                'statusCode': 500
            }
            self.finished.emit(response)  # Emit the signal
            return response
        except ValueError:
            response = {
                'message': 'Invalid JSON response',
                'statusCode': 500
            }
            self.finished.emit(response)  # Emit the signal
            return response