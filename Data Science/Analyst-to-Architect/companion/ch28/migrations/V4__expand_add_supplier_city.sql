ALTER TABLE suppliers ADD COLUMN supplier_city VARCHAR(50);
UPDATE suppliers SET supplier_city = city;
