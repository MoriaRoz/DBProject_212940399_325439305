CREATE OR REPLACE FUNCTION get_volunteer_schedule(volunteer_id INT)
RETURNS refcursor AS $$
DECLARE
    cur refcursor := 'schedule_cursor';
    is_active CHAR;
    activity_count INT;
    v_id INT := volunteer_id; -- העתק פרמטר לשם ברור
BEGIN
    -- בדיקה אם המתנדב קיים ופעיל
    SELECT active INTO is_active
    FROM volunteer
    WHERE volunteer.volunteer_id = v_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION '❌ Volunteer with ID % not found', v_id;
    ELSIF is_active <> 'T' THEN
        RAISE EXCEPTION '⛔ Volunteer with ID % is not active', v_id;
    END IF;

    -- בדיקה אם יש פעילויות בשבוע הקרוב
    SELECT COUNT(*) INTO activity_count
    FROM (
        SELECT 1
        FROM volunteering_participation vp
        JOIN volunteering v ON vp.volunteering_id = v.volunteering_id
        WHERE vp.volunteer_id = v_id
          AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

        UNION ALL

        SELECT 1
        FROM ride r
        JOIN volunteering v ON r.volunteering_id = v.volunteering_id
        WHERE (r.driver_id = v_id OR r.assistant_id = v_id)
          AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

        UNION ALL

        SELECT 1
        FROM event_participation ep
        JOIN event e ON ep.event_id = e.event_id
        WHERE ep.volunteer_id = v_id
          AND e.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
    ) AS activities;

    IF activity_count = 0 THEN
    RAISE NOTICE 'ℹ️ Volunteer % has no scheduled activities in the next 7 days.', v_id;

    OPEN cur FOR
    SELECT 
        'No scheduled activities this week' AS activity_type,
        NULL::date AS date,
        NULL::time AS time,
        NULL::text AS location;

    RETURN cur;
	END IF;

    -- פתיחת cursor
    OPEN cur FOR
    SELECT
        'volunteering' AS activity_type,
        v.date,
        MAKE_TIME(v.hour, 0, 0),
        v.location
    FROM volunteering_participation vp
    JOIN volunteering v ON vp.volunteering_id = v.volunteering_id
    WHERE vp.volunteer_id = v_id
      AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

    UNION ALL

    SELECT
        'ride (driver)' AS activity_type,
        v.date,
        r.pickup_time,
        d.destination_address
    FROM ride r
    JOIN destination d ON r.destination_name = d.destination_name
    JOIN volunteering v ON r.volunteering_id = v.volunteering_id
    WHERE r.driver_id = v_id
      AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

    UNION ALL

    SELECT
        'ride (assistant)' AS activity_type,
        v.date,
        r.pickup_time,
        d.destination_address
    FROM ride r
    JOIN destination d ON r.destination_name = d.destination_name
    JOIN volunteering v ON r.volunteering_id = v.volunteering_id
    WHERE r.assistant_id = v_id
      AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

    UNION ALL

    SELECT
        'event' AS activity_type,
        e.date,
        e.start_time,
        e.location
    FROM event_participation ep
    JOIN event e ON ep.event_id = e.event_id
    WHERE ep.volunteer_id = v_id
      AND e.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days';

    RETURN cur;
END;
$$ LANGUAGE plpgsql;