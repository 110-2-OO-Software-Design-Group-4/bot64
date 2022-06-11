from discord import Message, Embed, Colour, TextChannel
from typing import List
from libs.message_flag import MessageFlag

class LogMessage():
    def __init__(self, message: Message, flag: MessageFlag) -> None:
        self.embed = LogMessage._provideEmbed(message=message,flag=flag)
    
    async def sendLogMessage(self, channel:TextChannel) -> None:
        await channel.send(embed=self.embed)

    @staticmethod
    def _provideEmbed(message: Message, flag: MessageFlag) -> Embed:
        def provideTitle(flag: MessageFlag) -> str:
            if flag == MessageFlag.Safe:
                return 'Raw Message:'
            elif flag == MessageFlag.Suspicious:
                return 'Suspicious Raw Message:'
            else:
                return 'Malicious Raw Message:'
        
        def provideColor(flag: MessageFlag) -> Colour:
            if flag == MessageFlag.Safe:
                return Colour(value=0x6bcb77)
            elif flag == MessageFlag.Suspicious:
                return Colour(value=0xf9d923)
            else:
                return Colour(value=0xeb5353)
        
        title = provideTitle(flag=flag)
        description = message.content
        color = provideColor(flag=flag)
        timestamp = message.created_at
        
        author = message.author
        
        fieldTitle = 'Message Link'
        fieldValue = '[Click me]' + '(' + message.jump_url + ')'

        embed = Embed(title=title,description=description,color=color,timestamp=timestamp)
        embed.set_author(name=author.display_name,icon_url=author.avatar_url)
        embed.add_field(name=fieldTitle,value=fieldValue)
        return embed