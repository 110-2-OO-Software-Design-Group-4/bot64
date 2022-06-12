from enum import IntEnum

class MessageFlag(IntEnum):
    Safe = 1
    Suspicious = 2
    Malicious = 3

class PenaltyPolicyFlag(IntEnum):
    Ignore = 1
    Timeout = 2
    Kick = 3
    Ban = 4