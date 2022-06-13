# bot64

## Members

- B07902108 翁祖毅
- （其他人自己加）

## Introduction

- Bot64 is a discord bot which monitors and filters dirty words and phishing links.
- Each message sent in the guild are examined by Bot64 and marked with 3 mutual exclusive flags: `Safe`, `Suspicious` or `Malicious`.
- For those discord members sending messages marked with the last 2 flags, i.e. `Suspicious` or `Malicious`, Bot64 would exert penalties on them according to the policies set by the guild administrators.
- Possible policies are `Ignore`, `Mute`, `Kick` or `Ban`.
    - `Ignore`: Bot64 simply ignores this behavior.
    - `Mute`: if the mute role is set, Bot64 would add the role to the discord member.
    - `Kick`: Bot64 kicks the discord member out of the guild. He/She can rejoin the guild at any time.
    - `Ban`: Bot64 bans the discord member. He/She cannot rejoin the guild before unbanned.

## Deployment

- Please provide the following environment variables:
    - `BOT_TOKEN`: Discord Bot Token. You can create one at [Discord Developer Portal](https://discord.com/developers/applications).
    - `MONGO_URL`: MongoDB connection URL. (In development stage, we use [MongoDB Atlas](https://www.mongodb.com) free tier to test our bot.)
- Run the following commands in your terminal:
```sh
git clone https://github.com/110-2-OO-Software-Design-Group-4/bot64.git
cd bot64
pip install -r requirements.txt
cp .env.example .env # Please add environment variables in '.env'
python3 main.py
```
## Caveats

- You need to invite the discord bot into a guild to make it works!
- Bot64 needs at least the following permissions: `MANAGE_ROLES`, `KICK_MEMBERS` and `BAN_MEMBERS` to work correctly.
- If you choose to set the mute role, please make sure Bot64 has a higher role than the mute role. Otherwise, it could not add the mute role to the discord member, due to Discord's default limit.
- You are responsible for setting the mute role properly to deny the discord members with the mute role to send messages in any channel.
