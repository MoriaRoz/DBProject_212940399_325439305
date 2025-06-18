-- View showing each volunteer's participation in volunteering activities including contact info, date, type and report
CREATE OR REPLACE VIEW view_volunteer_participation AS
SELECT 
    v.volunteer_id,
    v.first_name,
    v.last_name,
    v.phone,
    v.city_of_residence,
    vp.volunteering_id,
    vol.date,
    vol.type,
    vol.report
FROM volunteer v
JOIN volunteering_participation vp ON v.volunteer_id = vp.volunteer_id
JOIN volunteering vol ON vp.volunteering_id = vol.volunteering_id
ORDER BY v.volunteer_id;

-- Q1: Count the number of volunteering activities for each type
SELECT type, COUNT(*) AS total_volunteering
FROM view_volunteer_participation
GROUP BY type;

-- Q2: List volunteers who participated in at least 3 volunteering activities, sorted by participation count
SELECT 
    v.volunteer_id,
    v.first_name,
    v.last_name,
    COUNT(vp.volunteering_id) AS total_participations
FROM volunteer v
JOIN volunteering_participation vp ON v.volunteer_id = vp.volunteer_id
GROUP BY v.volunteer_id, v.first_name, v.last_name
HAVING COUNT(vp.volunteering_id) >= 3
ORDER BY total_participations DESC;

-- View showing full ride details including date, pickup time, destination, vehicle, driver and assistant info
CREATE OR REPLACE VIEW view_rides_schedule AS
SELECT 
    r.volunteering_id,
    vol.date AS volunteering_date,
    r.pickup_time,
    d.destination_name,
    d.destination_address,
    v.license_plate,
    v.type AS vehicle_type,
    dr.volunteer_id AS driver_id,
    drv.first_name AS driver_first_name,
    drv.last_name AS driver_last_name,
    drv.phone AS driver_phone,
    ta.volunteer_id AS assistant_id,
    ast.first_name AS assistant_first_name,
    ast.last_name AS assistant_last_name
FROM ride r
JOIN volunteering vol ON r.volunteering_id = vol.volunteering_id
JOIN destination d ON r.destination_name = d.destination_name AND r.destination_address = d.destination_address
JOIN vehicle v ON r.vehicle_id = v.vehicle_id
JOIN driver dr ON r.driver_id = dr.volunteer_id
JOIN volunteer drv ON dr.volunteer_id = drv.volunteer_id
LEFT JOIN transport_assistant ta ON r.assistant_id = ta.volunteer_id
LEFT JOIN volunteer ast ON ta.volunteer_id = ast.volunteer_id
ORDER BY r.volunteering_id;

-- Q1: Show rides that have no assigned assistant, including driver name and phone
SELECT 
    volunteering_id,
    volunteering_date,
    pickup_time,
    driver_first_name,
    driver_last_name,
    driver_phone
FROM view_rides_schedule
WHERE assistant_id IS NULL;

-- Q2: Count the number of rides per month and year
SELECT 
    EXTRACT(YEAR FROM volunteering_date) AS year,
    EXTRACT(MONTH FROM volunteering_date) AS month,
    COUNT(*) AS total_rides
FROM view_rides_schedule
GROUP BY year, month
ORDER BY year, month;
