from discord import Message
from typing import Union

from libs.flag import MessageFlag

async def scanner(message: Message) -> MessageFlag:
    # TODO: scan the message
    
    return MessageFlag.Safe