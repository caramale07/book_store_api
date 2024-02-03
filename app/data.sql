CREATE TABLE IF NOT EXISTS users
(
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS  book_store
(
    book_id SERIAL PRIMARY KEY,
    author_name VARCHAR(255),
    book_name VARCHAR(255),
    publish_year INTEGER,
    price NUMERIC(10,2)
);

INSERT INTO book_store (author_name, book_name, publish_year, price)
VALUES 
  ('Author1', 'Book1', 2020, 29.99),
  ('Author2', 'Book2', 2018, 19.99),
  ('Author3', 'Book3', 2022, 39.99);
