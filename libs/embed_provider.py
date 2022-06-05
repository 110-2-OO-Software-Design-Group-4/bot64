from discord import Message, Embed, Colour
from libs.message_flag import MessageFlag

def provideEmbed(message: Message, flag: MessageFlag) -> Embed:
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
            return Colour(value=0xffd93d)
        else:
            return Colour(value=0xff6b6b)
    
    author = message.author
    title = provideTitle(flag=flag)
    description = message.content
    timestamp = message.created_at
    color = provideColor(flag=flag)
    
    embed = Embed(title=title,description=description,color=color,timestamp=timestamp)
    embed.set_author(name=author.display_name,icon_url=author.avatar_url)
    return embed