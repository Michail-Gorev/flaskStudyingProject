CREATE TABLE IF NOT EXISTS buildings (
    id integer PRIMARY KEY AUTOINCREMENT,
    building_name varchar NOT NULL UNIQUE,
    description text NOT NULL,
    pic_url varchar NOT NULL
);