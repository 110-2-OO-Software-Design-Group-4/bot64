from discord import Message
from typing import Literal

from libs.message_flag import MessageFlag

async def scanner(message: Message) -> Literal[MessageFlag.Safe, MessageFlag.Suspicious, MessageFlag.Malicious]:
    # TODO: scan the message
    
    return MessageFlag.Safe