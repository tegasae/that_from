import abc
from dataclasses import asdict

from loader.exceptions import InvalidRecord, NotFound

import abc
from dataclasses import asdict

from loader.domain.model import Employee
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryEmployee(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, employee: Employee):
        try:
            p = self.get(code1s=employee.code1s)
            # employee=p
        except InvalidRecord:
            self._add(employee)
            self.seen[employee.code1s] = employee
        employee = self.seen[employee.code1s]
        return self.seen[employee.code1s]

    def get(self, code1s: str) -> Employee:
        if code1s in self.seen.keys():
            return self.seen[code1s]
        try:
            employee = self._get(code1s)
        except NotFound:
            raise InvalidRecord()
        self.seen[code1s] = employee
        return employee

    @abc.abstractmethod
    def _add(self, employee: Employee):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Employee:
        raise NotImplementedError


class SqlLiteRepositoryEmployee(AbstractRepositoryEmployee):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = ('INSERT INTO employees (\n'
                       '                       is_predefined,\n'
                       '                       link_employee,\n'
                       '                       is_deleted,\n'
                       '                       is_group,\n'
                       '                       parent,\n'
                       '                       name,\n'
                       '                       code1s,\n'
                       '                       employee,\n'
                       '                       department_id,\n'
                       '                       code_sync,\n'
                       '                       drive_license,\n'
                       '                       idb24,\n'
                       '                       date_of_end,\n'
                       '                       telegram,\n'
                       '                       email,\n'
                       '                       phone,\n'
                       '                       is_penalty_coefficient\n'
                       '                       ) VALUES (\n'
                       '                            :is_predefined,\n'
                       '                            :link_employee,\n'
                       '                            :is_deleted,\n'
                       '                            :is_group,\n'
                       '                            :parent,\n'
                       '                            :name,\n'
                       '                            :code1s,\n'
                       '                            :employee,\n'
                       '                            :department,\n'
                       '                            :code_sync,\n'
                       '                            :drive_license,\n'
                       '                            :idb24,\n'
                       '                            :date_of_end,\n'
                       '                            :telegram,\n'
                       '                            :email,\n'
                       '                            :phone,\n'
                       '                            :is_penalty_coefficient \n'
                       '                       )')

        self.select = ('SELECT\n'
                       '                                       employee_id,\n'
                       '                            is_predefined,\n'
                       '                       link_employee,\n'
                       '                       is_deleted,\n'
                       '                       is_group,\n'
                       '                       parent,\n'
                       '                       name,\n'
                       '                       code1s,\n'
                       '                       employee,\n'
                       '                       department_id,\n'
                       '                       code_sync,\n'
                       '                       drive_license,\n'
                       '                       idb24,\n'
                       '                       date_of_end,\n'
                       '                       telegram,\n'
                       '                       email,\n'
                       '                       phone,\n'
                       '                       is_penalty_coefficient\n'
                       '                                   FROM employees\n'
                       '                                   WHERE code1s=:code1s')

    def _add(self, employee):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(employee))
        employee.employee_id = cur.lastrowid



    def _get(self, code1s: str) -> Employee:
        cur = self.conn.cursor()

        cur.execute(self.select, {'code1s': code1s})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return Employee(employee_id=result[0], is_predefined=result[1], link_employee=result[2], is_deleted=result[3],
                        is_group=result[4], parent=result[5], name=result[6], code1s=result[7],
                        employee=result[8],department=result[9],code_sync=result[10],drive_license=result[11],
                        idb24=result[12],date_of_end=result[13],telegram=result[14],email=result[15],phone=result[16],
                        is_penalty_coefficient=result[17])


