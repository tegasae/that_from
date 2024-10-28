import abc
from dataclasses import asdict

from loader.domain.model import CounterParty
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryCounterParty(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, counter_party: CounterParty):
        try:
            p = self.get(code1s=counter_party.code1s)
            # partner=p
        except InvalidRecord:
            self._add(counter_party)
            self.seen[counter_party.code1s] = counter_party
        counter_party = self.seen[counter_party.code1s]
        return self.seen[counter_party.code1s]

    def get(self, code1s: str) -> CounterParty:
        if code1s in self.seen.keys():
            return self.seen[code1s]
        try:
            counter_party = self._get(code1s)
        except NotFound:
            raise InvalidRecord()
        self.seen[code1s] = counter_party
        return counter_party

    @abc.abstractmethod
    def _add(self, counter_party: CounterParty):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> CounterParty:
        raise NotImplementedError


class SqlLiteRepositoryCounterParty(AbstractRepositoryCounterParty):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = ('INSERT INTO counterparties (\n'
                       '    is_predefined,\n'
                       '    link_counterparty,\n'
                       '    is_deleted,\n'
                       '    is_group,\n'
                       '    parent,\n'
                       '    name,\n'
                       '    code1s\n'
                       ') VALUES (\n'
                       '    :is_predefined,\n'
                       '    :link_counterparty,\n'
                       '    :is_deleted,\n'
                       '    :is_group,\n'
                       '    :parent,\n'
                       '    :name,\n'
                       '    :code1s\n'
                       ')')

        self.select = ('SELECT\n'
                       '                counterparty_id,\n'
                       '                is_predefined,\n'
                       '                link_counterparty,\n'
                       '                is_deleted,\n'
                       '                is_group,\n'
                       '                parent,\n'
                       '                name,\n'
                       '                code1s\n'
                       '            FROM counterparties\n'
                       '            WHERE code1s=:code1s')

    def _add(self, counter_party):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(counter_party))
        counter_party.counterparty_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, code1s: str) -> CounterParty:
        cur = self.conn.cursor()

        cur.execute(self.select, {'code1s': code1s})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return CounterParty(counterparty_id=result[0], is_predefined=result[1], link_counterparty=result[2],
                            is_deleted=result[3], is_group=result[4], parent=result[5], name=result[6],
                            code1s=result[7])
