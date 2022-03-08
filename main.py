#!/usr/bin/env python3

"""
This script is intended to clone and generate a Epitech C project automatically.
"""

import os
import sys
from os import path
from datetime import date
import argparse
from distutils import dir_util


def log(message: str, verbosity_level: int = 1):
    if verbosity >= verbosity_level:
        print(message)


def exec(command: str):
    if os.system(command) != 0:
        exit(1)


def markup(message, style="default", color="fg_default"):
    colors = {"bg_black": 40, "bg_red": 41, "bg_green": 42, "bg_orange": 43, "bg_blue": 44, "bg_magenta": 45,
              "bg_cyan": 46, "bg_light_grey": 47, "bg_default": 49, "bg_dark_grey": 100, "bg_light_red": 101,
              "bg_light_green": 102, "bg_yellow": 103, "bg_light_blue": 104, "bg_light_purple": 105, "bg_teal": 106,
              "bg_white": 107, "fg_black": 30, "fg_red": 31, "fg_green": 32, "fg_orange": 33, "fg_blue": 34,
              "fg_magenta": 35, "fg_cyan": 36, "fg_light_grey": 37, "fg_default": 39}
    markups = {"default": 0, "bold": 1, "underline": 4}
    return f"\033[{str(markups[style])};{str(colors[color])}m{str(message)}\033[0m"


def parser_generator():
    parser = argparse.ArgumentParser(
        description='This script is intended to clone and generate a Epitech C project automatically.')
    parser.add_argument('url', help='The empty repo url')
    parser.add_argument('name', help='The name of the project (the name of the repo by default', nargs='?',
                        default=None)
    parser.add_argument('-q', '--quiet', action="store_true",
                        help='Execute the program quietly (nothing will be displayed)')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Execute the program with more information displayed on-screen')
    parser.add_argument('-p', '--no-push', action="store_true",
                        help="Indicates that the program should not commit and push the repo")
    return parser.parse_args()


args = parser_generator()
verbosity = 1
if args.verbose:
    verbosity = 2
elif args.quiet:
    verbosity = 0
try:
    project_name = args.name if args.name else path.splitext(args.url.split('/')[-1])[0]
    working_dir = path.join(os.getcwd(), *project_name.split(path.sep)[:-1])
    project_name = project_name.split(path.sep)[-1]
    project_name = project_name.replace(' ', '_')
    os.chdir(working_dir)
    log(f"📥 Entering directory: {working_dir}", 2)
    script_dir = path.dirname(path.abspath(__file__))
    log(f"🔨 Generating project '{project_name}'...")
    url = args.url
    should_push = not args.no_push

    os.mkdir(path.join(working_dir, project_name))
    log(f"📂 Created directory '{project_name}'", 2)
    os.chdir(path.join(working_dir, project_name))
    working_dir = os.getcwd()
    log(f"📍 Changed working directory to '{working_dir}'", 2)

    exec(f"git init{' -q' if verbosity != 2 else ''}")
    exec(f"git remote add origin {args.url}")
    log(f"🌐 Repo '{url}' initialised")

    dir_util.copy_tree(path.join(script_dir, 'templates'), working_dir)
    os.mkdir(path.join(working_dir, "subject"))
    log(f"💾 Copied project template", 2)

    for r, d, f in os.walk(working_dir):
        if '.git' in r:
            continue
        for file in f:
            exec(f"sed -i 's/\\$PROJECT_NAME\\$/{project_name}/g' {path.join(r, file)}")
            exec(f"sed -i 's/\\$CURRENT_YEAR\\$/{date.today().year}/g' {path.join(r, file)}")
            exec(f"sed -i 's/\\$FILE_NAME\\$/{file}/g' {path.join(r, file)}")
    log(f"📝 Filled project files", 2)

    log("📑 Files generated")

    exec(f"make{' -s' if verbosity != 2 else ''}")
    log(f"💲 Binary file generated")
    exec(f"make clean{' -s' if verbosity != 2 else ''}")
    log(f"🧹 Object files and temporary files deleted", 2)

    with open(path.join(working_dir, '.git', 'info', 'exclude'), 'a', encoding='utf-8') as f:
        f.write("\n".join([
            os.sep + project_name, os.sep + ".idea", os.sep + ".vscode", "__pychache__", "*.o", "*vgcore*", "*.hi",
            "*.gc*", os.sep + "subject", "*~", "\\#*#", "*.out"
        ]))
    log("⛔ Added temporary files to local gitignore", 2)

    exec("git add -A")
    log("➕ Added files to git", 2)
    if should_push:
        exec(f'git commit -m "📍 Initial commit"{" -q" if verbosity != 2 else ""}')
        exec(f"git push --set-upstream origin master{' -q' if verbosity != 2 else ''}")
        log("📤 Project initialisation committed and pushed")

    log("\n" + markup("✅ Project generated ", style="bold", color="bg_green") + markup("", color="fg_green"))

    os.system(f"nohup clion {os.getcwd()} >/dev/null 2>&1 &")
except Exception as e:
    print(markup(e, style="bold", color="fg_red"), file=sys.stderr)
    exit(1)
