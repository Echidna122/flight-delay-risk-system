-- 1. View all flights
SELECT * FROM flights;

-- 2. Find all delayed flights
SELECT *
FROM flights
WHERE delay_minutes > 0;

-- 3. Find flights delayed more than 30 minutes
SELECT *
FROM flights
WHERE delay_minutes > 30;

-- 4. Average delay by airline
SELECT airline, AVG(delay_minutes) AS avg_delay
FROM flights
GROUP BY airline;

-- 5. Count of flights per airline
SELECT airline, COUNT(*) AS total_flights
FROM flights
GROUP BY airline;
