import abc
from dataclasses import asdict

from loader.domain.model import Status
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryStatus(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, status:Status):
        try:
            p = self.get(name=status.name)
            # partner=p
        except InvalidRecord:
            self._add(status)
            self.seen[status.name] = status
        status = self.seen[status.name]
        return self.seen[status.name]

    def get(self, name: str) -> Status:
        if name in self.seen.keys():
            return self.seen[name]
        try:
            status = self._get(name)
        except NotFound:
            raise InvalidRecord()
        self.seen[status.name] = status
        return status

    @abc.abstractmethod
    def _add(self, partner: Status):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Status:
        raise NotImplementedError


class SqlLiteRepositoryStatus(AbstractRepositoryStatus):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = 'INSERT INTO statuses (name) VALUES (:name)'

        self.select = ('SELECT\n'
                       '               status_id,\n'
                       '                name\n'
                       '            FROM statuses\n'
                       '            WHERE name=:name')

    def _add(self, status):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(status))
        status.status_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, name: str) -> Status:
        cur = self.conn.cursor()

        cur.execute(self.select, {'name': name})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return Status(status_id=result[0], name=result[1])
