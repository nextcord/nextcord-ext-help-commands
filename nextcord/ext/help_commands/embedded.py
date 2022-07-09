from typing import TYPE_CHECKING

from nextcord.ext.commands import Cog, Command, Group, HelpCommand

from nextcord import Embed, Message

if TYPE_CHECKING:
    from typing import Any, Callable, Mapping, Optional, Union

    from nextcord import Context


class EmbeddedHelpCommand(HelpCommand):
    """Custom help command override using embeds"""

    def __init__(self, **options):
        self.cog_heading = options.pop("cog_heading", "Cog Commands:")
        self.group_heading = options.pop("group_heading", "Group Commands:")
        self.command_heading = options.pop("command_heading", "Command:")
        self.dm_help = options.pop("dm_help", False)
        self.no_category = options.pop("no_category", "No Category")

        super().__init__(**options)

    @staticmethod
    def determine_group_or_command(obj: Union[Command, Group]):
        return f"`{obj.name}[group]`" if isinstance(obj, Group) else f"`{obj.name}`"

    async def send_embed(self, emb: Embed):
        return (
            await self.context.author.send(embed=emb)
            if self.dm_help
            else await self.context.send(embed=emb)
        )

    # help
    async def send_bot_help(self, mapping: Mapping) -> Union[Message, None]:
        emb = Embed(
            title=f"**Full command list.** For a detailed guide, check {self.context.clean_prefix}help <name of command>"
        )

        bare_cmd_list = " ".join(
            self.determine_group_or_command(cmd) for cmd in self.context.bot.commands if not cmd.cog
        )
        emb.add_field(name=self.no_category, value=bare_cmd_list, inline=False)

        for cog in self.context.bot.cogs:

            cog = self.context.bot.get_cog(cog)
            if cog is None:
                raise TypeError("cog is None")
            cog_cmds = cog.get_commands()

            cog_cmd_list = " ".join(self.determine_group_or_command(cmd) for cmd in cog_cmds)
            if cog_cmd_list:
                name = f"{cog.qualified_name} {f'| {cog.description}' if cog.description else ''}"
                emb.add_field(name=name, value=cog_cmd_list, inline=False)

        return await self.send_embed(emb)

    # help <cog>
    async def send_cog_help(self, cog: Cog) -> Union[Message, None]:
        emb = Embed(title=self.cog_heading)

        cog_cmds = cog.get_commands()

        cog_cmd_list = " ".join(self.determine_group_or_command(cmd) for cmd in cog_cmds)

        if cog_cmd_list:
            emb.add_field(name=str(cog.qualified_name), value=cog_cmd_list)

        return await self.send_embed(emb)

    # help <group>
    async def send_group_help(self, group: Group) -> Union[Message, None]:
        emb = Embed(title=self.group_heading)

        for sub_command in group.walk_commands():
            syntax = f"{self.context.prefix}{group.qualified_name} {sub_command.name} {sub_command.signature}"
            emb.add_field(
                name=f"{syntax}",
                value=f"`{sub_command.description or 'No description defined.'}`",
                inline=False,
            )

        return await self.send_embed(emb)

    # help <command>
    async def send_command_help(self, command: Command) -> Union[Message, None]:

        syntax = f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        emb = Embed(title=self.command_heading)
        emb.add_field(
            name=syntax, value=f"`{command.description or 'No description defined.'}`", inline=False
        )

        return await self.send_embed(emb)
