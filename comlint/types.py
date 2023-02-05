from typing import List, Dict

CommandName = str
OptionName = str
FlagName = str

OptionNames = List[OptionName]
FlagNames = List[FlagName]

CommandValue = str
CommandValues = List[CommandValue]
OptionValue = str
OptionValues = List[OptionValue]
OptionsMap = Dict[OptionName, OptionValue]
FlagsMap = Dict[FlagName, bool]

ANY: List[str] = []
NONE: List[str] = []
