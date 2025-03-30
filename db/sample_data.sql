
-- Insert customers
INSERT INTO customer (id, full_name, email) VALUES
(1, 'Alice Dupont', 'alice@example.com'),
(2, 'Bruno Marchand', 'bruno@example.com'),
(3, 'Claire Fontaine', 'claire@example.com'),
(4, 'David Rousseau', 'david@example.com');  -- Without account

-- Insert banks
INSERT INTO bank (id, name, cashier_check_validity_pattern) VALUES
(1, 'Banque Nationale', 'BNK[0-9]{6}'),
(2, 'Credit Maritime', 'CM[0-9]{5}');

-- Insert accounts
-- Note: The 3rd account references a non-existent bank (bank_id=999)
INSERT INTO account (id, customer_id, bank_id, account_number, balance) VALUES
(1, 1, 1, 'BNK000123456', 12500.00),
(2, 2, 2, 'CM00054321', 9800.75),
(3, 3, 999, 'FAKE99999999', 450.50);  -- Banque inexistante

-- Insert banking transactions (only for accounts 1 and 2)
INSERT INTO banking_transaction (account_id, transaction_type, amount) VALUES
(1, 'deposit', 1000.00),
(1, 'withdrawal', 200.00),
(1, 'deposit', 500.00),
(2, 'deposit', 2000.00),
(2, 'withdrawal', 300.25),
(2, 'withdrawal', 250.00);

-- Insert a loan application for Alice (customer_id=1)
INSERT INTO loan_application (customer_id, account_id, loan_type, loan_amount, loan_description, status) VALUES
(1, 1, 'personal', 15000.00, 'Refinancement de crédit auto', 'pending');

-- Insert a cashier's check for Bruno (customer_id=2, account_id=2)
INSERT INTO cashier_check (account_id, bank_id, check_number, issue_date, amount, is_valid) VALUES
(2, 2, 'CM12345', '2024-03-01 10:00:00', 10000.000, true);
