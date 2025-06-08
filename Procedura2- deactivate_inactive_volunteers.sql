CREATE OR REPLACE PROCEDURE deactivate_inactive_volunteers()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT v.volunteer_id, v.first_name, v.last_name
        FROM volunteer v
        WHERE v.active = 'T'
          AND NOT EXISTS (
              SELECT 1 FROM volunteering_participation vp
              JOIN volunteering vl ON vp.volunteering_id = vl.volunteering_id
              WHERE vp.volunteer_id = v.volunteer_id
                AND vl.date >= CURRENT_DATE - INTERVAL '6 months'
          )
          AND NOT EXISTS (
              SELECT 1 FROM event_participation ep
              JOIN event e ON ep.event_id = e.event_id
              WHERE ep.volunteer_id = v.volunteer_id
                AND e.date >= CURRENT_DATE - INTERVAL '6 months'
          )
          AND NOT EXISTS (
              SELECT 1 FROM ride r
              JOIN volunteering vl ON r.volunteering_id = vl.volunteering_id
              WHERE (r.driver_id = v.volunteer_id OR r.assistant_id = v.volunteer_id)
                AND vl.date >= CURRENT_DATE - INTERVAL '6 months'
          )
    LOOP
        BEGIN
            UPDATE volunteer
            SET active = 'F'
            WHERE volunteer_id = rec.volunteer_id;

            RAISE NOTICE '✅ Volunteer % % (ID: %) marked as inactive.', rec.first_name, rec.last_name, rec.volunteer_id;

        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE '⚠️ Could not deactivate volunteer % % (ID: %): %',
                    rec.first_name, rec.last_name, rec.volunteer_id, SQLERRM;
        END;
    END LOOP;

    RAISE NOTICE '🎯 Deactivation process completed.';
END;
$$;