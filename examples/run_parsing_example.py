import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from comlint.command_line_interface import CommandLineInterface, ParsedCommand


def run_add_command(command: ParsedCommand) -> None:
    print(f'Running add command for file {command.values[0]}')

    if command.flags['--verbose']:
        print(f'Being verbose')
    if command.flags['--interactive']:
        print(f'Adding interactively')


def run_commit_command(command: ParsedCommand) -> None:
    print(f'Running commit command!')

    if command.is_option_used('-m'):
        print(f'Adding message {command.options["-m"]}')
    if command.is_option_used('-c'):
        print(f'Re-editing commit {command.options["-c"]}')
    if command.flags['--amend']:
        print(f'Amending commit')
    if command.flags['--verbose']:
        print(f'Being verbose')


def run_merge_command(command: ParsedCommand) -> None:
    print(f'Running merge command for branches {command.values[0]} and {command.values[1]} using strategy '
          f'{command.options["-s"]}')

    if command.is_option_used('-m'):
        print(f'Adding message {command.options["-m"]}')


def run_submodule_command(command: ParsedCommand) -> None:
    print(f'Running submodule {command.values[0]} command!')

    if command.flags['--verbose']:
        print(f'Being verbose')


if __name__ == '__main__':
    try:
        # create a command line interface which always requires command line arguments
        cli: CommandLineInterface = CommandLineInterface(sys.argv,
                                                         program_name='ExampleApplication',
                                                         description='Example usage of Comlint library basing on some '
                                                                     'git commands',
                                                         allow_no_arguments=False)
        # add "add" command which requires 1 value (it can be any value), has no allowed options and 2 allowed flags (no
        # required options by default)
        cli.add_command('add', 'Add files to commit', num_of_required_values=1, allowed_flags=['--verbose',
                                                                                               '--interactive'])
        # add "commit" command which does not require any value, has 2 allowed options and 2 allowed flags (no required
        # options by default)
        cli.add_command('commit', 'Commit changes', allowed_options=['-m', '-c'], allowed_flags=['--verbose',
                                                                                                 '--amend'])
        # add "merge" command which requires 2 values (these can be any values), has 2 allowed option, no allowed flags
        # and 1 required options
        cli.add_command('merge', 'Merge two branches', num_of_required_values=2, allowed_options=['-s', '-m'],
                        required_options=['-s'])
        # add "submodule command which requires 1 value (it can be either "add" or "update"), has no allowed options and
        # 1 allowed flag (no required options by default)
        cli.add_command('submodule', 'Perform operation on submodule', num_of_required_values=1,
                        allowed_values=['add', 'update'], allowed_flags=['--verbose'])

        # add option "-b" (which can take any value by default)
        cli.add_option('-b', 'Specify branch name')
        # add option "-m" (which can take any value by default)
        cli.add_option('-m', 'Provide message')
        # add option "-c" (which can take any value by default)
        cli.add_option('-c', 'Provide commit hash')
        # add option "-s" which can take one of three allowed values: recursive, resolve or subtree
        cli.add_option('-s', 'Specify merging strategy', allowed_values=['recursive', 'resolve', 'subtree'])

        # add flags
        cli.add_flag('--verbose', 'Show verbose output')
        cli.add_flag('--interactive', 'Add files to commit interactively')
        cli.add_flag('--amend', 'Join to previous commit')

        # obtain parsed command with its properties
        parsed_command: ParsedCommand = cli.parse()

        # use parsed command to perform actions
        if parsed_command.name == 'add':
            run_add_command(parsed_command)
        if parsed_command.name == 'commit':
            run_commit_command(parsed_command)
        if parsed_command.name == 'merge':
            run_merge_command(parsed_command)
        if parsed_command.name == 'submodule':
            run_submodule_command(parsed_command)
    except Exception as e:
        print(e)
