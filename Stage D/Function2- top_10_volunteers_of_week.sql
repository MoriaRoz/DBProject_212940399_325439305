CREATE OR REPLACE FUNCTION get_top_10_volunteers_of_week()
RETURNS refcursor AS $$
DECLARE
    cur refcursor := 'top10_cursor';
    temp RECORD;
    count_check INT;
BEGIN
    -- בדיקה אם יש לפחות מתנדב אחד עם פעילות השבוע
    SELECT COUNT(*) INTO count_check FROM (
        SELECT volunteer_id FROM (
            SELECT vp.volunteer_id
            FROM volunteering_participation vp
            JOIN volunteering vo ON vp.volunteering_id = vo.volunteering_id
            WHERE vo.date >= CURRENT_DATE - INTERVAL '7 days'

            UNION ALL

            SELECT r.driver_id AS volunteer_id
            FROM ride r
            JOIN volunteering v ON r.volunteering_id = v.volunteering_id
            WHERE v.date >= CURRENT_DATE - INTERVAL '7 days'

            UNION ALL

            SELECT r.assistant_id AS volunteer_id
            FROM ride r
            JOIN volunteering v ON r.volunteering_id = v.volunteering_id
            WHERE v.date >= CURRENT_DATE - INTERVAL '7 days'

            UNION ALL

            SELECT ep.volunteer_id
            FROM event_participation ep
            JOIN event e ON ep.event_id = e.event_id
            WHERE e.date >= CURRENT_DATE - INTERVAL '7 days'
        ) AS all_ids
    ) AS all_volunteers;

    IF count_check = 0 THEN
        RAISE NOTICE 'ℹ️ No volunteer activities found in the last 7 days.';
        OPEN cur FOR
        SELECT NULL::INT AS volunteer_id, NULL::TEXT AS full_name, NULL::INT AS total_activities;
        RETURN cur;
    END IF;

    -- אם יש תוצאות – פתח Cursor
    OPEN cur FOR
    SELECT 
        v.volunteer_id,
        v.first_name || ' ' || v.last_name AS full_name,
        COUNT(*) AS total_activities
    FROM (
        SELECT vp.volunteer_id, vo.date
        FROM volunteering_participation vp
        JOIN volunteering vo ON vp.volunteering_id = vo.volunteering_id
        WHERE vo.date >= CURRENT_DATE - INTERVAL '7 days'

        UNION ALL

        SELECT r.driver_id AS volunteer_id, v.date
        FROM ride r
        JOIN volunteering v ON r.volunteering_id = v.volunteering_id
        WHERE v.date >= CURRENT_DATE - INTERVAL '7 days'

        UNION ALL

        SELECT r.assistant_id AS volunteer_id, v.date
        FROM ride r
        JOIN volunteering v ON r.volunteering_id = v.volunteering_id
        WHERE v.date >= CURRENT_DATE - INTERVAL '7 days'

        UNION ALL

        SELECT ep.volunteer_id, e.date
        FROM event_participation ep
        JOIN event e ON ep.event_id = e.event_id
        WHERE e.date >= CURRENT_DATE - INTERVAL '7 days'
    ) AS all_activities
    JOIN volunteer v ON v.volunteer_id = all_activities.volunteer_id
    GROUP BY v.volunteer_id, v.first_name, v.last_name
    ORDER BY total_activities DESC
    LIMIT 10;

    RETURN cur;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE '⚠️ Unexpected error occurred: %', SQLERRM;
        OPEN cur FOR SELECT NULL::INT, NULL::TEXT, NULL::INT;
        RETURN cur;
END;
$$ LANGUAGE plpgsql;
