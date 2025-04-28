SELECT:
1. SELECT v.First_name, v.Last_name, 
       EXTRACT(MONTH FROM vol.Date) AS Month, 
       SUM(vol.Duration) AS Total_Hours
FROM Volunteer v
JOIN Volunteering_Participation vp ON v.Volunteer_id = vp.Volunteer_id
JOIN Volunteering vol ON vp.Volunteering_id = vol.Volunteering_id
GROUP BY v.Volunteer_id, EXTRACT(MONTH FROM vol.Date)
ORDER BY Month;

2. 
WITH AgeData AS (
    SELECT volp.Volunteer_id, 
           vol.Duration,
           EXTRACT(YEAR FROM age(CURRENT_DATE, v.Birthday))::int AS Age
    FROM volunteering_participation volp
    JOIN volunteering vol ON volp.Volunteering_id = vol.Volunteering_id
    JOIN Volunteer v ON volp.Volunteer_id = v.Volunteer_id
)
SELECT CASE
           WHEN Age BETWEEN 0 AND 17 THEN '16-18'
           WHEN Age BETWEEN 18 AND 25 THEN '19-25'
           WHEN Age BETWEEN 26 AND 40 THEN '26-40'
           WHEN Age BETWEEN 41 AND 60 THEN '41-60'
           ELSE '60+'
       END AS Age_Group,
       AVG(Duration) AS Avg_Hours
FROM AgeData
GROUP BY Age_Group
ORDER BY Age_Group;


3.
SELECT c.Name AS CityName, 
       c.Area, 
       COUNT(DISTINCT e.Event_id) AS TotalEvents,
       AVG(participants.ParticipantCount) AS AvgParticipantsPerEvent
FROM City c
JOIN Event e ON e.Location = c.name
LEFT JOIN (
    SELECT ep.Event_id, COUNT(ep.Volunteer_id) AS ParticipantCount
    FROM Event_participation ep
    GROUP BY ep.Event_id
) participants ON participants.Event_id = e.Event_id
GROUP BY c.Name, c.Area;

4.
SELECT 
    First_name,
    Last_name,
    Birthday,
    EXTRACT(YEAR FROM age(CURRENT_DATE, Birthday)) AS Age
FROM Volunteer
WHERE EXTRACT(MONTH FROM Birthday) = EXTRACT(MONTH FROM CURRENT_DATE);

5.
SELECT 
    v.First_name, 
    v.Last_name,
    COUNT(vp.Volunteering_id) AS Volunteering_Count,
    SUM(vol.Duration) AS Total_Hours
FROM Volunteer v
JOIN Volunteering_participation vp ON v.Volunteer_id = vp.Volunteer_id
JOIN Volunteering vol ON vp.Volunteering_id = vol.Volunteering_id
WHERE vol.Date >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY v.Volunteer_id
ORDER BY Total_Hours DESC
LIMIT 50;

6.
SELECT 
    c.Area, 
    COUNT(DISTINCT v.Volunteer_id) AS Active_Volunteer_Count
FROM Volunteer v
JOIN Volunteering_Participation vp ON v.Volunteer_id = vp.Volunteer_id
JOIN Volunteering vol ON vp.Volunteering_id = vol.Volunteering_id
JOIN City c ON vol.Location = c.Name
GROUP BY c.Area
ORDER BY Active_Volunteer_Count DESC;

7.
SELECT p.Patient_id, p.First_name, p.Last_name, p.Birthday
FROM Patient p
WHERE p.Patient_id NOT IN (
  SELECT DISTINCT v.Patient_id
  FROM Volunteering v
  WHERE v.Date >= CURRENT_DATE - INTERVAL '1 year'
);

8.
SELECT e.type, 
       EXTRACT(YEAR FROM e.Date) AS year,
       ROUND(
         COUNT(ep.volunteer_id) * 1.0 / COUNT(DISTINCT e.Event_id), 2
       ) AS average_participants_per_event
FROM Event e
LEFT JOIN Event_participation ep ON e.Event_id = ep.Event_id
GROUP BY e.type, EXTRACT(YEAR FROM e.Date)
ORDER BY year DESC, average_participants_per_event DESC;

UPDATE:
1.
UPDATE Volunteer
SET Active = 'F'
WHERE Volunteer_id NOT IN (
    SELECT DISTINCT vp.Volunteer_id
    FROM Volunteering_Participation vp
    JOIN Volunteering v ON vp.Volunteering_id = v.Volunteering_id
    WHERE v.Date >= CURRENT_DATE - INTERVAL '1 year'

    UNION

    SELECT DISTINCT ep.Volunteer_id
    FROM Event_participation ep
    JOIN Event e ON ep.Event_id = e.Event_id
    WHERE e.Date >= CURRENT_DATE - INTERVAL '1 year'
);

2.
UPDATE Event_participation ep
SET Plus_one = 'F'
WHERE ep.Event_id IN (
    SELECT e.Event_id
    FROM event e
    JOIN city c ON e.Location = c.name
    WHERE c.Area IN ('North', 'South')
);

3.
UPDATE Volunteering_participation vp
SET Shift = 'M'
FROM Volunteer v
WHERE vp.Volunteer_id = v.Volunteer_id
  AND vp.Shift = 'E'
  AND DATE_PART('year', AGE(CURRENT_DATE, v.Birthday)) < 18;

DELETE:
1.
WITH ToDelete AS (
    SELECT V.Volunteer_id
    FROM Volunteer V
    WHERE V.Volunteer_id NOT IN (
        SELECT DISTINCT EP.Volunteer_id
        FROM Event_participation EP
        JOIN Event E ON EP.Event_id = E.Event_id
        WHERE E.Date >= (CURRENT_DATE - INTERVAL '2 years')
        
        UNION
        
        SELECT DISTINCT VP.Volunteer_id
        FROM Volunteering_participation VP
        JOIN Volunteering VOL ON VP.Volunteering_id = VOL.Volunteering_id
        WHERE VOL.Date >= (CURRENT_DATE - INTERVAL '2 years')
    )
    AND V.Volunteer_id NOT IN (
        SELECT DISTINCT Volunteer_id
        FROM KindOfVol
        WHERE Volunteer_id IS NOT NULL
    )
    AND V.Volunteer_id NOT IN (
        SELECT DISTINCT Volunteer_id
        FROM Event
        WHERE Volunteer_id IS NOT NULL
    )
)
-- מחיקת המתנדבים מהטבלה של השתתפות באירועים
DELETE FROM Event_participation
WHERE Volunteer_id IN (SELECT Volunteer_id FROM ToDelete);

WITH ToDelete AS (
    SELECT V.Volunteer_id
    FROM Volunteer V
    WHERE V.Volunteer_id NOT IN (
        SELECT DISTINCT EP.Volunteer_id
        FROM Event_participation EP
        JOIN Event E ON EP.Event_id = E.Event_id
        WHERE E.Date >= (CURRENT_DATE - INTERVAL '2 years')
        
        UNION
        
        SELECT DISTINCT VP.Volunteer_id
        FROM Volunteering_participation VP
        JOIN Volunteering VOL ON VP.Volunteering_id = VOL.Volunteering_id
        WHERE VOL.Date >= (CURRENT_DATE - INTERVAL '2 years')
    )
    AND V.Volunteer_id NOT IN (
        SELECT DISTINCT Volunteer_id
        FROM KindOfVol
        WHERE Volunteer_id IS NOT NULL
    )
    AND V.Volunteer_id NOT IN (
        SELECT DISTINCT Volunteer_id
        FROM Event
        WHERE Volunteer_id IS NOT NULL
    )
)
-- מחיקת המתנדבים מהטבלה של השתתפות בהתנדבויות
DELETE FROM Volunteering_participation
WHERE Volunteer_id IN (SELECT Volunteer_id FROM ToDelete);

WITH ToDelete AS (
    SELECT V.Volunteer_id
    FROM Volunteer V
    WHERE V.Volunteer_id NOT IN (
        SELECT DISTINCT EP.Volunteer_id
        FROM Event_participation EP
        JOIN Event E ON EP.Event_id = E.Event_id
        WHERE E.Date >= (CURRENT_DATE - INTERVAL '2 years')
        
        UNION
        
        SELECT DISTINCT VP.Volunteer_id
        FROM Volunteering_participation VP
        JOIN Volunteering VOL ON VP.Volunteering_id = VOL.Volunteering_id
        WHERE VOL.Date >= (CURRENT_DATE - INTERVAL '2 years')
    )
    AND V.Volunteer_id NOT IN (
        SELECT DISTINCT Volunteer_id
        FROM KindOfVol
        WHERE Volunteer_id IS NOT NULL
    )
    AND V.Volunteer_id NOT IN (
        SELECT DISTINCT Volunteer_id
        FROM Event
        WHERE Volunteer_id IS NOT NULL
    )
)
-- מחיקת המתנדבים עצמם
DELETE FROM Volunteer
WHERE Volunteer_id IN (SELECT Volunteer_id FROM ToDelete);

2.
DELETE FROM Volunteering
WHERE Patient_id IN (
  SELECT Patient_id
  FROM Patient
  WHERE AGE(Birthday) > INTERVAL '120 years'
);

DELETE FROM Patient
WHERE AGE(Birthday) > INTERVAL '120 years';

3.
DELETE FROM Event_participation
WHERE event_id IN (
  SELECT event_id
  FROM Event
  WHERE Date < CURRENT_DATE - INTERVAL '5 years'
);

DELETE FROM Event
WHERE Date < CURRENT_DATE - INTERVAL '5 years';