-- Minimal seed data for accounting types and common accounts
INSERT INTO company (name, tin) VALUES
('Redbrick Holdings', '11-22-33'),
('Redbrick Enterprises', '11-22-44')
ON CONFLICT (name) DO NOTHING;
 
INSERT INTO account_type (code, name, description) VALUES
('ASSET','Assets','Resources owned'),
('LIABILITY','Liabilities','Obligations owed'),
('EQUITY','Equity','Owner equity'),
('REVENUE','Revenue','Income accounts'),
('EXPENSE','Expense','Expense accounts')
ON CONFLICT (code) DO NOTHING;

-- Example sub types (optional)
INSERT INTO account_sub_type (type_id, code, name) VALUES
((SELECT id FROM account_type WHERE code='ASSET'), 'CASH', 'Cash'),
((SELECT id FROM account_type WHERE code='ASSET'), 'AR', 'Accounts Receivable'),
((SELECT id FROM account_type WHERE code='LIABILITY'), 'AP', 'Accounts Payable'),
((SELECT id FROM account_type WHERE code='REVENUE'), 'RENT_INC', 'Rental Income'),
((SELECT id FROM account_type WHERE code='EXPENSE'), 'MAINT', 'Maintenance Expense'),
((SELECT id FROM account_type WHERE code='EXPENSE'), 'UTIL', 'Utilities Expense')
ON CONFLICT (code) DO NOTHING;

-- Example accounts
INSERT INTO account (type_id, sub_type_id, name) VALUES
((SELECT id FROM account_type WHERE code='ASSET'), (SELECT id FROM account_sub_type WHERE code='CASH'), 'Cash'),
((SELECT id FROM account_type WHERE code='REVENUE'), (SELECT id FROM account_sub_type WHERE code='RENT_INC'), 'Rental Income'),
((SELECT id FROM account_type WHERE code='EXPENSE'), (SELECT id FROM account_sub_type WHERE code='MAINT'), 'Maintenance Expense')
ON CONFLICT (name) DO NOTHING;
