import os
import sys

COMLINT_PY_DIR: str = os.path.dirname(os.path.realpath(__file__))
sys.path.append(COMLINT_PY_DIR)

from .comlint.command_line_interface import CommandLineInterface
