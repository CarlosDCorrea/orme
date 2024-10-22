CREATE TABLE if not exists debts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value INTEGER NOT NULL,
    deptor TEXT,
    lender TEXT,
    description TEXT,
    interest_rate REAL NOT NULL,
    months INTEGER DEFAULT 60,
    date TEXT,
    created TEXT,
    updated TEXT
);