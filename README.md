# nextcord-ext-help-commands

[![Discord server invite](https://img.shields.io/discord/881118111967883295?color=blue&label=discord)](https://discord.gg/nextcord)
[![PyPI version info](https://img.shields.io/pypi/v/nextcord-ext-help-commands.svg)](https://pypi.python.org/pypi/nextcord-ext-help-commands)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/nextcord.svg)](https://pypi.python.org/pypi/nextcord)
[![Nextcord-ext-help-commands Documentation](https://img.shields.io/readthedocs/nextcord-ext-help-commands.svg)](https://nextcord-ext-help-commands.readthedocs.io)

A Nextcord extension for pre-built custom help commands for prefix commands and slash commands.

## Installing

### Requirements

**Python 3.8 or higher is required**

It is necessary to first install [Nextcord](https://github.com/nextcord/nextcord)

Then install the extension by running one of the following commands:

```py
# Linux/macOS
python3 -m pip install -U nextcord-ext-help-commands

# Windows
py -3 -m pip install -U nextcord-ext-help-commands
```

To make use of pagination help commands, you must also install [nextcord-ext-menus](https://github.com/nextcord/nextcord-ext-menus).

```py
# Linux/macOS
python3 -m pip install -U "nextcord-ext-help-commands[menus]"

# Windows
py -3 -m pip install -U nextcord-ext-help-commands[menus]
```

## Basic Usage

```py
from nextcord.ext import commands
from nextcord.ext import help_commands

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    help_command=help_commands.PaginatedHelpCommand()
)

bot.run("token")
```

## Links

- [Documentation](https://nextcord-ext-help-commands.readthedocs.io/en/latest/)
- [Official Discord server](https://discord.gg/nextcord)

## License

Copyright (c) 2022-Present The Nextcord Developers
