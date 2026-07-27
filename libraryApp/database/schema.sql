CREATE TABLE IF NOT EXISTS publishers (
    id TEXT PRIMARY KEY,

    created_at TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_at TEXT,
    updated_by TEXT,
    is_deleted INTEGER NOT NULL DEFAULT 0,
    deleted_at TEXT,
    row_version INTEGER NOT NULL DEFAULT 1,

    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    founded_year INTEGER,
    city TEXT,
    country TEXT,
    address TEXT ,
    email TEXT,
    phone TEXT,
    website TEXT,
    logo_url TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    

    CHECK (is_deleted IN (0,1)),
    CHECK(is_active IN (0,1)),
    CHECK(row_version >=1 )


)