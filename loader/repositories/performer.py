import abc
from dataclasses import asdict

from loader.domain.model import Performer
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryPerformer(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, performer: Performer):
        try:
            p = self.get(code1s=performer.code1s)
            # Perfomer=p
        except InvalidRecord:
            self._add(performer)
            self.seen[performer.code1s] = performer
        performer = self.seen[performer.code1s]
        return self.seen[performer.code1s]

    def get(self, code1s: str) -> Performer:
        if code1s in self.seen.keys():
            return self.seen[code1s]
        try:
            perfomer = self._get(code1s)
        except NotFound:
            raise InvalidRecord()
        self.seen[code1s] = perfomer
        return perfomer

    @abc.abstractmethod
    def _add(self, perfomer: Performer):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Performer:
        raise NotImplementedError


class SqlLiteRepositoryPerformer(AbstractRepositoryPerformer):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = ('INSERT INTO performers (\n'
                       '    is_predefined,\n'
                       '    link_Perfomer,\n'
                       '    is_deleted,\n'
                       '    is_group,\n'
                       '    parent,\n'
                       '    name,\n'
                       '    code1s\n'
                       ') VALUES (\n'
                       '    :is_predefined,\n'
                       '    :link_Perfomer,\n'
                       '    :is_deleted,\n'
                       '    :is_group,\n'
                       '    :parent,\n'
                       '    :name,\n'
                       '    :code1s\n'
                       ')')

        self.select = ('SELECT\n'
                       '                performer_id,\n'
                       '                is_predefined,\n'
                       '                link_Perfomer,\n'
                       '                is_deleted,\n'
                       '                is_group,\n'
                       '                parent,\n'
                       '                name,\n'
                       '                code1s\n'
                       '            FROM perfomers\n'
                       '            WHERE code1s=:code1s')

    def _add(self, perfomer):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(perfomer))
        perfomer.performer_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, code1s: str) -> Performer:
        cur = self.conn.cursor()

        cur.execute(self.select, {'code1s': code1s})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return Performer(perfomer_id=result[0], is_predefined=result[1], link_Perfomer=result[2], is_deleted=result[3],
                         is_group=result[4], parent=result[5], name=result[6], code1s=result[7])
