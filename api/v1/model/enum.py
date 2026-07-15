from enum import Enum


class AttendeeType(str, Enum):
    VIP = "vip"
    WORKER = "worker"
    NORMAL_GUEST = "normal-guest" 