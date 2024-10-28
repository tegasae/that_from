from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class Log:
    log_id: int = 0
    date_log: datetime
    address: str
    operation: str
    service: str
    quantity: float
    price: float

    def __eq__(self, other):
        if (self.date_log == other.date_log and self.operation == other.operation and self.service == other.service and
                self.quantity == other.quantity and self.price == other.price):
            return True
        else:
            return False


@dataclass(kw_only=True)
class Card:
    card_id: int = 0
    number: str
    logs: list[Log] = field(default_factory=list)


@dataclass(kw_only=True)
class Person:
    person_id: int = 0
    name: str
    cards: dict[str, Card] = field(default_factory=dict)
