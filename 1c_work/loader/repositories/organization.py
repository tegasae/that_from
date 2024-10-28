import abc
from dataclasses import asdict

from loader.domain.model import Organization
from loader.exceptions import InvalidRecord, NotFound


class AbstractRepositoryOrganization(abc.ABC):
    def __init__(self):
        self.seen = {}

    def add(self, organization: Organization):
        try:
            p = self.get(code1s=organization.code1s)
            # partner=p
        except InvalidRecord:
            self._add(organization)
            self.seen[organization.code1s] = organization
        organization = self.seen[organization.code1s]
        return self.seen[organization.code1s]

    def get(self, code1s: str) -> Organization:
        if code1s in self.seen.keys():
            return self.seen[code1s]
        try:
            organization = self._get(code1s)
        except NotFound:
            raise InvalidRecord()
        self.seen[code1s] = organization
        return organization

    @abc.abstractmethod
    def _add(self, organization: Organization):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, code1s: str) -> Organization:
        raise NotImplementedError


class SqlLiteRepositoryOrganization(AbstractRepositoryOrganization):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.insert = ('INSERT INTO organizations (\n'
                       '    is_predefined,\n'
                       '    link_organization,\n'
                       '    is_deleted,\n'
                       '    name,\n'
                       '    code1s\n'
                       ') VALUES (\n'
                       '    :is_predefined,\n'
                       '    :link_organization,\n'
                       '    :is_deleted,\n'
                       '    :name,\n'
                       '    :code1s\n'
                       ')')

        self.select = ('SELECT\n'
                       '                organization_id,\n'
                       '                is_predefined,\n'
                       '                link_organization,\n'
                       '                is_deleted,\n'
                       '                name,\n'
                       '                code1s\n'
                       '            FROM organizations\n'
                       '            WHERE code1s=:code1s')

    def _add(self, organization):
        cur = self.conn.cursor()
        cur.execute(self.insert, asdict(organization))
        organization.organization_id = cur.lastrowid

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

    def _get(self, code1s: str) -> Organization:
        cur = self.conn.cursor()

        cur.execute(self.select, {'code1s': code1s})
        result = cur.fetchone()
        if not result:
            raise NotFound()

        return Organization(organization_id=result[0], is_predefined=result[1],
                            link_organization=result[2], is_deleted=result[3], name=result[4], code1s=result[5])
