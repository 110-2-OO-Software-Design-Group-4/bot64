from typing import Union, Optional
import random
from discord import Embed, User, Member, Color
from datetime import datetime

def create_embed(
    title: Optional[str]=None,
    color: Optional[str]=None,
    description: Optional[str]=None,
    fields: Optional[dict]=None,
    author: Optional[Union[User, Member]]=None,
    image: Optional[str]=None,
    thumbnail: Optional[str]=None,
    inline: bool=True):
    
    footer_prefix = ''
    embed_kwargs = dict()

    if title != None:
        embed_kwargs['title'] = title
    
    if color != None:
        if color == 'random':
            color = Color(value=random.randint(0x000000, 0xFFFFFF))
        embed_kwargs['color'] = color
    
    if description != None:
        embed_kwargs['description'] = description

    embed = Embed(**embed_kwargs)

    if fields != None:
        for key, value in fields.items():
            embed.add_field(name=key, value=value, inline=inline)
    
    if author != None:
        embed.set_author(name=f'{author.display_name}#{author.discriminator}', icon_url=author.avatar_url)
        footer_prefix = f'ID: {author.id} • '
    
    if image != None:
        embed.set_image(image)
    
    if thumbnail != None:
        embed.set_thumbnail(thumbnail)

    embed.set_footer(text=footer_prefix + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + ' (UTC+0)')
    return embed