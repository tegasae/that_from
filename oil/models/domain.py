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
    check_summ:float=0

    def checking_summ(self)->bool:
        summ=0
        for i in self.logs:
            summ+=i.price
        if summ==self.check_summ:
            return True
        else:
            return False


@dataclass(kw_only=True)
class PersonOil:
    person_id: int = 0
    name: str
    cards: dict[str, Card] = field(default_factory=dict)


@dataclass(kw_only=True)
class Person:
    person_id:int=0
    name:str
    code1s:str

    def short_name(self):
        n=self.name.split(' ')

        if len(n)!=2 and len(n)!=3:
            raise ValueError(f"{self.name} {len(n)}")
        s_name=n[0]+' '+n[1][0]+"."
        if len(n)==3:
            s_name+=''+n[2][0]+"."
        return s_name

