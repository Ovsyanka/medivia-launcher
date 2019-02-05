# About

It is the launcher for the Medivia game.

Disclaimer: By now it is just proof of concept to see if it is in demand at all. So the installation process isn't automated well, documentation is poor and etc. You always can reach me on the Medivia Discord server (name: Ovsyanka) if you have questions or suggestions. If you interested in this tool and like to motivate me to improve it - please contact with me.

## Functionality

The main functionality it provides:

* You can have distinct "profiles" of settings (called instancies)
* On each closing of the client launcher saves the game configs and store all the history of changes.

# Installation


You have to install:

* [Python 3.7](https://www.python.org/downloads/)
* [click](https://pypi.org/project/click/)
* [pygit2](https://www.pygit2.org/install.html)

after installing Python run these commands in the command line to install `click` and `pygit2`:

```
pip install --user click
pip install --user pygit2
```

Then [download](https://github.com/Ovsyanka/medivia-launcher/archive/master.zip) the source code from the github and extract it somewhere you like.

# Usage

Run command line in the extracted folder and execute the command:

```
python medivia-launcher.py --executable=<path to the medivia binary> --instance=<instanceName>

# Windows example:
python main.py --executable="C:\Program Files (x86)\Medivia Online\Medivia_OGL.exe" --instance=instance1
```

# Under the hood

When you run the launcher at the first time it creates it's own configuration folder in `$HOME/.medivia-launcher`. It will not make any changes to your medivia client configuration folder `$HOME/.medivia`. Then it copies all content from the medivia client configuration folder `$HOME/.medivia` to the `$HOME/.medivia-launcher/originConfig`.

Each instance has it's own config folder `$HOME/.medivia-launcher/instancies/<instanceName>/`.

When you run the medivia client through the launcher it uses the instance config folder instead of origin client config folder.

TODO: finish the explanation ...

# Known problems

* The config file content have no expliced order. This leads to the big differences in config on each save
* The map file is binary and because of that the size of the repository will grow significantly
