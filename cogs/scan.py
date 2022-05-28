from discord import Message
from discord.ext.commands import Cog, Bot

from libs.check import isDMMessage, isSelfMessage
from libs.message_flag import MessageFlag
from libs.scanner import scanner

class Scan(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    async def handleSuspiciousMessage(self, message: Message) -> None:
        pass

    async def handleMaliciousMessage(self, message: Message) -> None:
        pass
    
    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if isSelfMessage(self_id=self.bot.user.id, message=message):
            return None
        elif isDMMessage(message=message):
            return None
        
        await message.channel.send(content=message.content)

        flag = await scanner(message=message)
        print(flag) # debug

        if flag == MessageFlag.Safe:
            pass
        elif flag == MessageFlag.Suspicious:
            await self.handleSuspiciousMessage(message=message)
        elif flag == MessageFlag.Malicious:
            await self.handleMaliciousMessage(message=message)

def setup(bot: Bot) -> None:
    bot.add_cog(Scan(bot))