<<<<<<< HEAD
=======
from dataclasses import dataclass, field
from datetime import datetime

>>>>>>> origin/main
import openpyxl

import pyexcel as p
import re

<<<<<<< HEAD
from models.domain import Log, Card, Person
=======

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

>>>>>>> origin/main

xls_file = 'oil_september.xls'
xlsx_file = 'oil_september.xlsx'

# Convert XLS to XLSX
p.save_book_as(file_name=xls_file, dest_file_name=xlsx_file)

dataframe = openpyxl.load_workbook("oil_september.xlsx")
datasheet = dataframe.worksheets[0]

people: dict[str, Person] = {}

empty_lines = 0
i = 1
while empty_lines < 30:
    card_number = datasheet.cell(row=i, column=2).value
    name = datasheet.cell(row=i, column=5).value
    i += 1

    if type(card_number) is not str:
        empty_lines += 1
        continue
    if re.match('^\d{5,}', card_number):
        if type(name) is str and not name in people.keys():
            p = Person(name=name)
            people[p.name] = p

            if not card_number in people[p.name].cards.keys():
                people[p.name].cards[card_number] = Card(number=card_number)

        while True:

            date = datasheet.cell(row=i, column=3).value
            if not date:
                break
            #date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
            address = datasheet.cell(row=i, column=5).value
            operation = datasheet.cell(row=i, column=6).value
            service = datasheet.cell(row=i, column=7).value
            quanity = datasheet.cell(row=i, column=8).value
            price = datasheet.cell(row=i, column=9).value
            log = Log(date_log=date, address=address, operation=operation, service=service, quantity=quanity,
                      price=price)

            #print(p)
            if not log in people[p.name].cards[card_number].logs:
                people[p.name].cards[card_number].logs.append(log)

            i += 1


for i in people.keys():
    print(people[i])
    # print(f"{people[i]} {people[i].cards}")

