import abc
from dataclasses import asdict

from loader.domain.model import Work


class AbstractRepositoryWork(abc.ABC):
    @abc.abstractmethod
    def add(self, work: Work) -> Work:
        raise NotImplementedError


class SqlLiteRepositoryWork(AbstractRepositoryWork):
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

    def add(self, work) -> Work:
        cur = self.conn.cursor()
        cur.execute("SELECT work_id FROM works WHERE code1s=:code1s", {"code1s": work.code1s})
        result = cur.fetchone()
        if result:
            cur.execute("DELETE FROM performers WHERE work_id=:work_id", {"work_id": result[0]})
            cur.execute("DELETE FROM services WHERE work_id=:work_id", {"work_id": result[0]})
            cur.execute("DELETE FROM works WHERE work_id=:work_id", {"work_id": result[0]})

        insert_work = '''INSERT INTO works
                        (is_passed,
                        link_work,
                        is_deleted,
                        code1s,
                        date_,
                        partner_id,
                        counterparty_id,
                        contract,
                        department_id,
                        status_id,
                        summ,
                        is_billed,
                        organization_id,
                        bill,
                        link_bill,
                        link_realization) 
                        VALUES( 
                        :is_passed,
                        :link_work,
                        :is_deleted,
                        :code1s,
                        :date_,
                        :partner_id,
                        :counterparty_id,
                        :contract,
                        :department_id,
                        :status_id,
                        :summ,
                        :is_billed,
                        :organization_id,
                        :bill,
                        :link_bill,
                        :link_realization) 
                    '''


        dict_work={
            'is_passed': work.is_passed,
            'link_work': work.link_work,
            'is_deleted': work.is_deleted,
            'code1s': work.code1s,
            'date_': work.date_,
            'partner_id': work.partner,
            'counterparty_id': work.counterparty,
            'contract': work.contract,
            'department_id': work.department,
            'status_id': work.status,
            'summ': work.summ,
            'is_billed': work.is_billed,
            'organization_id': work.organization,
            'bill': work.bill,
            'link_bill': work.link_bill,
            'link_realization': work.link_realization
        }
        n=asdict(work)
        cur.execute(insert_work,dict_work)
        work.work_id = cur.lastrowid
        insert_performer = '''INSERT INTO performers (
                    employee_id,
                    work_id,
                    number_of_col,
                    descr_work,
                    date_start,
                    date_end,
                    hours_payment,
                    hours_fact,
                    urgency_ticket_id,
                    status_ticket_id)
            VALUES (
                    :employee_id,
                    :work_id,
                    :number_of_col,
                    :descr_work,
                    :date_start,
                    :date_end,
                    :hours_payment,
                    :hours_fact,
                    :urgency_ticket_id,
                    :status_ticket_id)
            '''
        count = 0
        for p in work.performers:
            cur.execute(insert_performer, {
                'employee_id': p.employee,
                'work_id': work.work_id,
                'number_of_col': count + 1,
                'descr_work': p.descr_work,
                'date_start': p.date_start,
                'date_end': p.date_end,
                'hours_payment': p.hours_payment,
                'hours_fact': p.hours_fact,
                'urgency_ticket_id': p.urgency_ticket,
                'status_ticket_id': p.status_ticket
            })
            work.performers[count].performer_id = cur.lastrowid
            count += 1
        insert_service = '''
        INSERT INTO services  
                (work_id, nomenclature_id, number_of_col, quantity, summ, unit_of_measurement_id)
                VALUES
                (:work_id,:nomenclature_id,:number_of_col,:quantity,:summ,:unit_of_measurement_id)
        '''
        count = 0
        for s in work.services:
            cur.execute(insert_service, {
                'work_id': work.work_id,
                'nomenclature_id': s.nomenclature,
                'number_of_col': count + 1,
                'quantity': s.quantity,
                'summ': s.summ,
                'unit_of_measurement_id': s.unit_of_measurement
            })
            work.services[count].service_id = cur.lastrowid
            count += 1

        return work

    # for i in d:
    #    print(i['СчетВыставлен'])
    #    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])
