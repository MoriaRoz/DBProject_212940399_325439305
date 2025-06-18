DO $$
DECLARE
    volunteer_id INT := 10000101;  -- תז של המתנדב שבשבילו מחפשים את הלו"ז השבועי
    cur refcursor;
    rec RECORD;
BEGIN
    CALL assign_assistants_to_future_rides();

    cur := get_volunteer_schedule(volunteer_id);
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Activity: %, Date: %, Time: %, Location: %',
            rec.activity_type, rec.date, rec.make_time, rec.location;
    END LOOP;

    CLOSE cur;
END;
$$;
