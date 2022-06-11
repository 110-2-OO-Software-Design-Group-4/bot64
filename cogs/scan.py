from discord import Message
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
        await self.createBotChannels(message=message)

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

def setup(bot: Bot) -> None:
    bot.add_cog(Scan(bot))