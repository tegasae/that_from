import json
import sqlite3

from loader.domain.model import Partner, StatusTicket, Employee, UrgencyTicket, CounterParty, Department, Status, \
    Organization
from loader.fabrics import CollectionPartner, CollectionCounterParty, CollectionDepartment, CollectionStatus, \
    CollectionOrganization, CollectionEmployee, CollectionStatusTicket, CollectionUrgencyTicket, \
    CollectionUnitOfMeasurement, CollectionNomenclature, CollectionWork, CollectionPerformer, CollectionService
from loader.repositories.counter_party import SqlLiteRepositoryCounterParty
from loader.repositories.department import SqlLiteRepositoryDepartment
from loader.repositories.employee import SqlLiteRepositoryEmployee
from loader.repositories.nomenclature import SqlLiteRepositoryNomenclature
from loader.repositories.organization import SqlLiteRepositoryOrganization
from loader.repositories.partner import SqlLiteRepositoryPartner
from loader.repositories.status import SqlLiteRepositoryStatus
from loader.repositories.status_ticket import SqlLiteRepositoryStatusTicket
from loader.repositories.unit_of_measurment import SqlLiteRepositoryUnitOfMeasurement
from loader.repositories.urgency_ticket import SqlLiteRepositoryUrgencyTicket
from loader.repositories.work import SqlLiteRepositoryWork

con = sqlite3.connect("../works.db")

repository_partner = SqlLiteRepositoryPartner(conn=con)
collect_partner = CollectionPartner(repository=repository_partner)

repository_counter_party = SqlLiteRepositoryCounterParty(conn=con)
collect_counter_party = CollectionCounterParty(repository=repository_counter_party)

repository_department = SqlLiteRepositoryDepartment(conn=con)
collect_department = CollectionDepartment(repository=repository_department)

repository_status = SqlLiteRepositoryStatus(conn=con)
collect_status = CollectionStatus(repository=repository_status)

repository_status_ticket = SqlLiteRepositoryStatusTicket(conn=con)
collect_status_ticket = CollectionStatusTicket(repository=repository_status_ticket)

repository_urgency_ticket = SqlLiteRepositoryUrgencyTicket(conn=con)
collect_urgency_ticket = CollectionUrgencyTicket(repository=repository_urgency_ticket)

repository_unit_of_measurement = SqlLiteRepositoryUnitOfMeasurement(conn=con)
collect_unit_of_measurement = CollectionUnitOfMeasurement(repository=repository_unit_of_measurement)

repository_organization = SqlLiteRepositoryOrganization(conn=con)
collect_organization = CollectionOrganization(repository=repository_organization)

repository_employee = SqlLiteRepositoryEmployee(conn=con)
collect_employee = CollectionEmployee(repository=repository_employee,
                                      repository_department=repository_department)

repository_nomenclature = SqlLiteRepositoryNomenclature(conn=con)
collect_nomenclature = CollectionNomenclature(repository=repository_nomenclature,
                                              repository_unit_if_measurement=repository_unit_of_measurement)

collect_performer = CollectionPerformer()
collect_service = CollectionService()
repository_work = SqlLiteRepositoryWork(conn=con)
collect_work = CollectionWork(repository=repository_work)
with open("works.json", encoding='utf-8-sig') as j:
    d = json.load(j)

for i in d:
    n = i['Номер']
    print(i['Номер'])
    print(i)
    print("\n\n")

    partner: Partner = collect_partner.create(i['Партнер'])
    counter_party: CounterParty = collect_counter_party.create(i['Контрагент'])
    department: Department = collect_department.create(i['Отдел'])
    status: Status = collect_status.create(i['Статус'])
    organization: Organization = collect_organization.create(i['Организация'])

    status_ticket: StatusTicket
    employee: Employee
    urgency_ticket: UrgencyTicket
    performers = []
    for e in i['Исполнители']:
        collect_department.create(e['Сотрудник']['Отдел'])
        status_ticket = collect_status_ticket.create(e['СтатусЗаявки'])
        employee = collect_employee.create(e['Сотрудник'])
        urgency_ticket = collect_urgency_ticket.create(e['Срочность'])
        performers.append(collect_performer.create(data=e, employee_id=employee.employee_id,
                                                   urgency_ticket_id=urgency_ticket.urgency_ticket_id,
                                                   status_ticket_id=status_ticket.status_ticket_id))
    #
    # measurement_of_unit: UnitOfMeasurement
    # nomenclature: Nomenclature
    services = []
    for e in i['Услуги']:
        unit_of_measurement = collect_unit_of_measurement.create(e['ЕдИзмерения'])
        nomenclature = collect_nomenclature.create(e['Номенклатура'])
        services.append(collect_service.create(data=e, nomenclature_id=nomenclature.nomenclature_id,
                                               unit_of_measurement_id=unit_of_measurement.unit_of_measurement_id))
    work = collect_work.create(data=i, counterparty_id=counter_party.counterparty_id,
                               department_id=department.department_id, organization_id=organization.organization_id,
                               partner_id=partner.partner_id, performers=performers, services=services,
                               status_id=status.status_id)
    print(work)
# con = sqlite3.connect("../works.db")
# cur = con.cursor()
# sql = "INSERT INTO works (number_work, date_,summ) VALUES (?,?,?)"

# for i in d:
#    print(i['СчетВыставлен'])
#    cur.execute(sql, [i["Номер"], i["Дата"], i["Сумма"]])

con.commit()
con.close()
