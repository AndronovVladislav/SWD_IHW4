from enum import Enum


class OrderStatus(Enum):
    CREATED = 'CA'
    IN_QUEUE = 'IQ'
    IN_PROGRESS = 'IN'
    READY = 'RE'

    DELETED = 'DE'


STATUS_TRANSITIONS = {
    'CA': 'IQ',
    'IQ': 'IN',
    'IN': 'RE',
}
