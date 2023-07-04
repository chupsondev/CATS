import Command
from option_lib import Option, getOption

SHORT_OPTION = 1
LONG_OPTION = 2


def get_option_type(text: str):
    if text.startswith("--"):
        return LONG_OPTION
    if text.startswith("-"):
        return SHORT_OPTION
    return None


def disable_all_options(options, exclude=None):
    if exclude is None:
        exclude = []
    for opt in options:
        opt: Option = options[opt]
        if opt.getType() is bool and opt.getName() not in exclude:
            opt.setValue(False)

def default_options(options, settings):
    for opt in options:
        opt = options[opt]
        opt.setValue(settings[opt.getName()])  



def parse_option(text: str) -> str:
    return text[1:] if get_option_type(text) == SHORT_OPTION else text[2:]


class OptionsParser:

    def __init__(self, given_options: list[str], command: Command.Command, settings: dict):
        self.cats_settings = settings
        
        self.given_options = given_options
        self.command = command
        self.possible_options = self.command.options

        self.options = self.possible_options
        self.arguments = []
        self.parse_options()


    def parse_options(self):
        options_set = False
        last_option = None
        toggled_options = []
        for arg in self.given_options:
            option_type = get_option_type(arg)
            is_option = option_type is not None
            if not is_option and last_option is None:
                self.arguments.append(arg)
            elif is_option:
                options_set = True
                option = getOption(arg, self.options)
                last_option = option
                option = self.options[option]
                option.setValue(True)
                options_set = True
                toggled_options.append(option.getName())
            elif not is_option and last_option is not None:
                option = self.options[last_option]
                if option.getType() is int:
                    option.setValue(int(arg))
                elif option.getType() is not bool:
                    option.setValue(arg)

        if not toggled_options:
            default_options(self.options, self.cats_settings)
        else:
            disable_all_options(self.options, toggled_options)

    def get_options(self):
        return self.options

    def get_arguments(self):
        return self.arguments
