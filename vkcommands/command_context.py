import random

from vk_api import VkApi
from vk_api.bot_longpoll import VkBotMessageEvent


class CommandContextVK:
    def __init__(self, command_manager, event: VkBotMessageEvent, args, vk_client: VkApi):
        self.command_manager = command_manager
        self.event = event
        self.args = args
        self.vk_client = vk_client

    def get_command_manager(self):
        return self.command_manager

    def get_event(self):
        return self.event

    def get_args(self):
        return self.args

    def get_vk_client(self):
        return self.vk_client

    def send_message(self, content):
        self.vk_client.get_api().messages.send(user_id=self.event.obj.message['from_id'],
                                               message=content,
                                               random_id=random.randint(0, 2 ** 64))
