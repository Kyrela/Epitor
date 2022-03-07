#!/usr/bin/env python3

"""
This script is intended to clone and generate a Epitech C project automatically.
"""

import os
from os import path
from datetime import date
import argparse


def log(message: str, verbosity_level: int = 1):
    if verbosity >= verbosity_level:
        print(message)


parser = argparse.ArgumentParser(
    description='This script is intended to clone and generate a Epitech C project automatically.')
parser.add_argument('url', help='The empty repo url')
parser.add_argument('name', help='The name of the project (the name of the repo by default', nargs='?', default=None)
parser.add_argument('-v', '--verbose', metavar='level', type=int, choices=[0, 1, 2],
                    help='The verbosity level, (from 0 to 2). 0 if non-precised, 1 if only the flag is included',
                    nargs='?', default=0)
args = parser.parse_args()


verbosity = args.verbose if args.verbose is not None else 1
project_name = args.name if args.name else path.splitext(args.url.split('/')[-1])[0]
working_dir = path.join(os.getcwd(), *project_name.split(path.sep)[:-1])
project_name = project_name.split(path.sep)[-1]
project_name = project_name.replace(' ', '_')
os.chdir(working_dir)
log(f"Entering directory: {working_dir}", 2)
script_dir = path.dirname(path.abspath(__file__))
log(f"Generating project '{project_name}'...")
url = args.url

os.mkdir(path.join(working_dir, project_name))
log(f"Created directory '{project_name}'", 2)
os.chdir(path.join(working_dir, project_name))
log(f"Changed working directory to '{os.getcwd()}'", 2)

os.system(f"git init{' -q' if verbosity != 2 else ''}")
os.system(f"git remote add origin {args.url}")
log(f"Repo '{url}' initialised")


os.mkdir(path.join(working_dir, project_name, "subject"))
log(f"Created directory 'subject'", 2)
os.mkdir(path.join(working_dir, project_name, "src"))
log(f"Created directory 'src'", 2)
#os.mkdir(path.join(working_dir, project_name, ".idea"))
log(f"Created directory '.idea'", 2)

os.system(f"cp {path.join(script_dir, 'templates', 'main.c')} {path.join(working_dir, project_name, 'src', 'main.c')}")
os.system(f"sed -i 's/\\$PROJECT_NAME\\$/{project_name}/g' {path.join(working_dir, project_name, 'src', 'main.c')}")
os.system(f"sed -i 's/\\$CURRENT_YEAR\\$/{date.today().year}/g' {path.join(working_dir, project_name, 'src', 'main.c')}")
os.system(f"sed -i 's/\\$FILE_NAME\\$/main.c.c/g' {path.join(working_dir, project_name, 'src', 'main.c')}")
log(f"Generated 'main.c.c' in 'src'", 2)

os.system(f"cp {path.join(script_dir, 'templates', 'Makefile')} {path.join(working_dir, project_name, 'Makefile')}")
os.system(f"sed -i 's/\\$PROJECT_NAME\\$/{project_name}/g' {path.join(working_dir, project_name, 'Makefile')}")
os.system(f"sed -i 's/\\$CURRENT_YEAR\\$/{date.today().year}/g' {path.join(working_dir, project_name, 'Makefile')}")
log(f"Generated 'Makefile'", 2)

#os.system(f"cp {path.join(script_dir, 'templates', 'discord.xml')} "
 #         f"{path.join(working_dir, project_name, '.idea', 'discord.xml')}")
log(f"Generated configuration files", 2)

log("Files generated")

os.system(f"make{' -s' if verbosity != 2 else ''}")
os.system(f"make clean{' -s' if verbosity != 2 else ''}")
log(f"Binary file generated")

log("--- Project generated ---")


os.system(f"nohup clion {os.getcwd()} 2> /dev/null &")
