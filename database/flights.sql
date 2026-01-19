    create table if not exists flights(
        flight_id INTEGER PRIMARY KEY,
        flight_date DATE,
        airline TEXT,
        origin TEXT,
        destination TEXT,
        sched_dep_time TIME,
        actual_dep_time TIME,
        delay_minutes INTEGER
    );

