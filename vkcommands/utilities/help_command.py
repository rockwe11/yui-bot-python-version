from vkcommands.command_context import CommandContextVK


class HelpCommand:
    def handle(self, ctx: CommandContextVK):
        if len(ctx.get_args()) > 0:
            command_name = ctx.get_args()[0]
            command = ctx.command_manager.get_command(command_name)
            if command:
                ctx.send_message(command.get_help())
            else:
                ctx.command_manager.send_no_command(ctx.get_event())
        else:
            text_to_send = "📚 Список доступных команд:\n\n"
            for command in ctx.command_manager.commands:
                text_to_send += command.getName() + "\n"
            ctx.send_message(text_to_send)

    def getName(self):
        return "help"

    def get_help(self):
        return "Данная команда показывает список команд бота.\n\n" \
               "Использование: help [Название команды]"
