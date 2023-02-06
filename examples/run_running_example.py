import sys
import os
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from comlint.command_line_interface import CommandLineInterface, CommandHandlerInterface, CommandValues, OptionsMap, \
    FlagsMap


class AddCommandHandler(CommandHandlerInterface):
    def run(self, values: CommandValues, options: OptionsMap, flags: FlagsMap) -> None:
        print(f'Running add command for file {values[0]}')

        if flags['--verbose']:
            print(f'Being verbose')
        if flags['--interactive']:
            print(f'Adding interactively')


class CommitCommandHandler(CommandHandlerInterface):
    def run(self, values: CommandValues, options: OptionsMap, flags: FlagsMap) -> None:
        print(f'Running commit command!')

        if '-m' in options.keys():
            print(f'Adding message {options["-m"]}')
        if '-c' in options.keys():
            print(f'Re-editing commit {options["-c"]}')
        if flags['--amend']:
            print(f'Amending commit')
        if flags['--verbose']:
            print(f'Being verbose')


class MergeCommandHandler(CommandHandlerInterface):
    def run(self, values: CommandValues, options: OptionsMap, flags: FlagsMap) -> None:
        print(f'Running merge command for branches {values[0]} and {values[1]} using strategy '
              f'{options["-s"]}')

        if '-m' in options.keys():
            print(f'Adding message {options["-m"]}')


class SubmoduleCommandHandler(CommandHandlerInterface):
    def run(self, values: CommandValues, options: OptionsMap, flags: FlagsMap) -> None:
        print(f'Running submodule {values[0]} command!')

        if flags['--verbose']:
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

        # add command handlers
        cli.add_command_handler('add', AddCommandHandler())
        cli.add_command_handler('commit', CommitCommandHandler())
        cli.add_command_handler('merge', MergeCommandHandler())
        cli.add_command_handler('submodule', SubmoduleCommandHandler())

        # run command provided by the user from the command line
        cli.run()
    except Exception as e:
        print(f'{traceback.format_exc()}')
