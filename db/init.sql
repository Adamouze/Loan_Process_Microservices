-- Tables Creation Script

-- Customer table
CREATE TABLE IF NOT EXISTS customer (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL
);

-- Bank table
CREATE TABLE IF NOT EXISTS bank (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  account_number_validity_pattern VARCHAR(100) NOT NULL UNIQUE,
  cashier_check_validity_pattern VARCHAR(100) NOT NULL UNIQUE
);

-- Account table
CREATE TABLE IF NOT EXISTS account (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
  bank_id INTEGER NOT NULL REFERENCES bank(id) ON DELETE CASCADE,
  account_number VARCHAR(20) UNIQUE NOT NULL,
  balance DECIMAL(15, 2) NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Banking transaction table
CREATE TABLE IF NOT EXISTS banking_transaction (
  id SERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  transaction_type VARCHAR(20) NOT NULL,
  amount DECIMAL(15, 2) NOT NULL,
  transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Loan application table
CREATE TABLE IF NOT EXISTS loan_application (
  id SERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  loan_type VARCHAR(20) NOT NULL,
  loan_amount DECIMAL(15, 2) NOT NULL,
  loan_description TEXT,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cashier_Check table
CREATE TABLE IF NOT EXISTS cashier_check (
  id SERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
  check_number VARCHAR(50) NOT NULL,
  issue_date TIMESTAMP NOT NULL,
  amount  DECIMAL(15, 2) NOT NULL,
  is_valid BOOLEAN NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (account_id, check_number)
);

-- Loan monitoring table
CREATE TABLE IF NOT EXISTS loan_monitoring (
  id SERIAL PRIMARY KEY,
  loan_application_id INTEGER NOT NULL REFERENCES loan_application(id) ON DELETE CASCADE,
  monitoring_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  risk_status VARCHAR(100),
  check_validation_status VARCHAR(100),
  loan_provider_status VARCHAR(100),
  notification_status VARCHAR(100),
  customer_status VARCHAR(100)
);