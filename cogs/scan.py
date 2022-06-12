from discord import Message, Guild, RawReactionActionEvent
from discord.utils import get
from discord.ext.commands import Cog, Bot
from libs.check import isDMMessage, isSelfMessage, isSpecificChannelMessage
from libs.log_message import LogMessage
from libs.message_flag import MessageFlag
from libs.scanner import scanner

class Scan(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.bot_category = None
        self.bot_channel = None
    
    async def handleSuspiciousMessage(self, message: Message) -> None:
        pass

    async def handleMaliciousMessage(self, message: Message) -> None:
        pass

    async def createBotChannelsIfNotExist(self, guild: Guild) -> None:
        self.bot_category = get(guild.categories, name='BOT CHANNELS')
        if self.bot_category is None:
            self.bot_category = await guild.create_category('BOT CHANNELS')
        self.bot_channel = get(guild.text_channels, name='logs', category=self.bot_category)
        if self.bot_channel is None:
            self.bot_channel = await guild.create_text_channel('logs', category=self.bot_category)
    
    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        await self.createBotChannelsIfNotExist(guild=message.guild)

        if isSelfMessage(self_id=self.bot.user.id, message=message):
            return None
        if isDMMessage(message=message):
            return None
        if isSpecificChannelMessage(message=message, channel=self.bot_channel):
            return None
        
        flag = await scanner(message=message)
        print(flag) # debug
       
        logMessage = LogMessage(message=message,flag=flag)
        await logMessage.sendLogMessage(channel=self.bot_channel)

        if flag == MessageFlag.Safe:
            pass
        elif flag == MessageFlag.Suspicious:
            await self.handleSuspiciousMessage(message=message)
        elif flag == MessageFlag.Malicious:
            await self.handleMaliciousMessage(message=message)
    
    @Cog.listener()
    async def on_raw_reaction_add(self,payload: RawReactionActionEvent) -> None:
        await self.createBotChannelsIfNotExist(guild=self.bot.get_guild(payload.guild_id))

        # Trigger action only when the added reaction is in the logs channel AND the message is an embed.
        if payload.channel_id != self.bot_channel.id:
            return None
        message = await self.bot_channel.fetch_message(payload.message_id)
        if len(message.embeds) == 0:
            return None
        
        # TODO: Execute specific action based on the added reaction (emoji).
        # If you need to get user's id, you can get it from footer. (See log_message.py for detail)
        print(message.embeds[0].footer.text) #debug

def setup(bot: Bot) -> None:
    bot.add_cog(Scan(bot))