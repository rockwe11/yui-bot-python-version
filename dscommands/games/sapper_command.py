from dscommands.command_context import CommandContext


class SapperCommand:
    numbers = [
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣"
    ]

    sessions = []

    async def handle(self, ctx: CommandContext):
        pass

    def getName(self):
        return "sapper"
