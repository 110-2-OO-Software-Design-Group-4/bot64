from discord import Message, DMChannel, TextChannel

def isSelfMessage(self_id: int, message: Message):
    return self_id == message.author.id

def isDMMessage(message: Message):
    return isinstance(message.channel, DMChannel)

def isSpecificChannelMessage(message: Message, channel: TextChannel):
    return message.channel == channel