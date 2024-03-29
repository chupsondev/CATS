import option_lib


class Command:
    def __init__(self, name: str, description: str, usage: str, aliases: list[str], function=None,
                 options: list[option_lib.Option] = None, global_settings=dict(), local_settings=dict()):
        self.name = name
        self.description = description
        self.usage = usage
        self.aliases = aliases
        self.function = function
        self.options = options
        self.global_settings = global_settings
        self.local_settings = local_settings

    def getUsage(self):
        return self.usage

    def getName(self):
        return self.name

    def __str__(self):
        return self.name

    def hasAlias(self, alias: str):
        return alias in self.aliases

    @staticmethod
    def getCommand(alias: str, commands):
        for command in commands:
            if commands[command].hasAlias(alias):
                return command
        return None

    def setFunction(self, function):
        self.function = function

    def run(self, args, settings=None, location=None):
        self.function(args, settings, location)

    def getOptions(self):
        return self.options
