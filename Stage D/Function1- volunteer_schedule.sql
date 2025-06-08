CREATE OR REPLACE FUNCTION get_volunteer_schedule(v_id INT)
RETURNS refcursor AS $$
DECLARE
    cur refcursor := 'schedule_cursor';
    is_active CHAR;
BEGIN
    -- בדיקה אם המתנדב קיים ופעיל
    SELECT active INTO is_active
    FROM volunteer
    WHERE volunteer_id = v_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION '❌ Volunteer with ID % not found', v_id;
    ELSIF is_active <> 'T' THEN
        RAISE EXCEPTION '⛔ Volunteer with ID % is not active', v_id;
    END IF;

    -- פתיחת CURSOR לפעילויות בשבוע הקרוב
    OPEN cur FOR
    WITH all_activities AS (
        SELECT 'volunteering' AS activity_type, v.date, MAKE_TIME(v.hour,0,0) AS time, v.location
        FROM volunteering_participation vp
        JOIN volunteering v ON vp.volunteering_id = v.volunteering_id
        WHERE vp.volunteer_id = v_id
          AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

        UNION ALL

        SELECT 'ride (driver)', v.date, r.pickup_time, d.destination_address
        FROM ride r
        JOIN volunteering v ON r.volunteering_id = v.volunteering_id
        JOIN destination d ON r.destination_name = d.destination_name
        WHERE r.driver_id = v_id
          AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

        UNION ALL

        SELECT 'ride (assistant)', v.date, r.pickup_time, d.destination_address
        FROM ride r
        JOIN volunteering v ON r.volunteering_id = v.volunteering_id
        JOIN destination d ON r.destination_name = d.destination_name
        WHERE r.assistant_id = v_id
          AND v.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'

        UNION ALL

        SELECT 'event', e.date, e.start_time, e.location
        FROM event_participation ep
        JOIN event e ON ep.event_id = e.event_id
        WHERE ep.volunteer_id = v_id
          AND e.date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
    ),
    final_schedule AS (
        SELECT * FROM all_activities
        UNION ALL
        SELECT 'No scheduled activities this week', NULL, NULL, NULL
        WHERE NOT EXISTS (SELECT 1 FROM all_activities)
    )
    SELECT * FROM final_schedule
    ORDER BY date, time;

    RETURN cur;
END;
$$ LANGUAGE plpgsql;
