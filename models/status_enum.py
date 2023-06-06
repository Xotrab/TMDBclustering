from enum import Enum

class StatusEnum(Enum):
    RUMORED = 0,
    PLANNED = 1,
    IN_PRODUCTION = 2,
    POST_PRODUCTION = 3,
    RELEASED = 4,
    CANCELLED = 5