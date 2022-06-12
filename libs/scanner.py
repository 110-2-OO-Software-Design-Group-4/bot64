from discord import Message

from libs.flag import MessageFlag

class Scanner:
    def __init__(self) -> None:
        pass

    def scan(self, message: Message) -> MessageFlag:
        # TODO: scan the message
        
        return MessageFlag.Safe