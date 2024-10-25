import abc
from dataclasses import asdict

from loader.domain.model import UrgencyTicket
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryUrgencyTicket(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, urgency_ticket:UrgencyTicket):
        try:
            p = self.get(descr=urgency_ticket.descr)
            # partner=p
        except InvalidRecord:
            self._add(urgency_ticket)
            self.seen[urgency_ticket.descr] = urgency_ticket
        status = self.seen[urgency_ticket.descr]
        return self.seen[urgency_ticket.descr]

    def get(self, descr: str) -> UrgencyTicket:
        if descr in self.seen.keys():
            return self.seen[descr]
        try:
            urgency_ticket = self._get(descr)
        except NotFound:
            raise InvalidRecord()
        self.seen[urgency_ticket.descr] = urgency_ticket
        return urgency_ticket

    @abc.abstractmethod
    def _add(self, partner: UrgencyTicket):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> UrgencyTicket:
        raise NotImplementedError


class SqlLiteRepositoryUrgencyTicket(AbstractRepositoryUrgencyTicket):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = 'INSERT INTO urgency_tickets (descr) VALUES (:descr)'

        self.select = ('SELECT\n'
                       '               urgency_ticket_id,\n'
                       '                descr\n'
                       '            FROM urgency_tickets\n'
                       '            WHERE descr=:descr')

    def _add(self, urgency_ticket):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(urgency_ticket))
        urgency_ticket.urgency_ticket_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, descr: str) -> UrgencyTicket:
        cur = self.conn.cursor()

        cur.execute(self.select, {'descr': descr})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return UrgencyTicket(urgency_ticket_id=result[0], descr=result[1])
