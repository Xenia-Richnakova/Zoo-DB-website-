CREATE TABLE IF NOT EXISTS zoo(
    key INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    spiece TEXT, 
    origin_country TEXT,
    birth_date TEXT,
    food TEXT,
    feeding_time TEXT,
    last_cleaning TEXT,
    caregiver_key INTEGER,
    cage_key INTEGER
);


