![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/pawbar94/comlint_py/linux-tests.yml?label=Linux%20tests) ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/pawbar94/comlint_py/windows-tests.yml?label=Windows%20tests) [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

# Comlint for Python
Table of contents:

[What is it?](#what_is_it)<br>
[Conventions used](#conventions_used)<br>
[How to use](#how_to_use)<br>
&emsp;[Creating command line interface](#creating_command_line_interface)<br>
&emsp;&emsp;[Adding commands](#adding_commands)<br>
&emsp;&emsp;[Adding options](#adding_options)<br>
&emsp;&emsp;[Adding flags](#adding_flags)<br>
&emsp;[Parsing command line interface](#parsing_command_line_interface)<br>
&emsp;[Running command line interface](#running_command_line_interface)<br>
[Exceptions you may expect](#exceptions_you_may_expect)<br>

## <a name="what_is_it"></a>What is it?

Comlint is a framework which allows user to create a command line interface (CLI) for Python command line applications in an easy way. It works both on Windows and Linux. If your application is written in C++, check out [Comlint for C++](https://github.com/pawbar94/comlint_cpp).

## <a name="conventions_used"></a>Conventions used

Comlint splits all command line interface elements into 3 categories: **commands**, **options** and **flags**.

**Command** is a keyword specifying an action which should be executed during the application run. Comlint is a command-focused framework, so command is always placed directly after executable name. Command may take a value which details its behavior, but it's not required. For example, when calling `git pull`, _git_ is a program name and _pull_ is a command - command, which does not take any value. Another example may be `git add /some/file.txt`, where _git_ is a program name and _add_ is a command which takes a value which is _/some/file.txt_. So the general scheme of usage is:

`[program_name] [command_name]`

or

`[program_name] [command_name] [command_value]`


**Option** is a keyword which may parametrize command execution. Option is always prefixed with a single dash "-" and always takes a value. For example, calling `pip install -r requirements.txt`, _pip_ is a program name, _install_ is a command and _-r_ is the option which has been given the value _requirements.txt_. Therefore, the general scheme of usage is:

`[program_name] [command_name] [option_name] [option_value]`

**Flag** is a keyword enabling or disabling some functionalities during command execution. It is always prefixed with a double dash "--" and, because it represents a boolean switch, it never takes any value. For example, when calling `git pull --rebase`, _git_ is a program name, _pull_ is a command and _--rebase_ is the flag. The scheme of usage in this case is:

`[program_name] [command_name] [flag_name]`

## <a name="how_to_use"></a>How to use

The basis for all actions is creation of instance of Comlint command line interface object:

```Python
import sys
from comlint.command_line_interface import CommandLineInterface

if __name__ == '__main__':
    cli = CommandLineInterface(sys.argv)
```

Comlint bases on the user command line input, so there is one required constructor's parameters: argv. However, you may customize your command line interface help by providing program name and program description.

```Python
cli = CommandLineInterface(sys.argv, program_name="MyProgram", description="Description of MyProgram")
```

Additionally, you may decide whether you want to allow user to run your program without any input arguments. By default, user is allowed to run application without any input arguments, but if you want to disable it, set `allow_no_arguments` to false:

```Python
cli = CommandLineInterface(sys.argv, allow_no_arguments=False)
```

### <a name="creating_command_line_interface"></a>Creating command line interface

First step to a create command line application is to design an interface by adding supported commands, options and flags.

#### <a name="adding_commands"></a>Adding commands

The easiest way to add a supported command to the interface is by using:

```Python
cli.add_command("command_name", "Command description")
```

By default, such command does not take any value. There are also no options or flags that can be used together with this command. To allow this command to take a single value, use:

```Python
cli.add_command("command_name", "Command description", num_of_required_values=1)
```

Such call means that your command requires one value and it can be any value. If you want the command to accept only one of the predefined values, pass all these allowed values in form of a list as a next argument:

```Python
cli.add_command("command_name", "Command description", allowed_values=["value1", "value2"])
```

In such case, calling both `program.py command_name value1` or `program.py command_name value2` will be ok, but calling `program.py command_name value_3` will result in an error because you defined your command to accept only values _value1_ and _value2_, not _value3_.

A command may be associated with a set of options which are allowed for this particular command. By default, no options are allowed, but you can pass allowed options as a next parameter:

```Python
cli.add_command("command", "Command description", allowed_options=["-a", "-b"])
```

Such code adds a command which can be used together only with 2 options: _-a_ and _-b_. There can be other options supported by the interface, but this particular command can be used only with these two. Similarly in case if you want to add command accepting any value with the same list of allowed options:

```Python
cli.add_command("command", "Command description", num_of_required_values=1, allowed_options=["-a", "-b"])
```

The same when it comes to adding allowed flags:

```Python
cli.add_command("command", "Command description", allowed_flags=["--flag"])
cli.add_command("command", "Command description", num_of_required_values=1, allowed_flags=["--flag"])
```

First of the above lines adds command with no allowed options and one allowed flag _--flag_. Second of the above lines does the same, but for the command accepting any single value.

The last feature is the ability to add required options - in contrast to the allowed options (which **may** be used with a command), required options **must** be used with the particular command. For example:

```Python
cli.add_command("command", "Command description", allowed_options=["-a", "-b"], required_options=["-a"])
```

Command defined in such way has two allowed options (_-a_ and _-b_), but option _-a_ must be used any time the command is called - otherwise an error will be thrown.

#### <a name="adding_options"></a>Adding options

Adding options is very similar to adding commands:

```Python
cli.add_option("-option", "Option description")
```

Such option accepts by default any value. If you want to limit option values which user may pass, provide it in form of a list:

```Python
cli.add_option("-option", "Option description", allowed_values=["value1", "value2"]);
```

#### <a name="flags"></a>Adding flags

Because flags accept no values (see the [Conventions used](#conventions-used)), adding a flag limits to only two parameters - its name and description:

```Python
cli.add_flag("--flag", "Flag description");
```

### <a name="parsing_command_line_interface"></a>Parsing command line interface

After the definition of the command line interface is ready, you can parse the input provided by the user, calling:

```Python
parsed_command = cli.parse()
```

In this way, you will be given a structure which contains:
* command name used by the user
* command values provided by the user
* map of options, where key is the option name and value is option value
* map of flags, where key is the flag name and value is bool flag indicating whether flag was used or not

You are able to check whether an option has been used by the user by calling:

```Python
if parsed_command.is_option_used("-option"):
    # option used!
```

In case of flags, you don't have to check for their presence before the usage because flags which were not used by the user have assigned _false_ value.

```Python
parsed_command.flags["--flag"] # this returns false if --flag was not used, true otherwise
```

For more advanced example of command parsing, check _examples/parsing_example_main.Python_ file.

### <a name="running_command_line_interface"></a>Running command line interface

To make things easier, Comlint offers one more way to handle user input arguments - automatic command handler execution. Developer may implement his/her own class implementing logic which should be executed after user calls one of the supported commands in the constructed command line interface. Such class must derive from `CommandHandlerInterface` class and implement `run(command: ParsedCommand)` method. Code in this implementation will be executed automatically whenever user uses the corresponding command. Let's say we implement such class:

```Python
class SomeCommandHandler(CommandHandlerInterface)
    def run(self, command: ParsedCommand) -> None:
        print("Running logic for some command!")
```

And then in main we define command line interface as follows:

```Python
cli.add_command("some_command", "Some command description")
cli.add_command_handler("some_command", SomeCommandHandler())
```

Having that set up, we can call:

```Python
cli.run()
```

This one line will automatically call `run` method from `SomeCommandHandler` class whenever user calls `program.py some_command`.

For more advanced example of automatic command running, check _examples/running_example_main.Python_ file.

## <a name="exceptions_you_may_expect"></a>Exceptions you may expect
* `DuplicatedCommand` - you're trying to add a command to the interface which has been already added
* `DuplicatedFlag` - you're trying to add a flag to the interface which has been already added
* `DuplicatedOption` - you're trying to add an option to the interface which has been already added
* `ForbiddenFlag` - user used flag which is generally supported by the interface, but not allowed to use with the associated command
* `ForbiddenOptionValue` - user provided a value for the option which is not on the list of the allowed values for that option
* `ForbiddenOption` - user used option which is generally supported by the interface, but not allowed to use with the associated command
* `InvalidCommandHandler` - something's wrong with the command handler that you're trying to register (most probably it's a nullptr)
* `InvalidCommandName` - you're trying to add a command to the interface which has invalid name (most probably it begins with "-" or "--")
* `InvalidCommandPosition` - supported and valid command name has been found, but it's not directly after program name
* `InvalidFlagName` - you're trying to add a flag to the interface which has invalid name (most probably it doesn't start with "--" or starts with "-")
* `InvalidOptionName` - you're trying to add an option to the interface which has invalid name (most probably it doesn't start with "-" or starts with "--")
* `MissingCommandHandler` - you used `cli.Run()` method, but the user provided command for which no command handler has been registered
* `MissingCommandValue` - user called your program with a command which requires value(s), but the sufficient number of values has not been provided
* `MissingOptionValue` - user used an option, but gave it no value
* `MissingRequiredOption` - user called a command without an option which has been defined as a required one for that command
* `UnsupportedCommandValue` - user provided a value for the command which is not on the list of the allowed values for that command
* `UnsupportedCommand` - user called a command which was not added to the interface
* `UnsupportedFlag` - user used a flag which was not added to the interface
* `UnsupportedOption` - user used option which was not added to the interface



[![Stargazers repo roster for @pawbar94/comlint_py](https://reporoster.com/stars/pawbar94/comlint_py)](https://github.com/pawbar94/comlint_py/stargazers)
[![Forkers repo roster for @pawbar94/comlint_py](https://reporoster.com/forks/pawbar94/comlint_py)](https://github.com/pawbar94/comlint_py/network/members)
