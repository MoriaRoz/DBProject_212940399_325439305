-- פונקציית טריגר
CREATE OR REPLACE FUNCTION prevent_deactivating_active_responsible()
RETURNS TRIGGER AS $$
DECLARE
    future_event_count INT;
    volunteering_type_count INT;
BEGIN
    -- נבדוק רק אם רוצים להפוך ל'F'
    IF NEW.active = 'F' AND OLD.active = 'T' THEN

        -- בדיקה אם הוא אחראי על אירועים עתידיים
        SELECT COUNT(*) INTO future_event_count
        FROM event
        WHERE volunteer_id = NEW.volunteer_id
          AND date > CURRENT_DATE;

        IF future_event_count > 0 THEN
            RAISE EXCEPTION '⛔ Cannot deactivate volunteer % – responsible for % future event(s)',
                NEW.volunteer_id, future_event_count;
        END IF;

        -- בדיקה אם הוא אחראי על סוגי התנדבות
        SELECT COUNT(*) INTO volunteering_type_count
        FROM kindOfVol
        WHERE volunteer_id = NEW.volunteer_id;

        IF volunteering_type_count > 0 THEN
            RAISE EXCEPTION '⛔ Cannot deactivate volunteer % – responsible for % volunteering type(s)',
                NEW.volunteer_id, volunteering_type_count;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- יצירת הטריגר עצמו
CREATE TRIGGER trg_prevent_inactive_responsible
BEFORE UPDATE ON volunteer
FOR EACH ROW
EXECUTE FUNCTION prevent_deactivating_active_responsible();
