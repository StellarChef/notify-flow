CREATE TABLE orders(
    id SERIAL PRIMARY KEY,
    order_id TEXT UNIQUE,
    status TEXT,
    data JSONB,
    created_at TIMESTAMP DEFAULT now()
)