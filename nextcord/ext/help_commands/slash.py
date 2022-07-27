import itertools
from typing import Callable, Dict, Iterable, List, Optional, Sequence

import nextcord
from nextcord.ext import commands


class SlashHelpCommand:
    """The base implementation for slash help command formatting.

    This class is meant to be subclassed.

    Attributes
    ----------
    interaction: :class:`nextcord.Interaction`
        The interaction that triggered the help command.
    verify_checks: :class:`bool`
        Whether to verify the checks of commands.
    help_command_name: :class:`str`
        The name of the help slash command.
    help_command_description: :class:`str`
        The description of the help slash command.
    """

    def __init__(
        self,
        *,
        verify_checks: bool = True,
        help_command_name: str = "help",
        help_command_description: str = "Shows help for commands",
    ):
        self.verify_checks = verify_checks
        self.help_command_name = help_command_name
        self.help_command_description = help_command_description
        self._interaction: nextcord.Interaction = nextcord.utils.MISSING

    def get_cogs(self, client: nextcord.Client) -> List[nextcord.ClientCog]:
        """Retrieves the cogs for the help command."""
        cogs = client.cogs.values() if isinstance(client, commands.Bot) else client._client_cogs
        return list(cogs)

    def get_bot_mapping(
        self,
    ) -> Dict[Optional[nextcord.ClientCog], List[nextcord.BaseApplicationCommand]]:
        """Retrieves the bot mapping passed to :meth:`send_bot_help`."""
        client = self._interaction.client
        mapping: Dict[Optional[nextcord.ClientCog], List[nextcord.BaseApplicationCommand]] = {
            cog: cog.application_commands for cog in self.get_cogs(client)
        }
        mapping[None] = [c for c in client.get_all_application_commands() if c.parent_cog is None]
        return mapping

    async def filter_commands(
        self,
        commands: Iterable[nextcord.BaseApplicationCommand],
        *,
        sort: bool = False,
        key: Optional[Callable[[nextcord.BaseApplicationCommand], str]] = None,
    ):
        """|coro|

        Returns a filtered list of commands and optionally sorts them.

        This takes into account the :attr:`verify_checks` and :attr:`show_hidden`
        attributes.

        Parameters
        ------------
        commands: Iterable[:class:`nextcord.BaseApplicationCommand`]
            An iterable of commands that are getting filtered.
        sort: :class:`bool`
            Whether to sort the result.
        key: Optional[Callable[:class:`nextcord.BaseApplicationCommand`, Any]]
            An optional key function to pass to :func:`py:sorted` that
            takes a :class:`nextcord.BaseApplicationCommand` as its sole parameter. If ``sort`` is
            passed as ``True`` then this will default as the command name.

        Returns
        ---------
        List[:class:`BaseApplicationCommand`]
            A list of commands that passed the filter.
        """

        if sort and key is None:
            key = lambda c: c.name  # type: ignore

        iterator = commands

        if self.verify_checks is False:
            # if we do not need to verify the checks then we can just
            # run it straight through normally without using await.
            return sorted(iterator, key=key) if sort else list(iterator)  # type: ignore

        if self.verify_checks is None and not self.interaction.guild:
            # if verify_checks is None and we're in a DM, don't verify
            return sorted(iterator, key=key) if sort else list(iterator)  # type: ignore

        # if we're here then we need to check every command if it can run
        async def predicate(cmd: nextcord.BaseApplicationCommand):
            try:
                return await cmd.can_run(self.interaction)
            except nextcord.ApplicationError:
                return False

        ret = []
        for cmd in iterator:
            valid = await predicate(cmd)
            if valid:
                ret.append(cmd)

        if sort:
            ret.sort(key=key)
        return ret

    def get_max_size(self, commands: Sequence[nextcord.BaseApplicationCommand]):
        """Returns the largest name length of the specified command list.

        Parameters
        ------------
        commands: Sequence[:class:`~nextcord.BaseApplicationCommand`]
            A sequence of commands to check for the largest size.

        Returns
        --------
        :class:`int`
            The maximum width of the commands.
        """

        as_lengths = (nextcord.utils._string_width(c.name) for c in commands)  # type: ignore
        return max(as_lengths, default=0)

    def command_not_found(self, string: str):
        """|maybecoro|

        A method called when a command is not found in the help command.
        This is useful to override for i18n.

        Defaults to ``No command called {0} found.``

        Parameters
        ------------
        string: :class:`str`
            The string that contains the invalid command. Note that this has
            had mentions removed to prevent abuse.

        Returns
        ---------
        :class:`str`
            The string to use when a command has not been found.
        """
        return f'No command called "{string}" found.'

    def cog_not_found(self, string: str):
        """|maybecoro|

        A method called when a cog is not found in the help command.
        This is useful to override for i18n.

        Defaults to ``No cog called {0} found.``

        Parameters
        ------------
        string: :class:`str`
            The string that contains the invalid cog. Note that this has
            had mentions removed to prevent abuse.

        Returns
        ---------
        :class:`str`
            The string to use when a cog has not been found.
        """
        return f'No cog called "{string}" found.'

    async def send_bot_help(
        self,
        mapping: Dict[Optional[nextcord.ClientCog], List[nextcord.BaseApplicationCommand]],
    ):
        """|coro|

        Handles the implementation of sending the bot command page in the help command.
        This function is called when the help command is called with no arguments.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method.

        You can override this method to customise the behaviour.

        Parameters
        ----------
        mapping: Dict[Optional[nextcord.ClientCog], List[nextcord.BaseApplicationCommand]]
            A mapping of cogs to their application commands.
        """
        raise NotImplementedError

    async def send_command_help(self, command: nextcord.BaseApplicationCommand):
        """|coro|

        Handles the implementation of sending the command help page in the help command.
        This function is called when the help command is called with a command name.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method.

        You can override this method to customise the behaviour.

        Parameters
        ----------
        command: :class:`~nextcord.BaseApplicationCommand`
            The name of the command to send help for.
        """
        raise NotImplementedError

    async def send_cog_help(self, cog: nextcord.ClientCog):
        """|coro|

        Handles the implementation of sending the cog help page in the help command.
        This function is called when the help command is called with a cog name.

        It should be noted that this method does not return anything -- rather the
        actual message sending should be done inside this method.

        You can override this method to customise the behaviour.

        Parameters
        ----------
        cog: :class:`nextcord.ClientCog`
            The name of the cog to send help for.
        """
        raise NotImplementedError

    async def prepare_help_command(
        self,
        interaction: nextcord.Interaction,
        command_name: Optional[str],
        cog_name: Optional[str],
    ):
        """|coro|

        A low level method that can be used to prepare the help command
        before it does anything. For example, if you need to prepare
        some state in your subclass before the command does its processing
        then this would be the place to do it.

        The default implementation does nothing.

        .. note::

            This is called *inside* the help command callback body. So all
            the usual rules that happen inside apply here as well.

        Parameters
        -----------
        interaction: :class:`nextcord.Interaction`
            The interaction object for the help command.
        command_name: Optional[:class:`str`]
            The argument passed to the help command as a command name.
        cog_name: Optional[:class:`str`]
            The argument passed to the help command as a cog name.
        """
        pass

    async def command_callback(
        self,
        interaction: nextcord.Interaction,
        command_name: Optional[str],
        cog_name: Optional[str] = None,
    ):
        """|coro|

        The actual implementation of the help command.

        It is not recommended to override this method and instead change
        the behaviour through the methods that actually get dispatched.

        - :meth:`send_bot_help`
        - :meth:`send_cog_help`
        - :meth:`send_command_help`
        - :meth:`command_not_found`
        - :meth:`cog_not_found`
        - :meth:`send_error_message`
        - :meth:`on_help_command_error`
        - :meth:`prepare_help_command`
        """
        self._interaction = interaction
        client = interaction.client
        await self.prepare_help_command(interaction, command_name, cog_name)

        if cog_name:
            cog = (
                client.get_cog(cog_name)
                if isinstance(client, commands.Bot)
                else nextcord.utils.find(lambda c: str(c) == cog_name, client._client_cogs)
            )
            if cog is None:
                return await interaction.send(self.cog_not_found(cog_name))
            return await self.send_cog_help(cog)

        if command_name:
            command = nextcord.utils.find(
                lambda c: c.name == command_name, client.get_all_application_commands()
            )
            if command is None:
                return await interaction.send(self.command_not_found(command_name))
            return await self.send_command_help(command)

        await self.send_bot_help(self.get_bot_mapping())

    async def autocomplete_commands(self, interaction: nextcord.Interaction, query: str):
        clean_query = query.replace("/", "").lower().strip()
        application_commands = interaction.client.get_all_application_commands()
        filtered = [
            command.name
            for command in application_commands
            if command.name and command.name.lower().startswith(clean_query)
        ]
        await interaction.response.send_autocomplete(filtered)

    async def autocomplete_cogs(self, interaction: nextcord.Interaction, query: str):
        clean_query = query.lower().strip()
        cogs = [
            getattr(cog, "qualified_name", str(cog)) for cog in self.get_cogs(interaction.client)
        ]
        filtered = [cog for cog in cogs if cog.lower().startswith(clean_query)]
        await interaction.response.send_autocomplete(filtered)

    def add_to_client(self, client: nextcord.Client):
        async def slash_help_with_cogs_func(
            interaction: nextcord.Interaction,
            command: Optional[str] = nextcord.SlashOption(
                description="Command to get help for",
                autocomplete_callback=self.autocomplete_commands,
            ),
            cog: Optional[str] = nextcord.SlashOption(
                description="Cog to get help for",
                autocomplete_callback=self.autocomplete_cogs,
            ),
        ):
            await self.command_callback(interaction, command, cog)

        async def slash_help_no_cogs_func(
            interaction: nextcord.Interaction,
            command: Optional[str] = nextcord.SlashOption(
                description="Command to get help for",
                autocomplete_callback=self.autocomplete_commands,
            ),
        ):
            await self.command_callback(interaction, command)

        slash_help_func = (
            slash_help_with_cogs_func if self.get_cogs(client) else slash_help_no_cogs_func
        )

        slash_help_command = nextcord.slash_command(
            name=self.help_command_name,
            description=self.help_command_description,
        )(slash_help_func)

        client._application_commands_to_add.add(slash_help_command)

    @property
    def interaction(self) -> nextcord.Interaction:
        """:class:`nextcord.Interaction`: The interaction object for the help command."""
        return self._interaction


class MinimalSlashHelpCommand(SlashHelpCommand):
    """A minimal implementation of the :class:`SlashHelpCommand` class.

    Attributes
    ----------
    interaction: :class:`nextcord.Interaction`
        The interaction that triggered the help command.
    sort_commands: :class:`bool`
        Whether to sort the commands in the help command.
    command_heading: :class:`str`
        The heading to use for the command list.
    no_category: :class:`str`
        The heading to use for commands in no category.
    verify_checks: :class:`bool`
        Whether to verify the checks for the help command.
    help_command_name: :class:`str`
        The name of the help slash command.
    help_command_description: :class:`str`
        The description of the help slash command.
    """

    def __init__(
        self,
        *,
        sort_commands: bool = True,
        commands_heading: str = "Commands:",
        no_category: str = "No category",
        verify_checks: bool = True,
        help_command_name: str = "help",
        help_command_description: str = "Shows help for a commands.",
    ):
        self.sort_commands = sort_commands
        self.commands_heading = commands_heading
        self.no_category = no_category
        super().__init__(
            verify_checks=verify_checks,
            help_command_name=help_command_name,
            help_command_description=help_command_description,
        )

    def get_opening_note(self) -> str:
        """Returns help command's opening note. This is mainly useful to override for i18n purposes.

        The default implementation returns ::

            Use `/{command_name} [command]` for more info on a command.
            You can also use `/{command_name} [category]` for more info on a category.

        Returns
        -------
        :class:`str`
            The help command opening note.
        """
        command_name = self.help_command_name
        return (
            f"Type `/{command_name} [command]` for more info on a command.\n"
            f"You can also type `/{command_name} [category]` for more info on a category."
        )

    def get_ending_note(self):
        """Return the help command's ending note. This is mainly useful to override for i18n purposes.

        The default implementation does nothing.

        Returns
        -------
        :class:`str`
            The help command ending note.
        """
        return None

    async def send_bot_help(
        self,
        mapping: Dict[Optional[nextcord.ClientCog], List[nextcord.BaseApplicationCommand]],
    ):
        interaction = self.interaction
        client = interaction.client

        output = ""

        note = self.get_opening_note()
        if note:
            output += f"{note}\n\n"

        if getattr(client, "description", None):
            output += f"{client.description}\n\n"  # type: ignore

        no_category = f"\u200b{self.no_category}:"

        def get_category(
            command: nextcord.BaseApplicationCommand, *, no_category: str = no_category
        ):
            cog = command.parent_cog
            return (
                getattr(cog, "qualified_name", str(cog)) + ":" if cog is not None else no_category
            )

        filtered = await self.filter_commands(
            client.get_all_application_commands(), sort=True, key=get_category
        )
        to_iterate = itertools.groupby(filtered, key=get_category)

        # Now we can add the commands to the page.
        for category, commands in to_iterate:
            commands = (
                sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)  # type: ignore
            )
            if commands:
                joined = "\u2002".join(c.name for c in commands if c.name)
                output += f"__**{category}**__\n"
                output += f"{joined}\n\n"

        note = self.get_ending_note()
        if note:
            output += note

        await interaction.send(output)

    async def send_command_help(self, command: nextcord.BaseApplicationCommand):
        output: str = f"/{command.name}\n\n"
        if command.description:
            output += f"{command.description}\n\n"
        await self.interaction.send(output)

    async def send_cog_help(self, cog: nextcord.ClientCog):
        output = f"{getattr(cog, 'qualified_name', str(cog))}\n\n"
        if getattr(cog, "description", None):
            output += f"{cog.description}\n\n"  # type: ignore
        await self.interaction.send(output)
