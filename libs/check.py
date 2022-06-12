from discord import Message, DMChannel

def is_self_message(self_id: int, message: Message):
    return self_id == message.author.id

def is_dm_message(message: Message):
    return isinstance(message.channel, DMChannel)

def is_integer(value: str):
    for c in value:
        if not c.isdigit():
            return False
    return True