import json
import discum
import time
from datetime import datetime, timedelta
import random
import pytz
import threading

class Post:
    def __init__(self, token, channel_ID, warp_name, MIN_delay, MAX_delay, advertisements, delete):
        self.bot = discum.Client(token=token)
        self.channel_ID = channel_ID
        self.warp_name = warp_name
        self.MIN_delay = int(MIN_delay) * 60
        self.MAX_delay = int(MAX_delay) * 60
        self.advertisements = advertisements.split(';')
        if delete == 'да':
            self.delete = True
        elif delete == 'нет':
            self.delete == False
        
        while True:
            last_message_id = None
            messages = self.bot.getMessages(channelID=self.channel_ID, num=100, beforeDate=last_message_id)
            messages = messages.text
            messages = messages.replace('\\n', '')
            messages = messages.replace('\\"', '')
            messages = messages.encode().decode("unicode-escape")
            messages = messages.replace('\\', '')

            messages = json.loads(messages)

            message_founded = False
            for j in messages:
                if not message_founded: 
                    if j['author'].get('id') == '618536577282342912':
                        content = j['content']
                        if content.find(self.warp_name) != -1:
                            print('Найдено упоминание варпа: ' + j['content'])
                            message_founded = True
                            message_timestamp = j['timestamp']
                last_message_id = j['id']

            if message_founded:
                message_founded = False
                last_message_id = None

                message_time = datetime.strptime(message_timestamp, '%Y-%m-%dT%H:%M:%S.%f+00:00')
                
                timezone = pytz.timezone('Europe/Moscow')
                time_now = datetime.now(timezone)
                time_now = time_now - timedelta(hours=3)
                time_now = time_now.replace(tzinfo=None)
                
                if message_time < time_now - timedelta(minutes=10):
                    sended_message = self.bot.sendMessage(channelID=self.channel_ID, message=random.SystemRandom().choice(self.advertisements))
                    sended_message = sended_message.text.encode().decode('unicode-escape')
        
                    time.sleep(10)
                    sended_message_json = json.loads(sended_message.replace('\\', ''))
                    if self.delete:
                        self.bot.deleteMessage(channelID=self.channel_ID, messageID=sended_message_json['id'])
                    time.sleep(random.randint(self.MIN_delay, self.MAX_delay))
                else:
                    wait = message_time - time_now + timedelta(minutes=10)
                    time.sleep(wait.total_seconds())
                    time.sleep(random.randint(self.MIN_delay, self.MAX_delay))

            else:
                time.sleep(1)

number_of_channels = input('Введите количество каналов для отправки: ')
number_of_channels = int(number_of_channels)

for i in range(number_of_channels):
    threading.Thread(
        name='thread_' + str(i),
        target=Post, 
        args=(
            input('Введите Ваш Discord-токен: '),
            input('Введите ID канала для отправки: '),
            input('Введите имя рекламируемого Вами варпа: '),
            input('Введите минимальный промежуток между сообщениями (в минутах): '), 
            input('Введите максимальный промежуток между сообщениями (в минутах): '), 
            input('Введите рекламу (можно ввести несколько текстов через ; ): '),
            input('Удалять сообщения после отправки? (да/нет): '), 
        ),
    ).start()