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

Basic usage

.. code:: py

   from nextcord.ext import commands
   from nextcord.ext import help_commands

   bot = commands.Bot(command_prefix="$", help_command=help_commands.PaginatedHelpCommand())

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
   :target: https://discord.gg/ZebatWssCB
.. |PyPI version info| image:: https://img.shields.io/pypi/v/nextcord-ext-help-commands.svg
   :target: https://pypi.python.org/pypi/nextcord-ext-help-commands
.. |PyPI supported Python versions| image:: https://img.shields.io/pypi/pyversions/nextcord.svg
   :target: https://pypi.python.org/pypi/nextcord
