from typing import List, Dict
from comlint.command_properties import CommandProperties
from comlint.flag_properties import FlagProperties
from comlint.option_properties import OptionProperties
from comlint.types import CommandName, OptionName, FlagName

Commands = Dict[CommandName, CommandProperties]
Options = Dict[OptionName, OptionProperties]
Flags = Dict[FlagName, FlagProperties]

HELP_COMMAND_NAME: str = 'help'
HELP_OPTION_NAME: str = '-h'
HELP_FLAG_NAME: str = '--help'


class InterfaceHelper:
    @staticmethod
    def is_help_required(argv: List[str], allow_no_arguments: bool) -> bool:
        if len(argv) == 1 and allow_no_arguments:
            return False
        elif len(argv) == 1 and not allow_no_arguments:
            return True
        else:
            return argv[1] == HELP_COMMAND_NAME or argv[1] == HELP_OPTION_NAME or argv[1] == HELP_FLAG_NAME

    @staticmethod
    def get_help(program_name: str, program_description: str, commands: Commands, options: Options, flags: Flags) -> str:
        help_text: str = ''

        help_text += InterfaceHelper.__get_help_header(program_name, program_description)
        help_text += InterfaceHelper.__get_commands_help(commands)
        help_text += InterfaceHelper.__get_options_help(options)
        help_text += InterfaceHelper.__get_flags_help(flags)

        return help_text

    @staticmethod
    def get_hint(similar_values: str) -> str:
        return "" if not similar_values else f' Did you mean:\n{similar_values}'

    @staticmethod
    def __get_help_header(program_name: str, program_description: str) -> str:
        return f'Usage of {program_name}\n' \
               f'{program_description}\n\n'

    @staticmethod
    def __get_commands_help(commands: Commands) -> str:
        help_text: str = 'COMMANDS:\n'

        for command_name, command_properties in commands.items():
            help_text += f'{"{0: <25}".format(command_name)}{command_properties.description}\n'

            if command_properties.allowed_values:
                help_text += f'{"{0: <25}".format("  allowed values")}{command_properties.allowed_values}\n'
            if command_properties.allowed_options:
                help_text += f'{"{0: <25}".format("  allowed options")}{command_properties.allowed_options}\n'
            if command_properties.allowed_flags:
                help_text += f'{"{0: <25}".format("  allowed flags")}{command_properties.allowed_flags}\n'
            if command_properties.required_options:
                help_text += f'{"{0: <25}".format("  required options")}{command_properties.required_options}\n'

            help_text += '\n'

        return help_text

    @staticmethod
    def __get_options_help(options: Options) -> str:
        help_text: str = 'OPTIONS:\n'

        for option_name, option_properties in options.items():
            help_text += f'{"{0: <25}".format(option_name)}{option_properties.description}\n'

            if option_properties.allowed_values:
                help_text += f'{"{0: <25}".format("  allowed values")}{option_properties.allowed_values}\n'

        help_text += '\n'

        return help_text

    @staticmethod
    def __get_flags_help(flags: Flags) -> str:
        help_text: str = 'FLAGS:\n'

        for flag_name, flag_properties in flags.items():
            help_text += f'{"{0: <25}".format(flag_name)}{flag_properties.description}\n'

        return help_text
