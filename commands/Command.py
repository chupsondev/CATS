class Command:
    def __init__(self, name: str, description: str, usage: str, aliases: list[str] = None):
        self.name = name
        self.description = description
        self.usage = usage
        self.aliases = aliases

    def getUsage(self):
        return self.usage

    def __str__(self):
        return self.name

    def hasAlias(self, alias: str):
        return alias in self.aliases

    @staticmethod
    def getCommand(alias: str, commands):
        for command in commands:
            if command.hasAlias(alias):
                return command
        return None
