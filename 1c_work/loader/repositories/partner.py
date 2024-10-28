import abc
from dataclasses import asdict

from loader.domain.model import Partner
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryPartner(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, partner: Partner):
        try:
            p=self.get(code1s=partner.code1s)
            #partner=p
        except InvalidRecord:
            self._add(partner)
            self.seen[partner.code1s]=partner
        partner=self.seen[partner.code1s]
        return self.seen[partner.code1s]

    def get(self, code1s: str) -> Partner:
        if code1s in self.seen.keys():
            return self.seen[code1s]
        try:
            partner = self._get(code1s)
        except NotFound:
            raise InvalidRecord()
        self.seen[code1s] = partner
        return partner


    @abc.abstractmethod
    def _add(self, partner: Partner):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Partner:
        raise NotImplementedError


class SqlLiteRepositoryPartner(AbstractRepositoryPartner):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = ('INSERT INTO partners (\n'
                       '    is_predefined,\n'
                       '    link_partner,\n'
                       '    is_deleted,\n'
                       '    is_group,\n'
                       '    parent,\n'
                       '    name,\n'
                       '    code1s\n'
                       ') VALUES (\n'
                       '    :is_predefined,\n'
                       '    :link_partner,\n'
                       '    :is_deleted,\n'
                       '    :is_group,\n'
                       '    :parent,\n'
                       '    :name,\n'
                       '    :code1s\n'
                       ')')

        self.select = ('SELECT\n'
                       '                partner_id,\n'
                       '                is_predefined,\n'
                       '                link_partner,\n'
                       '                is_deleted,\n'
                       '                is_group,\n'
                       '                parent,\n'
                       '                name,\n'
                       '                code1s\n'
                       '            FROM partners\n'
                       '            WHERE code1s=:code1s')

    def _add(self, partner):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(partner))
        partner.partner_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, code1s: str) -> Partner:
        cur = self.conn.cursor()

        cur.execute(self.select, {'code1s':code1s})
        result = cur.fetchone()
        if not result:
            raise NotFound()


        return Partner(partner_id=result[0],is_predefined=result[1],link_partner=result[2],is_deleted=result[3],is_group=result[4],parent=result[5],name=result[6],code1s=result[7])
