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
