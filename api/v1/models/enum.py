from enum import Enum

class AttendeeType(str, Enum):
    vip = "vip"
    worker = "worker"
    normal-guest = "normal-guest" 