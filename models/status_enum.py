from enum import Enum

class StatusEnum(Enum):
    RUMORED = 'Rumored',
    PLANNED = 'Planned',
    IN_PRODUCTION = 'In Production',
    POST_PRODUCTION = 'Post Production',
    RELEASED = 'Released',
    CANCELLED = 'Cancelled'