CREATE OR REPLACE FUNCTION enforce_assistant_daily_limit()
RETURNS TRIGGER AS $$
DECLARE
    ride_count INT;
    ride_date DATE;
BEGIN
    -- קבלת תאריך הנסיעה מתוך טבלת ההתנדבות
    SELECT date INTO ride_date
    FROM volunteering
    WHERE volunteering_id = NEW.volunteering_id;

    -- בדיקה אם יש עוזר נסיעה (השדה הוא אופציונלי)
    IF NEW.assistant_id IS NULL THEN
        RETURN NEW;  -- אם אין עוזר, אין מה לבדוק
    END IF;

    -- ספירת נסיעות קיימות של אותו עוזר באותו תאריך
    SELECT COUNT(*) INTO ride_count
    FROM ride r
    JOIN volunteering v ON r.volunteering_id = v.volunteering_id
    WHERE r.assistant_id = NEW.assistant_id
      AND v.date = ride_date;

    -- הגבלת מקסימום נסיעות לעוזר (3 ביום)
    IF ride_count >= 3 THEN
        RAISE EXCEPTION '⛔ Assistant % already assigned to % rides on % – limit is 3',
            NEW.assistant_id, ride_count, ride_date;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_limit_assistant_rides
BEFORE INSERT OR UPDATE ON ride
FOR EACH ROW
EXECUTE FUNCTION enforce_assistant_daily_limit();
