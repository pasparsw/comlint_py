from comlint.types import CommandName, OptionName, FlagName

OPTION_PREFIX: str = '-'
FLAG_PREFIX: str = '--'
MIN_COMMAND_NAME_LENGTH: int = 1
MIN_OPTION_NAME_LENGTH: int = 2
MIN_FLAG_NAME_LENGTH: int = 3


class InterfaceValidator:
    @staticmethod
    def is_command_name_valid(command_name: CommandName) -> bool:
        return len(command_name) >= MIN_COMMAND_NAME_LENGTH and command_name[0] != OPTION_PREFIX

    @staticmethod
    def is_option_name_valid(option_name: OptionName) -> bool:
        return len(option_name) >= MIN_OPTION_NAME_LENGTH and option_name[0] == OPTION_PREFIX \
               and option_name[:2] != FLAG_PREFIX

    @staticmethod
    def is_flag_name_valid(flag_name: FlagName) -> bool:
        return len(flag_name) >= MIN_FLAG_NAME_LENGTH and flag_name[:2] == FLAG_PREFIX
