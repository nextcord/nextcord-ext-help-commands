Documentation for nextcord-ext-help-commands
============================================

|Discord server invite| |PyPI version info| |PyPI supported Python versions|

A Nextcord extension for pre-built custom help commands for prefix commands and slash commands.

Installing
----------

.. code:: py

   pip install -U nextcord-ext-help-commands

To use pagination help commands:

.. code:: py

   pip install -U nextcord-ext-help-commands[menus]

Basic help command usage
------------------------

.. code:: py

   from nextcord.ext import commands
   from nextcord.ext import help_commands

   intents = nextcord.Intents.default()
   intents.message_content = True

   bot = commands.Bot(
      command_prefix="$",
      intents=intents,
      help_command=help_commands.PaginatedHelpCommand(),
   )

   bot.run("token")

Slash help command usage
------------------------

.. code:: py

   from nextcord.ext import commands
   from nextcord.ext import help_commands

   # An instance of nextcord.Client may be used instead of commands.Bot
   bot = commands.Bot()

   # Pass your Bot or Client instance to the add_to_client method
   help_commands.MinimalSlashHelpCommand().add_to_client(bot)

   bot.run("token")


Contents
--------

.. toctree::
   :maxdepth: 2

   ext/help_commands/api

License
-------

| Copyright (c) 2022-Present The Nextcord Developers


.. |Discord server invite| image:: https://discord.com/api/guilds/881118111967883295/embed.png
   :target: https://discord.gg/nextcord
.. |PyPI version info| image:: https://img.shields.io/pypi/v/nextcord-ext-help-commands.svg
   :target: https://pypi.python.org/pypi/nextcord-ext-help-commands
.. |PyPI supported Python versions| image:: https://img.shields.io/pypi/pyversions/nextcord.svg
   :target: https://pypi.python.org/pypi/nextcord
