import time
from vkcommands.command_context import CommandContextVK


class PingCommand:
    def handle(self, ctx: CommandContextVK):
        ctx.send_message(f"Пинг: {'{:.2f}'.format(time.time() - int(ctx.get_event().message['date']))} сек.")

    def getName(self):
        return "ping"

    def get_help(self):
        return "Данная команда показывает задержку между сервером и ботом.\n\n" \
               "Использование: ping"
