import os, json
import Command


class Settings:
    def __init__(self, commands: list[Command.Command], global_settings, settingsPath):
        self.commands = commands
        self.global_settings = global_settings
        self.settings = Settings.loadSettings(commands, global_settings, settingsPath)

    @staticmethod
    def loadSettings(commands, global_settings, settingPath):
        if not os.path.exists(settingPath):
            Settings.createDefaultSettings(commands, global_settings, settingPath)
        return json.load(open(settingPath, "r"))

    @staticmethod
    def createDefaultSettings(commands, global_settings, settingsPath):
        settings = {}
        for global_setting in global_settings:
            settings[global_setting] = global_settings[global_setting]
        for command in commands:
            commandObject = commands[command]
            commandName = commandObject.getName()
            commandOptions = commands[command].getOptions()
            settings[commandName] = {}
            for option in commandOptions:
                optionObject = commandOptions[option]
                optionName = optionObject.getName()
                settings[commandName][optionName] = optionObject.defaultValue
        open(settingsPath, "w").write(json.dumps(settings, indent=4))


class Setting:  # a class for a setting, and option that is not specified in the command line, but in settings
    pass
