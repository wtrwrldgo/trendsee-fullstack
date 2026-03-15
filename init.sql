CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS publications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed a test user
INSERT INTO users (id, name) VALUES (1, 'Test User') ON CONFLICT DO NOTHING;

-- Seed some test publications (some old, some new to test Redis cache logic)
-- E.g. 15 publications, meaning some will trigger pagination
INSERT INTO publications (user_id, title, text, created_at)
SELECT 1, 'Post ' || i, 'This is the body text for post number ' || i, NOW() - (i * INTERVAL '1 day')
FROM generate_series(1, 15) as s(i);
