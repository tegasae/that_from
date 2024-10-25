import abc
from dataclasses import asdict

from loader.domain.model import Nomenclature
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryNomenclature(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, nomenclature: Nomenclature):
        try:
            p = self.get(code1s=nomenclature.code1s)
            # partner=p
        except InvalidRecord:
            self._add(nomenclature)
            self.seen[nomenclature.code1s] = nomenclature
        nomenclature = self.seen[nomenclature.code1s]
        return self.seen[nomenclature.code1s]

    def get(self, code1s: str) -> Nomenclature:
        if code1s in self.seen.keys():
            return self.seen[code1s]
        try:
            nomenclature = self._get(code1s)
        except NotFound:
            raise InvalidRecord()
        self.seen[code1s] = nomenclature
        return nomenclature

    @abc.abstractmethod
    def _add(self, nomenclature: Nomenclature):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Nomenclature:
        raise NotImplementedError


class SqlLiteRepositoryNomenclature(AbstractRepositoryNomenclature):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = ('INSERT INTO nomenclatures (\n'
                       '    is_predefined,\n'
                       '    link_nomenclature,\n'
                       '    is_deleted,\n'
                       '    is_group,\n'
                       '    parent,\n'
                       '    name,\n'
                       '    code1s,\n'
                       '    unit_of_measurement_id'
                       ') VALUES (\n'
                       '    :is_predefined,\n'
                       '    :link_nomenclature,\n'
                       '    :is_deleted,\n'
                       '    :is_group,\n'
                       '    :parent,\n'
                       '    :name,\n'
                       '    :code1s,\n'
                       '    :base_unit_of_measurement'
                       ')')

        self.select = ('SELECT\n'
                       '                nomenclature_id,\n'
                       '                is_predefined,\n'
                       '                link_nomenclature,\n'
                       '                is_deleted,\n'
                       '                is_group,\n'
                       '                parent,\n'
                       '                name,\n'
                       '                code1s,\n'
                       '                unit_of_measurement_id\n'
                       '            FROM nomenclatures\n'
                       '            WHERE code1s=:code1s')

    def _add(self, nomenclature):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(nomenclature))
        nomenclature.nomenclature_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, code1s: str) -> Nomenclature:
        cur = self.conn.cursor()

        cur.execute(self.select, {'code1s': code1s})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return Nomenclature(nomenclature_id=result[0], is_predefined=result[1], link_nomenclature=result[2],
                            is_deleted=result[3], is_group=result[4], parent=result[5],
                            name=result[6], code1s=result[7], base_unit_of_measurement=result[8])
