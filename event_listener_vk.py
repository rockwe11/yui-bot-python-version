import random
import threading

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent

from command_manager_vk import CommandManagerVK
from data import db_session
from data.users import User


class ListenerVK:
    def __init__(self, longpoll, vk_session):
        self.longpoll = longpoll
        self.vk_session = vk_session
        self.command_manager = CommandManagerVK(vk_session)

    def message_listener(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                threading.Thread(target=self.on_message, args=(event,)).start()

    def on_message(self, event: VkBotMessageEvent):
        db_sess = db_session.create_session()
        user_id = event.message['from_id']
        user = db_sess.query(User).filter(User.vid == user_id).first()
        if user:
            user.coins += 5
            db_sess.commit()
        # content = event.obj.message['text']
        # if content.startswith(.prefix):
        db_sess.close()
        self.command_manager.handle(event)
        # print(event)
        # print('Новое сообщение:')
        # print('Для меня от:', event.obj.message['from_id'])
        # print('Текст:', event.obj.message['text'])
        # vk = self.vk_session.get_api()
        # vk.messages.send(user_id=event.obj.message['from_id'],
        #                  message="Спасибо, что написали нам. Мы обязательно ответим",
        #                  random_id=random.randint(0, 2 ** 64))
