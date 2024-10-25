import abc
from dataclasses import asdict

from loader.domain.model import UnitOfMeasurement
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryUnitOfMeasurement(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, unit_of_measurement:UnitOfMeasurement):
        try:
            p = self.get(descr=unit_of_measurement.descr)
            # partner=p
        except InvalidRecord:
            self._add(unit_of_measurement)
            self.seen[unit_of_measurement.descr] = unit_of_measurement
        unit_of_measurement = self.seen[unit_of_measurement.descr]
        return self.seen[unit_of_measurement.descr]

    def get(self, descr: str) -> UnitOfMeasurement:
        if descr in self.seen.keys():
            return self.seen[descr]
        try:
            unit_of_measurement = self._get(descr)
        except NotFound:
            raise InvalidRecord()
        self.seen[unit_of_measurement.descr] = unit_of_measurement
        return unit_of_measurement

    @abc.abstractmethod
    def _add(self, partner: UnitOfMeasurement):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> UnitOfMeasurement:
        raise NotImplementedError


class SqlLiteRepositoryUnitOfMeasurement(AbstractRepositoryUnitOfMeasurement):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = 'INSERT INTO units_of_measurement (descr) VALUES (:descr)'

        self.select = ('SELECT\n'
                       '               unit_of_measurement_id,\n'
                       '                descr\n'
                       '            FROM units_of_measurement\n'
                       '            WHERE descr=:descr')

    def _add(self, unit_of_measurement):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(unit_of_measurement))
        unit_of_measurement.unit_of_measurement_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self,descr: str) -> UnitOfMeasurement:
        cur = self.conn.cursor()

        cur.execute(self.select, {'descr': descr})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return UnitOfMeasurement(unit_of_measurement_id=result[0], descr=result[1])
