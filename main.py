#!/usr/bin/env python3

"""
This script is intended to clone and generate a Epitech C project automatically.
"""

import os
from os import path
from datetime import date
import argparse
from distutils import dir_util


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
working_dir = os.getcwd()
log(f"Changed working directory to '{working_dir}'", 2)

os.system(f"git init{' -q' if verbosity != 2 else ''}")
os.system(f"git remote add origin {args.url}")
log(f"Repo '{url}' initialised")

dir_util.copy_tree(path.join(script_dir, 'templates'), working_dir)
os.mkdir(path.join(working_dir, "subject"))
log(f"Copied project template", 2)

for r, d, f in os.walk(working_dir):
    if '.git' in r:
        continue
    for file in f:
        os.system(f"sed -i 's/\\$PROJECT_NAME\\$/{project_name}/g' {path.join(r, file)}")
        os.system(f"sed -i 's/\\$CURRENT_YEAR\\$/{date.today().year}/g' {path.join(r, file)}")
        os.system(f"sed -i 's/\\$FILE_NAME\\$/{file}/g' {path.join(r, file)}")
log(f"Filled project files", 2)

log("Files generated")

os.system(f"make{' -s' if verbosity != 2 else ''}")
os.system(f"make clean{' -s' if verbosity != 2 else ''}")
log(f"Binary file generated")

with open(path.join(working_dir, '.git', 'info', 'exclude'), 'a', encoding='utf-8') as f:
    f.write(os.sep + project_name)
log("Excluded binary file", 2)

log("--- Project generated ---")

os.system(f"nohup clion {os.getcwd()} >/dev/null 2>&1 &")
