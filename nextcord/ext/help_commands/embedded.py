from typing import Mapping, Union

from nextcord.ext.commands import Cog, Command, Group, HelpCommand

from nextcord import Embed, Message


class EmbeddedHelpCommand(HelpCommand):
    """Custom help command override using embeds"""

    def __init__(self, **options):
        self.options = options
        self.dm_help = options.pop("dm_only", False)
        self.default_color = options.pop("default_color", 0xFFFFFF)

        self.main_embed_title = options.pop(
            "main_embed_title", "Overview about Cogs, Groups and Commands"
        )
        self.main_embed_description = options.pop("main_embed_description", "")
        self.main_embed_color = options.pop("main_embed_color", self.default_color)

        self.command_embed_title = options.pop("command_embed_title", "Command help")
        self.command_embed_description = options.pop(
            "command_embed_description",
            "If a parameter is surrounded by `<>`, it is a `required` parameter\nIf a parameter is surrounded by `[]`, it is an `optional` parameter.",
        )
        self.command_embed_color = options.pop("command_embed_color", self.default_color)

        self.group_embed_title = options.pop("group_embed_title", "Group help")
        self.group_embed_description = options.pop("group_embed_description", "")
        self.group_embed_color = options.pop("group_embed_color", self.default_color)

        self.cog_embed_title = options.pop("cog_embed_title", f"Cog help")
        self.cog_embed_description = options.pop("cog_embed_description", "")
        self.cog_embed_color = options.pop("cog_embed_color", self.default_color)

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
    async def send_bot_help(self, mapping: Mapping) -> Message:
        total_command_count = len(self.context.bot.commands)

        self.main_embed_description = self.options.pop("main_embed_description", f"main desc")
        main_embed = Embed(
            title=self.main_embed_title,
            description=self.main_embed_description,
            color=self.main_embed_color,
        )

        bare_cmd_list = " ".join(
            self.determine_group_or_command(cmd) for cmd in self.context.bot.commands if not cmd.cog
        )
        if bare_cmd_list:
            bare_cmd_count = len([x.name for x in self.context.bot.commands if not x.cog])
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
    async def send_command_help(self, command: Command) -> Message:
        syntax = f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        command_embed = Embed(
            title=self.command_embed_title,
            description=self.command_embed_description,
            color=self.command_embed_color,
        )
        command_embed.add_field(
            name=f"`{syntax}`", value=f"`{command.help or 'No description defined.'}`", inline=False
        )

        return await self.send_embed(command_embed)

    # help <group>
    async def send_group_help(self, group: Group) -> Message:
        group_embed = Embed(
            title=self.group_embed_title,
            description=self.group_embed_description,
            color=self.group_embed_color,
        )

        for sub_command in group.walk_commands():
            syntax = f"{self.context.prefix}{group.qualified_name} {sub_command.name} {sub_command.signature}"
            group_embed.add_field(
                name=f"{syntax}",
                value=f"`{sub_command.help or 'No description defined.'}`",
                inline=False,
            )
        group_embed.set_footer(text=f"{len(group.commands)} Sub-Commands")
        return await self.send_embed(group_embed)

    # help <cog>
    async def send_cog_help(self, cog: Cog) -> Message:
        cog_embed = Embed(
            title=self.cog_embed_title,
            description=self.cog_embed_description,
            color=self.cog_embed_color,
        )

        cog_cmds = cog.get_commands()
        cog_cmd_list = " ".join(self.determine_group_or_command(cmd) for cmd in cog_cmds)

        if cog_cmd_list:
            cog_embed.add_field(
                name=f"**{cog.qualified_name} Commands:**", value=cog_cmd_list, inline=False
            )
        cog_embed.set_footer(text=f"{len(cog_cmds)} Cog-Commands")
        return await self.send_embed(cog_embed)
