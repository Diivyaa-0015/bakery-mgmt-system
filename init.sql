CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(6, 2),
    stock INT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    quantity INT,
    status VARCHAR(50)
);

-- Optional: seed with some dummy products
INSERT INTO products (name, price, stock) VALUES
('Chocolate Cake', 15.99, 10),
('Croissant', 2.50, 25),
('Baguette', 3.00, 20);
 
