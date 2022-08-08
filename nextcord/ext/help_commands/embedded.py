from typing import Mapping, Optional, Union

from nextcord import Embed, Message
from nextcord.ext import commands


class EmbeddedHelpCommand(commands.HelpCommand):
    """A help command implementation using embeds.
    This inherits from :class:`HelpCommand`.
    It extends it with the following attributes.

    Attributes
    ------------
    dm_help: :class:`bool`
        A bool that indicates if the output should only be sent via DM instead of the channel.
        Defaults to False.
    default_color: :class:`int`
        The default color of all embeds.
        Defaults to 0xFFFFFF (White).
    main_embed_title: :class:`str`
        The title for the embed which gets sent by invoking `help`.
        Defaults to "Overview about Cogs, Groups and Commands".
    main_embed_description: Optional[:class:`str`]
        The description for the embed which gets sent by invoking `help`.
    main_embed_color: Optional[:class:`int`]
        The color for the embed which gets sent by invoking `help`.
        Defaults to default_color.
    command_embed_title: :class:`str`
        The title for the embed which gets sent by `help <command>`.
        Defaults to "Command help".
    command_embed_description: :class:`str`
        The description for the embed which gets sent by invoking `help <command>`.
        Defaults to "If a parameter is surrounded by `<>`, it is a required parameter\nIf a parameter is surrounded by `[]`, it is an optional parameter."
    command_embed_color: Optional[:class:`int`]
        The color for the embed which gets sent by invoking `help <command>`.
        Defaults to default_color.
    group_embed_title: :class:`str`
        The title for the embed which gets sent by invoking `help <group>`.
        Defaults to "Group help".
    group_embed_description: Optional[:class:`str`]
        The description for the embed which gets sent by invoking `help <group>`.
    group_embed_color: Optional[:class:`int`]
        The color for the embed which gets sent by invoking `help <group>`.
        Defaults to default_color.
    cog_embed_title: :class:`str`
        The title for the embed which gets sent by invoking `help <cog>`.
        Defaults to "Cog help".
    cog_embed_description: Optional[:class:`str`]
        The description for the embed which gets sent by invoking `help <cog>`.
    cog_embed_color: Optional[:class:`int`]
        The color for the embed which gets sent by invoking `help <cog>`.
        Defaults to default_color.
    """

    def __init__(
        self,
        *,
        dm_help: bool = False,
        default_color: int = 0xFFFFFF,
        main_embed_title: str = "Overview about Cogs, Groups and Commands",
        main_embed_description: Optional[str] = None,
        main_embed_color: Optional[int] = None,
        command_embed_title: str = "Command help",
        command_embed_description: str = "If a parameter is surrounded by `<>`, it is a required parameter. \\\\n If a parameter is surrounded by `[]`, it is an optional parameter.",
        command_embed_color: Optional[int] = None,
        group_embed_title: str = "Group help",
        group_embed_description: Optional[str] = None,
        group_embed_color: Optional[int] = None,
        cog_embed_title: str = "Cog help",
        cog_embed_description: Optional[str] = None,
        cog_embed_color: Optional[int] = None,
    ):

        self.dm_help = dm_help
        self.default_color = default_color

        self.main_embed_title = main_embed_title
        self.main_embed_description = main_embed_description
        self.main_embed_color = main_embed_color or self.default_color

        self.command_embed_title = command_embed_title
        self.command_embed_description = command_embed_description
        self.command_embed_color = command_embed_color or self.default_color

        self.group_embed_title = group_embed_title
        self.group_embed_description = group_embed_description
        self.group_embed_color = group_embed_color or self.default_color

        self.cog_embed_title = cog_embed_title
        self.cog_embed_description = cog_embed_description
        self.cog_embed_color = cog_embed_color or self.default_color

        super().__init__()

    @staticmethod
    def determine_group_or_command(obj: Union[commands.Command, commands.Group]):
        return f"`{obj.name}[group]`" if isinstance(obj, commands.Group) else f"`{obj.name}`"

    async def send_embed(self, emb: Embed):
        if self.dm_help:
            return await self.context.author.send(embed=emb)
        return await self.context.send(embed=emb)

    # help
    async def send_bot_help(self, mapping: Mapping) -> Message:
        total_command_count = len(self.context.bot.commands)
        main_embed = Embed(
            title=self.main_embed_title,
            description=self.main_embed_description,
            color=self.main_embed_color,
        )

        bare_cmd_list = " ".join(
            self.determine_group_or_command(bare_cmd)
            for bare_cmd in self.context.bot.commands
            if not bare_cmd.cog
        )
        if bare_cmd_list:
            bare_cmd_count = len(
                [bare_cmd.name for bare_cmd in self.context.bot.commands if not bare_cmd.cog]
            )
            main_embed.add_field(name=f"Bare [{bare_cmd_count}]", value=bare_cmd_list, inline=False)

        for cog in self.context.bot.cogs:
            cog = self.context.bot.get_cog(cog)
            cog_cmds = cog.get_commands()
            cog_cmd_list = " ".join(self.determine_group_or_command(cmd) for cmd in cog_cmds)
            if cog_cmd_list:
                main_embed.add_field(
                    name=f"**{cog.qualified_name} Commands [{len(cog_cmds)}]:**",
                    value=cog_cmd_list,
                    inline=False,
                )
        main_embed.set_footer(text=f"{total_command_count} Commands")
        return await self.send_embed(main_embed)

    # help <command>
    async def send_command_help(self, command: commands.Command) -> Message:
        syntax = f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        command_embed = Embed(
            title=self.command_embed_title,
            description=self.command_embed_description,
            color=self.command_embed_color,
        )
        command_embed.add_field(
            name=syntax,
            value=f"`{command.help or command.brief or 'No description provided.'}`",
            inline=False,
        )

        return await self.send_embed(command_embed)

    # help <group>
    async def send_group_help(self, group: commands.Group) -> Message:
        group_embed = Embed(
            title=self.group_embed_title,
            description=self.group_embed_description,
            color=self.group_embed_color,
        )

        for sub_command in group.walk_commands():
            syntax = f"{self.context.clean_prefix}{group.qualified_name} {sub_command.name} {sub_command.signature}"
            group_embed.add_field(
                name=syntax,
                value=f"`{sub_command.help or sub_command.brief or 'No description provided.'}`",
                inline=False,
            )
        group_embed.set_footer(text=f"{len(group.commands)} subcommands")
        return await self.send_embed(group_embed)

    # help <cog>
    async def send_cog_help(self, cog: commands.Cog) -> Message:
        cog_embed = Embed(
            title=self.cog_embed_title,
            description=self.cog_embed_description,
            color=self.cog_embed_color,
        )

        cog_cmds = cog.get_commands()
        for command in cog.walk_commands():
            if not command.parent:
                syntax = f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
                cog_embed.add_field(
                    name=syntax,
                    value=f"`{command.help or command.brief or 'No description provided.'}`",
                    inline=False,
                )

        cog_embed.set_footer(text=f"{len(cog_cmds)} commands")
        return await self.send_embed(cog_embed)
