import Command


class OptionsParser:

    def __init__(self, given_options: list[str], command: Command.Command, settings: dict):
        self.given_options = given_options
        self.command = command
        self.possible_options = self.command.options

        self.options = None
        self.arguments = None
        self.parse_options()

    def parse_options(self):
        pass

    def get_options(self):
        return self.options

    def get_arguments(self):
        return self.arguments
