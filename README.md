# Epitor

## But

À chaque nouveau projet, il faut répéter un certain nombre de tâches avant de commencer à travailler. Il faut
initialiser le repo, ajouter un certain nombre de fichiers "de base", et les changer en fonction du nom du
projet, compiler afin de générer un binaire, ajouter un gitignore, mettre dans le binaire ainsi que les
fichiers temporaires, faire un premier commit initial, ouvrir son IDE, ainsi qu'un certain nombre d'autres
tâches toutes aussi importantes, et pourtant tout aussi répétées.

**Epitor** vise à régler ce problème. Il s'agit d'un script léger et simple, mais permettant une grande
customisation. Il peut réaliser les tâches suivantes :

- Créer le dossier contenant le projet
- Initialiser un repo git
- Copier un template de fichier (ceux par défaut ou ceux de l'utilisateur)
- Remplir automatiquement ce template en fonction de variables customisables telles la date, le nom du projet 
  ou de l'utilisateur
- Ajouter les fichiers indésirables dans `.git/info/exclude`, qui est un équivalent local de `.gitignore`
- Compiler le binaire
- Supprimer les traces laissées par la compilation
- Ajouter tous les fichiers du projet à git
- Commit & push le projet
- Ouvrir un IDE tel que Clion ou VScode

Les templates de projets par défaut sont conçus pour être à la fois pratiques et agréables à utiliser.

Par exemple, les Makefile pour les projets en c et cpp possèdent une règle `debug`. De plus, les sources et 
les includes utilisent des wildcards récursives pour ne pas avoir à se soucier d'ajouter chaque fichier et 
dossier dans le bMakefile.

## Installation

Clonez le repo ou téléchargez-le, puis exécutez `./install.sh`

```
install.sh [-h] [-e] [-r]
Install the Epitor script on the system

USAGE:
        -h --help               Display this message
        -o --overwrite-config   Force the installation of template and configuration files, erasing any configuration files that are already present
        -r --remove             Remove the program from the system
```

## Usage

```
usage: epitor [-h] [-q] [-V] [-p] [-P] [-i] [-I] [--ide-path IDE_PATH] {c,cpp} url [name]

This script is intended to initialize and generate a programming project automatically.

positional arguments:
  {c,cpp}              The project language
  url                  The empty repo url
  name                 The name of the project (the name of the repo by default)

optional arguments:
  -h, --help           show this help message and exit
  -q, --quiet          Execute the program quietly (nothing will be displayed)
  -V, --verbose        Execute the program with more information displayed on-screen
  -p, --push           Indicates that the program should commit and push the generation result
  -P, --no-push        Indicates that the program should not commit and push the generation result (silent --push)
  -i, --ide            Indicate that the program should launch the IDE
  -I, --no-ide         Indicate that the program should not launch the IDE (silent --ide)
  --ide-path IDE_PATH  The path of the IDE

Args that start with '--' (eg. -q) can also be set in a config file (/home/Mathis/.config/epitor/config.toml). Config file syntax allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at https://goo.gl/R74nmi). If an arg
is specified in more than one place, then commandline values override config file values which override defaults.

```

## Customisation

Toutes les options de customisation se font dans `~/.config/epitor`.
- `config.toml` permet de passer certains arguments par défaut à epitor
- `gitignore_model.txt` permet de lister les fichiers à exclure de git par défaut
- `variables.toml` permet de modifier les variables de templates disponibles
- `templates/` contient la liste des templates disponibles à l'utilisation, qui sont modifiables

> Vous pouvez aussi modifier facilement le comportement du code en modifiant le fichier 
> `/usr/local/bin/epitor`.

## Futur d'Epitor

- Un système de mise à jour automatique sera bientôt ajouté (il est à noter cependant que celui-ci écrasera
le code précédemment modifié)
- La liste des templates disponibles sera modifiable directement dans les fichiers de configuration
- Plus de languages seront disponibles
- Une meilleure documentation concernant les options de customisation sera disponible
- Le readme sera entièrement en anglais, tout comme le reste du repo.
- Le fichier `install.sh` sera amélioré et un fichier d'installation en ligne sera proposé