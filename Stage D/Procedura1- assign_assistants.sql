CREATE OR REPLACE PROCEDURE assign_assistants_to_future_rides()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    candidate RECORD;
    ride_date DATE;
    ride_start TIME;
    ride_end TIME;
    assigned BOOLEAN;
BEGIN
    FOR r IN
        SELECT DISTINCT ON (rd.volunteering_id)
               rd.volunteering_id, rd.destination_name,
               d.destination_city, c.area,
               v.date AS ride_date, v.hour, v.duration
        FROM ride rd
        JOIN volunteering v ON rd.volunteering_id = v.volunteering_id
        JOIN destination d ON rd.destination_name = d.destination_name
        JOIN city c ON d.destination_city = c.name
        WHERE rd.assistant_id IS NULL
          AND v.date > CURRENT_DATE
        ORDER BY rd.volunteering_id, v.date
    LOOP
        ride_date := r.ride_date;
        ride_start := MAKE_TIME(r.hour, 0, 0);
        ride_end := ride_start + make_interval(mins => r.duration);
        assigned := false;

        -- Step 1: Try city match
        FOR candidate IN
            SELECT ta.volunteer_id
            FROM transport_assistant ta
            JOIN volunteer v ON v.volunteer_id = ta.volunteer_id
            WHERE v.active = 'T'
              AND v.city_of_residence = r.destination_city
              AND NOT EXISTS (
                  -- Conflicting rides
                  SELECT 1 FROM ride r2
                  JOIN volunteering v2 ON r2.volunteering_id = v2.volunteering_id
                  WHERE r2.assistant_id = ta.volunteer_id
                    AND v2.date = ride_date
                    AND ride_start < (MAKE_TIME(v2.hour, 0, 0) + make_interval(mins => v2.duration))
                    AND ride_end > MAKE_TIME(v2.hour, 0, 0)
              )
              AND NOT EXISTS (
                  -- Conflicting volunteering
                  SELECT 1 FROM volunteering_participation vp
                  JOIN volunteering vln ON vp.volunteering_id = vln.volunteering_id
                  WHERE vp.volunteer_id = ta.volunteer_id
                    AND vln.date = ride_date
                    AND ride_start < (MAKE_TIME(vln.hour, 0, 0) + make_interval(mins => vln.duration))
                    AND ride_end > MAKE_TIME(vln.hour, 0, 0)
              )
              AND NOT EXISTS (
                  -- Any event on that day
                  SELECT 1 FROM event_participation ep
                  JOIN event e ON ep.event_id = e.event_id
                  WHERE ep.volunteer_id = ta.volunteer_id
                    AND e.date = ride_date
              )
            LIMIT 1
        LOOP
            BEGIN
                UPDATE ride
                SET assistant_id = candidate.volunteer_id
                WHERE volunteering_id = r.volunteering_id;
                RAISE NOTICE '✔️ Assigned assistant % to ride % (city match)', candidate.volunteer_id, r.volunteering_id;
                assigned := true;
                EXIT;
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLERRM LIKE '⛔ Assistant % already assigned to % rides on % – limit is 3%' THEN
                        RAISE NOTICE '🎯 Could not assign assistant % to ride % – already has 3 rides that day.', candidate.volunteer_id, r.volunteering_id;
                    ELSE
                        RAISE EXCEPTION 'Unexpected error: %', SQLERRM;
                    END IF;
            END;
        END LOOP;

        -- Step 2: Try area match (similar to above)
        IF NOT assigned THEN
            FOR candidate IN
                SELECT ta.volunteer_id
                FROM transport_assistant ta
                JOIN volunteer v ON v.volunteer_id = ta.volunteer_id
                JOIN city c ON v.city_of_residence = c.name
                WHERE v.active = 'T'
                  AND c.area = r.area
                  AND NOT EXISTS (
                      SELECT 1 FROM ride r2
                      JOIN volunteering v2 ON r2.volunteering_id = v2.volunteering_id
                      WHERE r2.assistant_id = ta.volunteer_id
                        AND v2.date = ride_date
                        AND ride_start < (MAKE_TIME(v2.hour, 0, 0) + make_interval(mins => v2.duration))
                        AND ride_end > MAKE_TIME(v2.hour, 0, 0)
                  )
                  AND NOT EXISTS (
                      SELECT 1 FROM volunteering_participation vp
                      JOIN volunteering vln ON vp.volunteering_id = vln.volunteering_id
                      WHERE vp.volunteer_id = ta.volunteer_id
                        AND vln.date = ride_date
                        AND ride_start < (MAKE_TIME(vln.hour, 0, 0) + make_interval(mins => vln.duration))
                        AND ride_end > MAKE_TIME(vln.hour, 0, 0)
                  )
                  AND NOT EXISTS (
                      SELECT 1 FROM event_participation ep
                      JOIN event e ON ep.event_id = e.event_id
                      WHERE ep.volunteer_id = ta.volunteer_id
                        AND e.date = ride_date
                  )
                LIMIT 1
            LOOP
                BEGIN
                    UPDATE ride
                    SET assistant_id = candidate.volunteer_id
                    WHERE volunteering_id = r.volunteering_id;
                    RAISE NOTICE '✔️ Assigned assistant % to ride % (area match)', candidate.volunteer_id, r.volunteering_id;
                    assigned := true;
                    EXIT;
                EXCEPTION
                    WHEN OTHERS THEN
                        IF SQLERRM LIKE '⛔ Assistant % already assigned to % rides on % – limit is 3%' THEN
                            RAISE NOTICE '🎯 Could not assign assistant % to ride % – already has 3 rides that day.', candidate.volunteer_id, r.volunteering_id;
                        ELSE
                            RAISE EXCEPTION 'Unexpected error: %', SQLERRM;
                        END IF;
                END;
            END LOOP;
        END IF;

        IF NOT assigned THEN
            RAISE NOTICE '⚠️ No assistant found for ride % on %', r.volunteering_id, ride_date;
        END IF;
    END LOOP;
END;
$$;
