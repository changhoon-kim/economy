import requests

class Telegram:
    def __init__(self):
        self.token = '1649233790:AAG3t7IqU1uQvooVmNh85UnGzKlL3acQ_eQ'
        self.chatid = '1651959619'

    def push(self, text):
        url = 'https://api.telegram.org/bot%s/sendmessage?chat_id=%s&text=%s' %(self.token, self.chatid, text)

        r = requests.get(url).json()

        #TODO: logging
