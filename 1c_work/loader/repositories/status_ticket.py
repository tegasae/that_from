import abc
from dataclasses import asdict

from loader.domain.model import StatusTicket
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryStatusTicket(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, status_ticket: StatusTicket):
        try:
            p = self.get(descr=status_ticket.descr)
            # partner=p
        except InvalidRecord:
            self._add(status_ticket)
            self.seen[status_ticket.descr] = status_ticket
        status_ticket = self.seen[status_ticket.descr]
        return self.seen[status_ticket.descr]

    def get(self, descr: str) -> StatusTicket:
        if descr in self.seen.keys():
            return self.seen[descr]
        try:
            status_ticket = self._get(descr)
        except NotFound:
            raise InvalidRecord()
        self.seen[status_ticket.descr] = status_ticket
        return status_ticket

    @abc.abstractmethod
    def _add(self, partner: StatusTicket):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> StatusTicket:
        raise NotImplementedError


class SqlLiteRepositoryStatusTicket(AbstractRepositoryStatusTicket):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = 'INSERT INTO status_tickets (descr) VALUES (:descr)'

        self.select = ('SELECT\n'
                       '               status_ticket_id,\n'
                       '                descr\n'
                       '            FROM status_tickets\n'
                       '            WHERE descr=:descr')

    def _add(self, status_ticket):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(status_ticket))
        status_ticket.status_ticket_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, descr: str) -> StatusTicket:
        cur = self.conn.cursor()

        cur.execute(self.select, {'descr': descr})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return StatusTicket(status_ticket_id=result[0], descr=result[1])
