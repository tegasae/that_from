import abc

from loader.domain.model import Partner, CounterParty, Department, Status, Organization, Employee, StatusTicket, \
    UrgencyTicket, UnitOfMeasurement, Nomenclature, Performer, Service, Work


class Collect(abc.ABC):
    def __init__(self, repository):
        self.repository = repository

    @abc.abstractmethod
    def create(self, data: dict):
        raise NotImplementedError


class CollectionPartner(Collect):
    def create(self, data: dict):
        p = Partner(
            is_predefined=data['Предопределенный'],
            link_partner=data['Ссылка'],
            is_deleted=data['ПометкаУдаления'],
            is_group=data['ЭтоГруппа'],
            parent=data['Родитель'],
            name=data['Наименование'],
            code1s=data['Код'])

        # return self.partners[data['Код']]
        return self.repository.add(partner=p)


class CollectionCounterParty(Collect):
    def create(self, data: dict):
        counter_party = CounterParty(
            is_predefined=data['Предопределенный'],
            link_counterparty=data['Ссылка'],
            is_deleted=data['ПометкаУдаления'],
            is_group=data['ЭтоГруппа'],
            parent=data['Родитель'],
            name=data['Наименование'],
            code1s=data['Код']
        )
        return self.repository.add(counter_party=counter_party)
        # return self.repository.add(partner=cp)


class CollectionDepartment(Collect):
    def create(self, data: str):
        department = Department(
            name=data
        )
        return self.repository.add(department=department)
        # return self.repository.add(partner=cp)


class CollectionStatus(Collect):
    def create(self, data: str):
        status = Status(
            name=data
        )
        return self.repository.add(status=status)
        # return self.repository.add(partner=cp)


class CollectionStatusTicket(Collect):
    def create(self, data: str):
        status_ticket = StatusTicket(
            descr=data
        )
        return self.repository.add(status_ticket=status_ticket)
        # return self.repository.add(partner=cp)


class CollectionUrgencyTicket(Collect):
    def create(self, data: str):
        urgency_ticket = UrgencyTicket(
            descr=data
        )
        return self.repository.add(urgency_ticket=urgency_ticket)
        # return self.repository.add(partner=cp)


class CollectionUnitOfMeasurement(Collect):
    def create(self, data: str):
        unit_of_measurement = UnitOfMeasurement(
            descr=data
        )
        return self.repository.add(unit_of_measurement=unit_of_measurement)
        # return self.repository.add(partner=cp)


class CollectionOrganization(Collect):
    def create(self, data: dict):
        organization = Organization(
            is_predefined=data['Предопределенный'],

            is_deleted=data['ПометкаУдаления'],
            name=data['Наименование'],
            code1s=data['Код']
        )
        return self.repository.add(organization=organization)
        # return self.repository.add(partner=cp)


class CollectionEmployee(Collect):
    def __init__(self, repository, repository_department):
        super().__init__(repository)
        self.repository_department = repository_department

    def create(self, data: dict):
        d = self.repository_department.get(name=data['Отдел'])
        p = Employee(
            is_predefined=data['Предопределенный'],
            link_employee=data['Ссылка'],
            is_deleted=data['ПометкаУдаления'],
            is_group=data['ЭтоГруппа'],
            parent=data['Родитель'],
            name=data['Наименование'],
            code1s=data['Код'],
            employee=data['Сотрудник'],
            department=d.department_id,
            code_sync=data['КодСинхр'],
            drive_license=data['ВодительскоеУдостоверение'],
            idb24=data['ИдБ24'],
            date_of_end=data['ДатаСКотНеРаботает'],
            email=data['ЭлПочта'],
            phone=data['Телефон'],
            is_penalty_coefficient=data['ШтрафнойКоэффициент']
        )

        # return self.partners[data['Код']]
        return self.repository.add(employee=p)


class CollectionNomenclature(Collect):
    def __init__(self, repository, repository_unit_if_measurement):
        super().__init__(repository)
        self.repository_unit_of_measurement = repository_unit_if_measurement

    def create(self, data: dict):
        n = data['БазоваяЕдиницаИзмерения']
        d = self.repository_unit_of_measurement.get(descr=n)
        p = Nomenclature(
            is_predefined=data['Предопределенный'],
            link_nomenclature=data['Ссылка'],
            is_deleted=data['ПометкаУдаления'],
            is_group=data['ЭтоГруппа'],
            parent=data['Родитель'],
            name=data['Наименование'],
            code1s=data['Код'],
            base_unit_of_measurement=d.unit_of_measurement_id
        )

        # return self.partners[data['Код']]
        return self.repository.add(p)


class CollectionPerformer:
    def create(self, data: dict, employee_id: int, urgency_ticket_id: int, status_ticket_id: int):
        performer = Performer(
            employee=employee_id,
            descr_work=data['СоставРабот'],
            date_start=data['ДатаС'],
            date_end=data['ДатаПо'],
            hours_payment=data['КолЧасовНаОплату'],
            hours_fact=data['КолЧасовФакт'],
            urgency_ticket=urgency_ticket_id,
            status_ticket=status_ticket_id
        )

        return performer


class CollectionService:
    def create(self, data: dict, nomenclature_id: int, unit_of_measurement_id: int):
        service = Service(
            nomenclature=nomenclature_id,
            quantity=data['Количество'],
            price=data['Цена'],
            summ=data['Сумма'],
            unit_of_measurement=unit_of_measurement_id
        )
        return service


class CollectionWork:
    def __init__(self, repository):
        self.repository = repository

    def create(self, data: dict, performers: list[Performer], services: list[Service],
               partner_id: int, counterparty_id: int, department_id: int, status_id: int, organization_id: int):
        work = Work(
            is_passed=data['Проведен'],
            link_work=data['Ссылка'],
            is_deleted=data['ПометкаУдаления'],
            date_=data['Дата'],
            code1s=data['Номер'],
            partner=partner_id,
            counterparty=counterparty_id,
            contract=data['Договор'],
            department=department_id,
            comment=data['Комментарий'],
            status=status_id,
            summ=data['Сумма'],
            is_billed=data['СчетВыставлен'],
            organization=organization_id,
            bill=data['Счет'],
            link_bill=data['СсылкаНаСчет'],
            link_realization=data['СсылкаНаДокументРеализации'],
            performers=performers,
            services=services

        )
        work = self.repository.add(work=work)
        return work
