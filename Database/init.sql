-- Uruchamia się AUTOMATYCZNIE przy pierwszym starcie kontenera Postgres
-- (gdy wolumen pgdata jest jeszcze pusty). Tworzy tabelę pod push_order().

CREATE TABLE IF NOT EXISTS orders (
    id          SERIAL PRIMARY KEY,         -- wewnętrzne ID, baza nadaje sama
    order_id    TEXT UNIQUE,                -- ID ze sklepu ("1053") - do wyszukiwania
    status      TEXT,                       -- status wyciągnięty na wierzch (łatwe filtrowanie)
    data        JSONB,                      -- CAŁY OrderJSON jako źródło prawdy
    created_at  TIMESTAMP DEFAULT now()
);
