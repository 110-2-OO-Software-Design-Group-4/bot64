import sys
from discord import Message
from discord.utils import get
from discord.ext.commands import Cog, Bot, Context, CommandError, group, guild_only, has_guild_permissions

from libs.check import is_dm_message, is_self_message, is_integer
from libs.log_message import LogMessage
from libs.flag import MessageFlag
from libs.scanner import scanner
from libs.database import Database
from libs.embed import create_embed
class Scan(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.bot_category = None
        self.bot_channel = None
        self.db = Database()
    
    async def handleSuspiciousMessage(self, message: Message) -> None:
        pass

    async def handleMaliciousMessage(self, message: Message) -> None:
        pass

    # TODO: Do we really need dependency on message in order to create channels?
    async def createBotChannels(self, message: Message) -> None:
        guild = message.guild
        self.bot_category = get(guild.categories, name='BOT CHANNELS')
        if self.bot_category is None:
            self.bot_category = await guild.create_category('BOT CHANNELS')
        self.bot_channel = get(guild.text_channels, name='logs', category=self.bot_category)
        if self.bot_channel is None:
            self.bot_channel = await guild.create_text_channel('logs', category=self.bot_category)
    
    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        # await self.createBotChannels(message=message)

        if is_self_message(self_id=self.bot.user.id, message=message):
            return None
        elif is_dm_message(message=message):
            return None
        
        flag = await scanner(message=message)
        print(flag) # debug
       
        # logMessage = LogMessage(message=message,flag=flag)
        # await logMessage.sendLogMessage(channel=self.bot_channel)

        if flag == MessageFlag.Safe:
            pass
        elif flag == MessageFlag.Suspicious:
            await self.handleSuspiciousMessage(message=message)
        elif flag == MessageFlag.Malicious:
            await self.handleMaliciousMessage(message=message)
    
    @group()
    @guild_only()
    @has_guild_permissions(administrator=True)
    async def config(self, ctx: Context) -> None:
        """[Bot64 configurations]"""

        if ctx.invoked_subcommand == None:
            await ctx.send_help(ctx.command)

    @config.command()
    async def show(self, ctx: Context) -> None:
        """[Shows Bot64 scanner configurations in this guild]"""

        guild_id = ctx.guild.id
        guild_config = self.db.get_guild_config(guild_id=guild_id)
        del guild_config['_id']

        embed = create_embed(title='Guild Config', color='random', fields=guild_config, author=ctx.author, inline=False)
        await ctx.send(embed=embed)
    
    @config.command()
    async def log_channel(self, ctx: Context, channel_id: str=None) -> None:
        """<channel_id> [Sets log channel]"""

        if channel_id == None:
            await ctx.send_help(ctx.command)
            return
        elif not is_integer(channel_id):
            await ctx.send('`channel_id` must be an integer (without sign).')

        channel_id = int(channel_id)
        self.db.set_log_channel_id(guild_id=ctx.guild.id, log_channel_id=channel_id)
        await self.show(ctx)
    
    @config.command()
    async def timeout(self, ctx: Context, seconds: str=None) -> None:
        """<seconds> [Sets timeout seconds]"""

        if seconds == None:
            await ctx.send_help(ctx.command)
            return
        elif not is_integer(seconds):
            await ctx.send('`seconds` must be an integer (without sign).')

        seconds = int(seconds)
        self.db.set_timeout_seconds(guild_id=ctx.guild.id, timeout_seconds=seconds)
        await self.show(ctx)

    @config.error
    async def config_error(self, ctx: Context, error: CommandError):
        exception = error.original
        print(exception, file=sys.stderr)
        await ctx.send(f'An error occurred:\n```{str(exception)}```')

def setup(bot: Bot) -> None:
    bot.add_cog(Scan(bot))