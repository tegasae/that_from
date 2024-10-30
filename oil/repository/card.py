import abc

from models.domain import PersonOil, Person, Card


class AbstractRepositoryPerson(abc.ABC):
    def __init__(self):
        self.seen = {}
        self.people1c = {}

    def add_card(self, card: Card) -> Card:
        return self._add_card(card)

    def add_log(self, person:PersonOil) -> PersonOil:
        return self._add_log(person)

    def add(self, person: PersonOil) -> PersonOil:
        p = self.get(name=person.name)
        if p.person_id == 0:
            self._add(person=person)
            self.seen[person.name] = person
            p.person_id = person.person_id
        for c in person.cards.keys():
            n = self.add_card(card=person.cards[c])
            p.cards[c] = n
        n = self.add_log(person=p)
        p=n
        self.add_employee(p)
        return p

    def add_employee(self,person:PersonOil):
        self._add_employee(person)
    def get(self, name: str) -> PersonOil:
        if len(self.people1c) == 0:
            self._get1c()
        if name in self.seen:
            return self.seen[name]
        p = self._get(name=name)
        if p.person_id != 0:
            self.seen[name] = p
        return p

    @abc.abstractmethod
    def _add(self, person: PersonOil):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, name: str) -> PersonOil:
        raise NotImplementedError

    @abc.abstractmethod
    def _get1c(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _add_card(self, card: Card) -> Card:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_log(self, person:PersonOil) -> PersonOil:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_employee(self,person:PersonOil):
        raise NotImplementedError
class SqlLiteRepositoryPerson(AbstractRepositoryPerson):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def _add(self, person: PersonOil):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO oil_people (name) VALUES(:name)", {'name': person.name})
        person.person_id = cur.lastrowid

    def _get(self, name: str) -> PersonOil:
        cur = self.conn.cursor()
        cur.execute("SELECT person_id, name FROM oil_people WHERE name=:name", {'name': name})
        result = cur.fetchone()
        if not result:
            return PersonOil(name='')
        return PersonOil(person_id=result[0], name=result[1])

    def _get1c(self):
        cur = self.conn.cursor()
        cur.execute("SELECT employee_id, employee,code1s FROM employees")
        result = cur.fetchall()
        if result:
            for r in result:
                self.people1c[r[0]] = Person(person_id=r[0], name=r[1].strip(), code1s=r[2].strip())

    def _add_card(self, card: Card) -> Card:
        cur = self.conn.cursor()
        cur.execute("SELECT card_id, number FROM oil_cards WHERE number=:number", {'number': card.number})
        r = cur.fetchone()
        if not r:
            cur.execute("INSERT INTO oil_cards (number) VALUES (:number)", {'number': card.number})
            card.card_id = cur.lastrowid
        else:
            card.card_id = r[0]
        return card

    def _add_log(self, person: PersonOil) -> PersonOil:
        cur = self.conn.cursor()

        for k in person.cards.keys():
            i = -1
            for log in person.cards[k].logs:
                i += 1
                cur.execute("SELECT log_id, date_,address FROM oil_logs WHERE card_id=:card_id and date_=:date and address=:address",
                            {'card_id': person.cards[k].card_id,'date':log.date_log,'address':log.address})
                r = cur.fetchone()
                if not r or (log.date_log != r[1] and log.address != r[2]):
                    cur.execute(
                        "INSERT INTO oil_logs (card_id,person_id,date_,address,operation,service,quantity,price) "
                        "VALUES (:number,:person,:date,:address,:operation,:service,:quantity,:price)",
                        {'number': person.cards[k].card_id, 'person': person.person_id, 'date': log.date_log,
                         'address': log.address,
                         'operation': log.operation, 'service': log.service, 'quantity': log.quantity,
                         'price': log.price})
                    person.cards[k].logs[i]=cur.lastrowid
                else:
                    person.cards[k].logs[i].log_id = r[0]
        return person

    def _add_employee(self,person:PersonOil):
        for i in self.people1c.keys():
            if self.people1c[i].short_name()==person.name:
                cur = self.conn.cursor()
                cur.execute(
                    "SELECT employee_id, oil_person_id FROM oil_employee WHERE employee_id=:employee_id AND oil_person_id=:oil_person_id",
                    {'employee_id': i,'oil_person_id': person.person_id})
                r=cur.fetchone()
                if not r:
                    cur.execute("INSERT INTO oil_employee (oil_person_id, employee_id) VALUES (:oil_person_id,:employee_id)", {'oil_person_id':person.person_id,'employee_id':i})
