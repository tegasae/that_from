import abc
from dataclasses import asdict

from loader.domain.model import Department
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryDepartment(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, department: Department):
        try:
            p = self.get(name=department.name)
            # partner=p
        except InvalidRecord:
            self._add(department)
            self.seen[department.name] = department
        department = self.seen[department.name]
        return self.seen[department.name]

    def get(self, name: str) -> Department:
        if name in self.seen.keys():
            return self.seen[name]
        try:
            department = self._get(name)
        except NotFound:
            raise InvalidRecord()
        self.seen[department.name] = department
        return department

    @abc.abstractmethod
    def _add(self, partner: Department):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Department:
        raise NotImplementedError


class SqlLiteRepositoryDepartment(AbstractRepositoryDepartment):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = 'INSERT INTO departments (name) VALUES (:name)'

        self.select = ('SELECT\n'
                       '               department_id,\n'
                       '                name\n'
                       '            FROM departments\n'
                       '            WHERE name=:name')

    def _add(self, department):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(department))
        department.department_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, name: str) -> Department:
        cur = self.conn.cursor()

        cur.execute(self.select, {'name': name})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return Department(department_id=result[0], name=result[1])
