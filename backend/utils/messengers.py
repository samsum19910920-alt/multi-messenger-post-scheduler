import requests
import os
from datetime import datetime

class MessengerBase:
    def __init__(self, bot_token):
        self.bot_token = bot_token
    
    def send_message(self, chat_id, text):
        raise NotImplementedError
    
    def send_photo(self, chat_id, photo_path, caption=None):
        raise NotImplementedError
    
    def send_video(self, chat_id, video_path, caption=None):
        raise NotImplementedError

class RubikaMessenger(MessengerBase):
    API_URL = "https://messengerg2c63.iranlms.ir"
    
    def send_message(self, chat_id, text):
        payload = {
            "bot_api_key": self.bot_token,
            "type": "Text",
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(f"{self.API_URL}/sendMessage", json=payload)
        return response.json()
    
    def send_photo(self, chat_id, photo_path, caption=None):
        with open(photo_path, 'rb') as f:
            files = {'image': f}
            data = {
                "bot_api_key": self.bot_token,
                "chat_id": chat_id,
                "caption": caption or ""
            }
            response = requests.post(f"{self.API_URL}/sendPhoto", data=data, files=files)
        return response.json()

class BaleMessenger(MessengerBase):
    API_URL = "https://tapi.bale.ai"
    
    def send_message(self, chat_id, text):
        url = f"{self.API_URL}/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, json=payload)
        return response.json()
    
    def send_photo(self, chat_id, photo_path, caption=None):
        url = f"{self.API_URL}/bot{self.bot_token}/sendPhoto"
        with open(photo_path, 'rb') as f:
            files = {'photo': f}
            data = {'chat_id': chat_id, 'caption': caption or ""}
            response = requests.post(url, data=data, files=files)
        return response.json()

class EitaaMessenger(MessengerBase):
    API_URL = "https://eitaayar.ir/api"
    
    def send_message(self, chat_id, text):
        url = f"{self.API_URL}/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, json=payload)
        return response.json()

class SorooshMessenger(MessengerBase):
    API_URL = "https://api.soroosh.io"
    
    def send_message(self, chat_id, text):
        url = f"{self.API_URL}/messages/send"
        payload = {
            "to": chat_id,
            "type": "TEXT",
            "body": text,
            "token": self.bot_token
        }
        response = requests.post(url, json=payload)
        return response.json()

def get_messenger(messenger_type, bot_token):
    """
    Factory function to get messenger instance
    """
    messengers = {
        'rubika': RubikaMessenger,
        'bale': BaleMessenger,
        'eitaa': EitaaMessenger,
        'soroosh': SorooshMessenger
    }
    
    if messenger_type not in messengers:
        raise ValueError(f"Unknown messenger type: {messenger_type}")
    
    return messengers[messenger_type](bot_token)
