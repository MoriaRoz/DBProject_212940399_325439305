DO $$
DECLARE
    cur refcursor;
    rec RECORD;
BEGIN
    CALL deactivate_inactive_volunteers();

    cur := get_top_10_volunteers_of_week();
	RAISE NOTICE 'This week''s top 10: 🎉';
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;
        RAISE NOTICE 'Volunteer ID: %, Name: %, Total: %',
            rec.volunteer_id, rec.full_name, rec.total_activities;
    END LOOP;

    CLOSE cur;
END;
$$;
