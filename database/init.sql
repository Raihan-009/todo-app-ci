\c postgres;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'todos') THEN
        CREATE DATABASE todos;
    END IF;
END
$$;

\c todos;

-- Create the todo table if it doesn't exist
CREATE TABLE IF NOT EXISTS todo (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);