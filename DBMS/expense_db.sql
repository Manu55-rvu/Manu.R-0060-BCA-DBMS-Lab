CREATE DATABASE expenses_b;
USE expenses_b;
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    type ENUM('Income', 'Expense') NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    transaction_date DATE NOT NULL,
    notes VARCHAR(255)
);
INSERT INTO transactions
(title, type, category, amount, transaction_date, notes)
VALUES
('Pocket Money', 'Income', 'Allowance', 5000.00, '2026-10-01',
 'Monthly pocket money'),
('Lunch', 'Expense', 'Food', 150.00, '2026-10-02',
 'College lunch'),
('Bus Pass', 'Expense', 'Travel', 500.00, '2026-10-03',
 'Monthly bus pass');
SELECT * FROM transactions;
