#!/usr/bin/env python3

"""
This script is intended to clone and generate an Epitech C project automatically.
"""

import os
import sys
import traceback
from os import path
from datetime import date
import configargparse
from distutils import dir_util
import toml

home = os.getenv("HOME")

__version__ = "0.1"


def log(message: str, verbosity_level: int = 1):
    """
    Prints a message if the verbosity level is high enough

    :param message: str - the message to print
    :type message: str
    :param verbosity_level: The higher the verbosity level, the more information you'll get, defaults to 1
    :type verbosity_level: int (optional)
    """
    if args.verbosity >= verbosity_level:
        print(message)


def exec_command(command: str):
    """
    Execute the given command and exit if it fails

    :param command: The command to execute
    :type command: str
    """
    if os.system(command) != 0:
        exit(1)


def markup(message, color="fg_default", style="default"):
    """
    This function takes a message and returns it with a markup

    :param message: The message you want to print
    :param style: The style of the text, defaults to default (optional)
    :param color: The color of the text, defaults to fg_default (optional)
    :return: A string with the message and the markup.
    """
    colors = {"bg_black": 40, "bg_red": 41, "bg_green": 42, "bg_orange": 43, "bg_blue": 44, "bg_magenta": 45,
              "bg_cyan": 46, "bg_light_grey": 47, "bg_default": 49, "bg_dark_grey": 100, "bg_light_red": 101,
              "bg_light_green": 102, "bg_yellow": 103, "bg_light_blue": 104, "bg_light_purple": 105, "bg_teal": 106,
              "bg_white": 107, "fg_black": 30, "fg_red": 31, "fg_green": 32, "fg_orange": 33, "fg_blue": 34,
              "fg_magenta": 35, "fg_cyan": 36, "fg_light_grey": 37, "fg_default": 39}
    markups = {"default": 0, "bold": 1, "underline": 4}
    return f"\033[{str(markups[style])};{str(colors[color])}m{str(message)}\033[0m"


def parser_generator():
    """
    It creates a parser object, adds arguments to it, and returns the result of parsing the arguments
    :return: A dictionary containing the arguments of the program.
    """
    parser = configargparse.ArgumentParser(
        default_config_files=[f"{home}/.config/epitor/config.toml"], prog="epitor",
        description='This script is intended to initialize and generate a programming project automatically.')
    parser.add_argument('language', help="The project language", choices=['c', 'cpp'])
    parser.add_argument('url', help='The empty repo url')
    parser.add_argument('name', help='The name of the project (the name of the repo by default)', nargs='?',
                        default=None)
    parser.add_argument('-q', '--quiet', action="store_true",
                        help='Execute the program quietly (nothing will be displayed)')
    parser.add_argument('-V', '--verbose', action="store_true",
                        help='Execute the program with more information displayed on-screen')
    parser.add_argument('-p', '--push', action="store_true",
                        help="Indicates that the program should commit and push the generation result")
    parser.add_argument('-P', '--no-push', action="store_true",
                        help="Indicates that the program should not commit and push the generation result "
                             "(silent --push)")
    parser.add_argument('-i', '--ide', action="store_true",
                        help="Indicate that the program should launch the IDE")
    parser.add_argument('-I', '--no-ide', action="store_true",
                        help="Indicate that the program should not launch the IDE (silent --ide)")
    parser.add_argument('--ide-path', help="The path of the IDE")
    return parser.parse_args()


args = parser_generator()
args.verbosity = 1
if args.verbose:
    args.verbosity = 2
elif args.quiet:
    args.verbosity = 0

variables = toml.load(f"{home}/.config/epitor/variables.toml")

try:
    args.name = args.name or path.splitext(args.url.split('/')[-1])[0]
    working_dir = path.join(os.getcwd(), *args.name.split(path.sep)[:-1])
    args.name = args.name.split(path.sep)[-1].replace(' ', '_')
    log(markup("Entering directory: " + repr(working_dir), 'fg_light_grey'), 2)
    script_dir = path.dirname(path.abspath(__file__))
    log(f"Generating project {markup(repr(args.name), 'fg_green')}...\n")

    os.mkdir(path.join(working_dir, args.name))
    log(f"- Created directory {markup(repr(args.name), 'fg_light_grey')}", 2)
    os.chdir(path.join(working_dir, args.name))
    working_dir = os.getcwd()
    os.chdir(working_dir)
    log(f"- Changed working directory to {markup(repr(working_dir), 'fg_light_grey')}", 2)

    exec_command(f"git init{' -q' if args.verbosity != 2 else ''}")
    exec_command(f"git remote add origin {args.url}")
    log(f"- Repo {markup(repr(args.url), 'fg_light_grey')} initialised")

    dir_util.copy_tree(path.join(f"{home}/.config/epitor/templates", args.language), working_dir)
    log(f"- Copied project template", 2)

    exec_command(f"cp {home}/.config/epitor/gitignore_model.txt {working_dir}/.git/info/exclude")
    log("- Added temporary files to local gitignore", 2)

    for r, d, f in os.walk(working_dir):
        for file in f:
            for var, code in variables.items():
                exec_command(f"sed -i 's/\\${var}\\$/{eval(code)}/g' {path.join(r, file)}")
    log(f"- Filled project files", 2)

    log("- Files generated")

    exec_command(f"make{' &> /dev/null' if args.verbosity != 2 else ''}")
    log(f"- {markup(repr(args.name), 'fg_light_grey')} binary file generated")
    exec_command(f"make clean{' &> /dev/null' if args.verbosity != 2 else ''}")
    log(f"- Object files and temporary files deleted", 2)

    exec_command("git add -A")
    log("- Added files to git", 2)
    if args.push and not args.no_push:
        exec_command(f'git commit -m "📍 Initial commit"{" -q" if args.verbosity != 2 else ""}')
        exec_command(f"git push --set-upstream origin master{' -q' if args.verbosity != 2 else ''}")
        log("- Project committed and pushed")

    log("\n" + markup("✔ Project generated ", style="bold", color="fg_green"))

    if args.ide and not args.no_ide:
        if not args.ide_path:
            raise RuntimeError("The IDE path isn't found. Can't launch the IDE")
        os.system(f"nohup {args.ide_path} {os.getcwd()} >/dev/null 2>&1 &")
        log(markup(repr(args.ide_path) + " launched", 'fg_light_grey'), 2)
except Exception as e:
    traceback.print_exception(type(e), e, e.__traceback__)
    print(markup(e, style="bold", color="fg_red"), file=sys.stderr)
    exit(1)
