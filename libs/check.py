from discord import Message, DMChannel

def isSelfMessage(self_id: int, message: Message):
    return self_id == message.author.id

def isDMMessage(message: Message):
    return isinstance(message.channel, DMChannel)