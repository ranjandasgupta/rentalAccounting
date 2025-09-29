-- PostgreSQL schema for Rental Accounting

CREATE TABLE IF NOT EXISTS company (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  tin VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS property (
  id SERIAL PRIMARY KEY,
  company_id INTEGER NOT NULL REFERENCES company(id) ON DELETE CASCADE,
  street_address VARCHAR(255) NOT NULL,
  city VARCHAR(255) NOT NULL,
  state VARCHAR(255) NOT NULL,
  zip VARCHAR(255) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS tenant (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(200) NOT NULL,
  last_name VARCHAR(200) NOT NULL,
  phone VARCHAR(64),
  email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS lease (
  id SERIAL PRIMARY KEY,
  tenant_id INTEGER NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
  property_id INTEGER NOT NULL REFERENCES property(id) ON DELETE CASCADE,
  from_date DATE NOT NULL,
  to_date DATE
);

CREATE TABLE IF NOT EXISTS rent (
  id SERIAL PRIMARY KEY,
  property_id INTEGER NOT NULL REFERENCES property(id) ON DELETE CASCADE,
  from_date DATE NOT NULL,
  to_date DATE,
  amount NUMERIC(12,2) NOT NULL,
  CONSTRAINT uq_rent_prop_from UNIQUE (property_id, from_date)
);

CREATE TABLE IF NOT EXISTS account_type (
  id SERIAL PRIMARY KEY,
  code VARCHAR(32) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS account_sub_type (
  id SERIAL PRIMARY KEY,
  type_id INTEGER NOT NULL REFERENCES account_type(id) ON DELETE RESTRICT,
  code VARCHAR(64) UNIQUE NOT NULL,
  name VARCHAR(200) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS account (
  id SERIAL PRIMARY KEY,
  type_id INTEGER NOT NULL REFERENCES account_type(id) ON DELETE RESTRICT,
  sub_type_id INTEGER REFERENCES account_sub_type(id) ON DELETE SET NULL,
  name VARCHAR(200) UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS transaction (
  id SERIAL PRIMARY KEY,
  debit_account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE RESTRICT,
  credit_account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE RESTRICT,
  property_id INTEGER REFERENCES property(id) ON DELETE SET NULL,
  tenant_id INTEGER REFERENCES tenant(id) ON DELETE SET NULL,
  date DATE NOT NULL,
  amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
  description TEXT
);

CREATE INDEX IF NOT EXISTS ix_trans_date ON transaction(date);
CREATE INDEX IF NOT EXISTS ix_trans_property ON transaction(property_id);
CREATE INDEX IF NOT EXISTS ix_trans_tenant ON transaction(tenant_id);
CREATE INDEX IF NOT EXISTS ix_rent_prop ON rent(property_id);
