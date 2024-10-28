
create table partners (
    partner_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_partner TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    is_group INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    parent TEXT,
    name TEXT,
    code1s TEXT UNIQUE
);

create table counterparties (
    counterparty_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_counterparty TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    is_group INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    parent TEXT,
    name TEXT,
    code1s TEXT UNIQUE
);

create table departments (
    department_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

create table managers (
    manager_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_manager TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    is_group INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    parent TEXT,
    name TEXT,
    code1s TEXT UNIQUE
);

create table statuses (
    status_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

create table currencies (
    currency_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_currency TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    name TEXT,
    code1s TEXT UNIQUE
);

create table organizations (
    organization_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_organization TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    name TEXT,
    code1s TEXT UNIQUE
);

create table urgency_tickets (
    urgency_ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    descr TEXT
);

create table status_tickets (
    status_ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    descr TEXT
);

create table units_of_measurement(
    unit_of_measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    descr TEXT
);



CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_employee TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    is_group INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    parent TEXT,
    name TEXT,
    code1s TEXT UNIQUE,
    employee TEXT,
    department_id INTEGER,
    code_sync TEXT,
    drive_license TEXT,
    idb24 TEXT,
    date_of_end TEXT,
    telegram TEXT,
    email TEXT,
    phone TEXT,
    is_penalty_coefficient INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    FOREIGN KEY (department_id)  REFERENCES departments (department_id)
);



create table performers (
    performer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    work_id INTEGER,
    number_of_col INTEGER,
    descr_work TEXT,
    date_start TEXT,
    date_end TEXT,
    hours_payment NUMERIC,
    hours_fact NUMERIC,
    urgency_ticket_id INTEGER,
    status_ticket_id INTEGER,
    FOREIGN KEY (employee_id)  REFERENCES employees (employee_id),
    FOREIGN KEY (work_id)  REFERENCES works (work_id),
    FOREIGN KEY (urgency_ticket_id)  REFERENCES urgency_tickets (urgency_ticket_id),
    FOREIGN KEY (status_ticket_id)  REFERENCES status_tickets (status_ticket_id)
);




create table services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_id INTEGER,
    nomenclature_id INTEGER,
    number_of_col INTEGER,
    quantity NUMERIC,
    price NUMERIC,
    summ NUMERIC,
    unit_of_measurement_id INTEGER,
    FOREIGN KEY (work_id)  REFERENCES works (work_id),
    FOREIGN KEY (nomenclature_id)  REFERENCES nomenclatures (nomenclature_id),
    FOREIGN KEY (unit_of_measurement_id)  REFERENCES units_of_measurement (unit_of_measurement_id)
);

create table nomenclatures (
    nomenclature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_predefined INTEGER DEFAULT (0) NOT NULL CHECK(is_predefined=0 OR is_predefined = 1),
    link_nomenclature TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    is_group INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    parent TEXT,
    name TEXT,
    code1s TEXT UNIQUE,
    article TEXT,
    kind_of_nomenclature TEXT,
    weight_of_coefficient NUMERIC,
    accounting_by_series INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    accounting_by_measurement INTEGER DEFAULT (0) NOT NULL CHECK(is_group=0 OR is_group = 1),
    unit_of_measurement_id INTEGER,
    FOREIGN KEY (unit_of_measurement_id)  REFERENCES units_of_measurement (unit_of_measurement_id)

);

create table works (
    work_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    is_passed INTEGER DEFAULT (0) NOT NULL CHECK(is_passed=0 OR is_passed = 1),
    link_work TEXT,
    is_deleted INTEGER DEFAULT (0) NOT NULL CHECK(is_deleted=0 OR is_deleted = 1),
    code1s TEXT UNIQUE,
    date_ TEXT,
    partner_id INTEGER,
    counterparty_id INTEGER,
    contract TEXT,
    department_id INTEGER,
    manager_id INTEGER,
    status_id INTEGER,
    summ NUMERIC,
    is_billed INTEGER DEFAULT (0) NOT NULL CHECK(is_billed=0 OR is_billed = 1),
    currency_id INTEGER,
    kind_of_price TEXT,
    organization_id INTEGER,
    bill TEXT,
    link_bill TEXT,
    link_realization TEXT,
    FOREIGN KEY (partner_id)  REFERENCES partners (partner_id),
    FOREIGN KEY (counterparty_id)  REFERENCES counterparties (counterparty_id),
    FOREIGN KEY (department_id)  REFERENCES departments (department_id),
    FOREIGN KEY (manager_id)  REFERENCES managers (manager_id),
    FOREIGN KEY (status_id)  REFERENCES statuses (status_id),
    FOREIGN KEY (currency_id)  REFERENCES currencies (currency_id),
    FOREIGN KEY (organization_id)  REFERENCES organizations (organization_id)
);



create table reasons_of_work (
    reasons_of_work_id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_id INTEGER,
    number_of_col INTEGER,
    reasons_of_work TEXT,
    FOREIGN KEY (work_id)  REFERENCES works (work_id)
);

create table materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_id INTEGER,
    material TEXT,
    FOREIGN KEY (work_id)  REFERENCES works (work_id)
);

