#!/bin/sh

# Version 0.1

if [ "$1" == "--help" ] || [ "$1" == "-h" ]
then
  echo -e "install.sh [-h] [-e] [-r]
Install the Epitor script on the system

USAGE:
\t-h --help\t\tDisplay this message
\t-o --overwrite-config\tForce the installation of template and configuration files, erasing any configuration files that are already present
\t-r --remove\t\tRemove the program from the system"
  exit
fi

if [ "$1" == "--remove" ] || [ "$1" == "-r" ]
then
  echo "Removing Epitor..."
  rm -rf /usr/local/bin/epitor
  echo "Epitor removed!"
  echo "Do you want to remove the configuration files? [y/n]"
  read -r res
  if [ "$res" == "y" ] || [ "$res" == "Y" ] || [ "$res" == "yes" ] || [ "$res" == "Yes" ] || [ "$res" == "YES" ]
  then
    rm -rf ~/.config/epitor
    echo "Configuration files removed!"
  fi
  exit
fi

echo "Installing Epitor..."
pip3 install -r requirements.txt 1> /dev/null
cp -f main.py /usr/local/bin/epitor
if [ "$1" == "--overwrite-config" ] || [ "$1" == "-o" ]
then
  cp -Trf data ~/.config/epitor
else
  cp -Trn data ~/.config/epitor
fi

echo "Epitor installed! You can modify the default configuration and the templates in ~/.config/epitor"
echo "To use it, just call the 'epitor' command"
echo "usage: epitor [-h] [-q] [-V] [-p] [-i] [--ide-path IDE_PATH] {c,cpp} url [name]"