-- Insert customers
INSERT INTO customer (full_name, email) VALUES
('Alice Dupont', 'alice@example.com'),
('Bruno Marchand', 'bruno@example.com'),
('Claire Fontaine', 'claire@example.com'),
('David Rousseau', 'david@example.com');  -- Without account

-- Insert banks
INSERT INTO bank (name, account_number_validity_pattern, cashier_check_validity_pattern) VALUES
('Banque Nationale', 'BNK[0-9]{4}', 'BNK[0-9]{8}'),
('Credit Maritime', 'CM[0-9]{4}', 'CM[0-9]{8}');

-- Insert accounts
INSERT INTO account (customer_id, bank_id, account_number, balance) VALUES
(1, 1, 'BNK0123', 12500.00),
(2, 2, 'CM5874', 9800.75),
(3, 1, 'BNK5726', 1500.00),
(3, 2, 'CM5720', 2500.00);

-- Insert banking transactions (only for accounts 1 and 2)
INSERT INTO banking_transaction (account_id, transaction_type, amount) VALUES
(1, 'deposit', 1000.00),
(1, 'withdrawal', 200.00),
(1, 'deposit', 500.00),
(2, 'deposit', 2000.00),
(2, 'withdrawal', 300.25),
(2, 'withdrawal', 250.00),
(3, 'deposit', 1500.00),
(3, 'withdrawal', 100.00),
(3, 'deposit', 200.00),
(4, 'withdrawal', 500.00),
(4, 'deposit', 1000.00),
(4, 'withdrawal', 300.00),
(4, 'deposit', 500.00),
(4, 'withdrawal', 200.00);

-- Insert a cashier's check for Bruno (customer_id=2, account_id=2)
INSERT INTO cashier_check (account_id, check_number, issue_date, amount, is_valid, created_at) VALUES
(2, 'CM12345678', '2024-03-01 10:00:00', 10000.000, true, '2024-01-01 10:00:00');
