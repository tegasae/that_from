from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass(kw_only=True)
class Partner:
    partner_id: int = 0  # Primary Key, NOT NULL
    is_predefined: bool = field(default=False)  # INTEGER, NOT NULL, DEFAULT 0 (False)
    link_partner: str = ""  # TEXT, nullable
    is_deleted: bool = False
    is_group: bool = False
    parent: str = ""
    name: str
    code1s: str


@dataclass(kw_only=True)
class CounterParty:
    counterparty_id: int = 0  # Primary Key, NOT NULL
    is_predefined: bool = False
    link_counterparty: str = ""
    is_deleted: bool = False
    is_group: bool = False
    parent: str = ""
    name: str
    code1s: str


@dataclass(kw_only=True)
class Department:
    department_id: int = 0
    name: str


@dataclass(kw_only=True)
class Manager:
    manager_id: int = 0
    is_predefined: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_predefined=0 OR is_predefined=1)
    link_manager: str = ""
    is_deleted: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_deleted=0 OR is_deleted=1)
    is_group: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_group=0 OR is_group=1)
    parent: str = ""
    name: str
    code1s: str


@dataclass(kw_only=True)
class Status:
    status_id: int = 0
    name: str


@dataclass(kw_only=True)
class Currency:
    currency_id: int = 0
    is_predefined: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_predefined=0 OR is_predefined=1)
    link_currency: str = ""
    is_deleted: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_deleted=0 OR is_deleted=1)
    name: str
    code1s: str


@dataclass(kw_only=True)
class Organization:
    organization_id: int = 0
    is_predefined: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_predefined=0 OR is_predefined=1)
    link_organization: str = ""
    is_deleted: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_deleted=0 OR is_deleted=1)
    name: str
    code1s: str


@dataclass(kw_only=True)
class UrgencyTicket:
    urgency_ticket_id: int = 0
    descr: str


@dataclass(kw_only=True)
class StatusTicket:
    status_ticket_id: int = 0
    descr: str


@dataclass(kw_only=True)
class UnitOfMeasurement:
    unit_of_measurement_id: int = 0
    descr: str


@dataclass(kw_only=True)
class Employee:
    employee_id: int = 0
    is_predefined: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_predefined=0 OR is_predefined=1)
    link_employee: str = ""
    is_deleted: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_deleted=0 OR is_deleted=1)
    is_group: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_group=0 OR is_group=1)
    parent: str = ""
    name: str
    code1s: str
    employee: str = ""
    department: int
    code_sync: str = ""
    drive_license: str = ""
    idb24: str = ""
    date_of_end: datetime
    telegram: str = ""
    email: str = ""
    phone: str = ""
    is_penalty_coefficient: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_deleted=0 OR is_deleted=1)


@dataclass(kw_only=True)
class Performer:
    performer_id: int = 0
    employee: int
    descr_work: str = ""
    date_start: datetime
    date_end: datetime
    hours_payment: float = 0
    hours_fact: float = 0
    urgency_ticket: int
    status_ticket: int


@dataclass(kw_only=True)
class Nomenclature:
    nomenclature_id: int = 0
    is_predefined: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_predefined=0 OR is_predefined=1)
    link_nomenclature: str = ""
    is_deleted: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_deleted=0 OR is_deleted=1)
    is_group: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_group=0 OR is_group=1)
    parent: str = ""
    name: str
    code1s: str
    article: str = ""
    kind_of_nomenclature: str = ""
    weight_of_coefficient: str = ""
    accounting_by_series: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_group=0 OR is_group=1)
    accounting_by_measurement: bool = field(default=False)  # INTEGER DEFAULT 0, CHECK(is_group=0 OR is_group=1)
    base_unit_of_measurement: int


@dataclass(kw_only=True)
class Service:
    service_id: int = 0
    nomenclature: int
    quantity: float = 0
    price: float = 0
    summ: float = 0
    unit_of_measurement: int


@dataclass(kw_only=True)
class ReasonOfWork:
    reasons_of_work_id: int = 0
    reasons_of_work: str = ""


@dataclass(kw_only=True)
class Material:
    material_id: int = 0
    material: str = ""


@dataclass(kw_only=True)
class Work:
    work_id: Optional[int] = field(default=0)
    is_passed: bool = field(default=True)
    link_work: str = ""
    is_deleted: bool = field(default=False)
    code1s: str
    date_: datetime
    partner: int
    counterparty: int
    contract: str = ""
    department: int
    comment: str = ""
    manager: int = 0
    status: int
    summ: Decimal = 0
    is_billed: bool = False
    currency: int = 0
    kind_of_price: str = ""
    organization: int
    bill: str = ""
    link_bill: str = ""
    link_realization: str = ""
    performers: list[Performer]
    services: list[Service]
    materials: list[Material] = field(default_factory=list)
    reasons_of_work: list[ReasonOfWork]=field(default_factory=list)
