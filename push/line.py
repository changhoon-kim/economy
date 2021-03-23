import requests

# $ curl -XPOST -H 'Content-Type:application/json; charset=UTF-8' -H 'Authorization:Bearer hYvzzb3VcyRMp+fG8Ou+5gnJzqpyyu58hIkTB3e+AXNCzJgyCJdfTuCsbzEEYtjM1nlApTA33E5UJ/HZlWHm75U/OwkvME1cDtVieFWT6kWIiw635wyFK0ECaml7t2rlQM3Fz+3z3Q0XbNWyq3pXvwdB04t89/1O/w1cDnyilFU=' -H 'X-Line-Bot-Id:U2666e44fa78fbbeb22eb7f988984c321' 'https://api.line.me/v2/bot/message/push' -d '{"to":"Uaa089c22e244706a96f9c703ae10a3ca", "messages":[{"type":"text", "text":"test"}]}'

class Line:
    def __init__(self):
        self.url = 'https://api.line.me/v2/bot/message/push'
        self.token = 'hYvzzb3VcyRMp+fG8Ou+5gnJzqpyyu58hIkTB3e+AXNCzJgyCJdfTuCsbzEEYtjM1nlApTA33E5UJ/HZlWHm75U/OwkvME1cDtVieFWT6kWIiw635wyFK0ECaml7t2rlQM3Fz+3z3Q0XbNWyq3pXvwdB04t89/1O/w1cDnyilFU='
        self.bot_id = 'U2666e44fa78fbbeb22eb7f988984c321'
        self.user_id = 'Uaa089c22e244706a96f9c703ae10a3ca'
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer %s'%self.token,
            'X-Line-Bot-Id': self.bot_id,
        }

    def push(self, text):
        data = {
            'to': self.user_id,
            'messages':[{
                'type': 'text',
                'text': text,
            }]
        }

        r = requests.post(self.url, headers=self.headers, json=data).json()

        #TODO: logging
