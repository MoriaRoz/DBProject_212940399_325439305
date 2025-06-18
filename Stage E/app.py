import flask
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2 import errors

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="mydatabase",
        user="myuser",
        password="mypassword"
    )
    return conn
def get_top_volunteers():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("BEGIN;")
        cur.execute("SELECT get_top_10_volunteers_of_week();")
        cur.execute("FETCH ALL FROM top10_cursor;")
        rows = cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print("❌ Error:", e)
        rows = []
        cur.execute("ROLLBACK;")
    finally:
        cur.close()
        conn.close()

    # החזרת רשימה של שמות
    return [row[1] for row in rows]
@app.route('/')
def home():
    volunteers = get_top_volunteers()
    return render_template("home.html", volunteers=volunteers)
@app.route('/personal_area/<int:volunteer_id>', methods=['GET', 'POST'])
def personal_area(volunteer_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # שליפת לוח זמנים
    schedule = []
    try:
        cur.execute("BEGIN;")
        cur.execute(f"SELECT get_volunteer_schedule({volunteer_id});")
        cur.execute("FETCH ALL IN schedule_cursor;")
        schedule = cur.fetchall()
        cur.execute("COMMIT;")
    except Exception as e:
        print("❌ Schedule error:", e)
        cur.execute("ROLLBACK;")

    # אם POST – לעדכן פרטים
    if flask.request.method == 'POST':
        first = flask.request.form['first_name']
        last = flask.request.form['last_name']
        birth = flask.request.form['birthday']
        phone = flask.request.form['phone']
        active = flask.request.form['active']
        city = flask.request.form['city_of_residence']

        try:
            cur.execute("""
                UPDATE volunteer
                SET first_name = %s,
                    last_name = %s,
                    birthday = %s,
                    phone = %s,
                    active = %s,
                    city_of_residence = %s
                WHERE volunteer_id = %s
            """, (first, last, birth, phone, active, city, volunteer_id))
            conn.commit()
        except Exception as e:
            print("❌ Update error:", e)
            conn.rollback()

    # שליפת פרטים אישיים
    cur.execute("""
        SELECT first_name, last_name, birthday, phone, active, city_of_residence
        FROM volunteer
        WHERE volunteer_id = %s
    """, (volunteer_id,))
    volunteer = cur.fetchone()

    # בדיקת תפקיד
    cur.execute("SELECT 1 FROM driver WHERE volunteer_id = %s", (volunteer_id,))
    is_driver = cur.fetchone() is not None
    cur.execute("SELECT 1 FROM transport_assistant WHERE volunteer_id = %s", (volunteer_id,))
    is_assistant = cur.fetchone() is not None

    if is_driver and is_assistant:
        role = "Driver / Assistant"
    elif is_driver:
        role = "Driver"
    elif is_assistant:
        role = "Assistant"
    else:
        role = "None"

    cur.close()
    conn.close()

    return render_template("personal_area.html",
                           volunteer_id=volunteer_id,
                           volunteer=volunteer,
                           role=role,
                           schedule=schedule)
@app.route("/volunteers", methods=["GET", "POST"])
def volunteers():
    js_alert = None
    volunteer_data = None
    role = "None"

    if request.method == "POST":
        search_id = request.form.get("search_id")
        volunteer_id = request.form.get("volunteer_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        active = request.form.get("active")
        city = request.form.get("city_of_residence")
        new_role = request.form.get("role")
        current_role = request.form.get("current_role")

        license_number = request.form.get("license_number")
        night_avail = request.form.get("night_avail")
        has_medical_training = request.form.get("has_medical_training")

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # 🔍 חיפוש מתנדב
            if search_id:
                cur.execute("""
                    SELECT first_name, last_name, birthday, phone, active, city_of_residence
                    FROM volunteer WHERE volunteer_id = %s
                """, (search_id,))
                row = cur.fetchone()

                if row:
                    cur.execute("SELECT 1 FROM driver WHERE volunteer_id = %s", (search_id,))
                    is_driver = cur.fetchone() is not None

                    cur.execute("SELECT 1 FROM transport_assistant WHERE volunteer_id = %s", (search_id,))
                    is_assistant = cur.fetchone() is not None

                    if is_driver and is_assistant:
                        role = "Driver/Assistant"
                    elif is_driver:
                        role = "Driver"
                    elif is_assistant:
                        role = "Assistant"
                    else:
                        role = "None"

                    volunteer_data = {
                        "volunteer_id": search_id,
                        "first_name": row[0],
                        "last_name": row[1],
                        "birthday": row[2].isoformat(),
                        "phone": row[3],
                        "active": row[4],
                        "city_of_residence": row[5]
                    }
                else:
                    js_alert = "Volunteer not found."

            else:
                # 🛠️ בדיקה אם המתנדב כבר קיים
                cur.execute("SELECT 1 FROM volunteer WHERE volunteer_id = %s", (volunteer_id,))
                exists = cur.fetchone()

                if exists:
                    # עדכון
                    cur.execute("""
                        UPDATE volunteer
                        SET first_name = %s,
                            last_name = %s,
                            birthday = %s,
                            phone = %s,
                            active = %s,
                            city_of_residence = %s
                        WHERE volunteer_id = %s
                    """, (first_name, last_name, birthday, phone, active, city, volunteer_id))
                else:
                    # הוספה
                    cur.execute("""
                        INSERT INTO volunteer (volunteer_id, first_name, last_name, birthday, phone, active, city_of_residence)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (volunteer_id, first_name, last_name, birthday, phone, active, city))

                # טיפול בתפקידים
                if new_role != current_role or not exists:
                    cur.execute("DELETE FROM driver WHERE volunteer_id = %s", (volunteer_id,))
                    cur.execute("DELETE FROM transport_assistant WHERE volunteer_id = %s", (volunteer_id,))

                    if new_role == "Driver":
                        cur.execute("""
                            INSERT INTO driver (volunteer_id, license_number, night_avail)
                            VALUES (%s, %s, %s)
                        """, (volunteer_id, license_number, night_avail))
                    elif new_role == "Assistant":
                        cur.execute("""
                            INSERT INTO transport_assistant (volunteer_id, has_medical_training)
                            VALUES (%s, %s)
                        """, (volunteer_id, has_medical_training))
                    elif new_role == "Driver/Assistant":
                        cur.execute("""
                            INSERT INTO driver (volunteer_id, license_number, night_avail)
                            VALUES (%s, %s, %s)
                        """, (volunteer_id, license_number, night_avail))
                        cur.execute("""
                            INSERT INTO transport_assistant (volunteer_id, has_medical_training)
                            VALUES (%s, %s)
                        """, (volunteer_id, has_medical_training))

                conn.commit()

        except Exception as e:
            conn.rollback()
            js_alert = f"Error: {str(e)}"

        finally:
            cur.close()
            conn.close()

    # שלב משותף – גם אחרי POST וגם ב־GET
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT city_of_residence FROM volunteer ORDER BY city_of_residence")
        city_of_residence = [row[0] for row in cur.fetchall()]

        active_options = ['T', 'F']

        # שליפת כל המתנדבים לטבלה
        cur.execute("""
            SELECT v.volunteer_id, v.first_name, v.last_name, v.birthday,
                   v.phone, v.active, v.city_of_residence,
                   CASE 
                       WHEN d.volunteer_id IS NOT NULL AND a.volunteer_id IS NOT NULL THEN 'Driver/Assistant'
                       WHEN d.volunteer_id IS NOT NULL THEN 'Driver'
                       WHEN a.volunteer_id IS NOT NULL THEN 'Assistant'
                       ELSE 'None'
                   END AS role
            FROM volunteer v
            LEFT JOIN driver d ON v.volunteer_id = d.volunteer_id
            LEFT JOIN transport_assistant a ON v.volunteer_id = a.volunteer_id
            ORDER BY v.volunteer_id
        """)
        volunteers = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    return render_template(
        "volunteers.html",
        volunteers=volunteers,
        volunteer_data=volunteer_data,
        city_of_residence=city_of_residence,
        active=active_options,
        role=role,
        js_alert=js_alert
    )
@app.route("/delete_volunteer", methods=["POST"])
def delete_volunteer():
    volunteer_id = request.form.get("volunteer_id")
    if not volunteer_id:
        return "<h3 style='color:red;'>Volunteer ID missing.</h3>"

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # בדיקה אם הוא נהג בנסיעה
        cur.execute("""
            SELECT volunteering_id FROM ride WHERE driver_id = %s
        """, (volunteer_id,))
        ride = cur.fetchone()

        if ride:
            # החזר תשובה בקוד 409 עם כתובת ההפניה
            return {"requires_confirmation": True,
                    "redirect_url": url_for("confirm_delete_with_ride", volunteer_id=volunteer_id,
                                            ride_id=ride[0])}, 409

        # מחיקה רגילה
        delete_volunteer_everywhere(cur, volunteer_id)
        conn.commit()

    except Exception as e:
        conn.rollback()
        return f"<h3 style='color:red;'>Error deleting volunteer: {str(e)}</h3>"
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('volunteers'))
def delete_volunteer_everywhere(cur, volunteer_id):
    cur.execute("DELETE FROM event_participation WHERE volunteer_id = %s", (volunteer_id,))
    cur.execute("DELETE FROM volunteering_participation WHERE volunteer_id = %s", (volunteer_id,))
    cur.execute("DELETE FROM driver WHERE volunteer_id = %s", (volunteer_id,))
    cur.execute("DELETE FROM transport_assistant WHERE volunteer_id = %s", (volunteer_id,))
    cur.execute("DELETE FROM volunteer WHERE volunteer_id = %s", (volunteer_id,))
@app.route("/confirm_delete_with_ride/<int:volunteer_id>/<int:ride_id>")
def confirm_delete_with_ride(volunteer_id, ride_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # שלב 1: מחיקת הנסיעה (שמחזיקה את ה־driver_id)
        cur.execute("DELETE FROM ride WHERE driver_id = %s", (volunteer_id,))

        # שלב 2: מחיקת שאר התלויות, ואז את המתנדב
        delete_volunteer_everywhere(cur, volunteer_id)

        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"<h3 style='color:red;'>Error deleting both volunteer and ride: {str(e)}</h3>"
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('volunteers'))
@app.route("/volunteer_info/<int:volunteer_id>")
def get_volunteer_info(volunteer_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT first_name, last_name, birthday, phone, active, city_of_residence
        FROM volunteer
        WHERE volunteer_id = %s
    """, (volunteer_id,))
    row = cur.fetchone()

    # נוסיף שליפת תפקיד
    cur.execute("SELECT 1 FROM driver WHERE volunteer_id = %s", (volunteer_id,))
    is_driver = cur.fetchone() is not None

    cur.execute("SELECT 1 FROM transport_assistant WHERE volunteer_id = %s", (volunteer_id,))
    is_assistant = cur.fetchone() is not None

    if is_driver and is_assistant:
        role = "Driver/Assistant"
    elif is_driver:
        role = "Driver"
    elif is_assistant:
        role = "Assistant"
    else:
        role = "None"

    conn.close()

    if row:
        return {
            "success": True,
            "volunteer": {
                "first_name": row[0],
                "last_name": row[1],
                "birthday": row[2].isoformat(),
                "phone": row[3],
                "active": row[4],
                "city_of_residence": row[5],
                "role": role
            }
        }
    else:
        return {"success": False}
@app.route("/deactivate_volunteers", methods=["POST"])
def deactivate_volunteers():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL deactivate_inactive_volunteers();")
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"<h3 style='color:red;'>❌ Failed to deactivate: {str(e)}</h3>"
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("volunteers"))
@app.route("/delete_inactive_volunteers", methods=["POST"])
def delete_inactive_volunteers():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # הגדרת תת-שאילתה פעם אחת
        delete_condition = """
            SELECT V.volunteer_id
            FROM volunteer V
            WHERE V.volunteer_id NOT IN (
                SELECT DISTINCT EP.volunteer_id
                FROM event_participation EP
                JOIN event E ON EP.event_id = E.event_id
                WHERE E.date >= (CURRENT_DATE - INTERVAL '2 years')
                UNION
                SELECT DISTINCT VP.volunteer_id
                FROM volunteering_participation VP
                JOIN volunteering VOL ON VP.volunteering_id = VOL.volunteering_id
                WHERE VOL.date >= (CURRENT_DATE - INTERVAL '2 years')
                UNION
                SELECT DISTINCT r.driver_id
                FROM ride r
                JOIN volunteering vol ON r.volunteering_id = vol.volunteering_id
                WHERE vol.date >= (CURRENT_DATE - INTERVAL '2 years')
                UNION
                SELECT DISTINCT r.assistant_id
                FROM ride r
                JOIN volunteering vol ON r.volunteering_id = vol.volunteering_id
                WHERE r.assistant_id IS NOT NULL
                AND vol.date >= (CURRENT_DATE - INTERVAL '2 years')
            )
            AND V.volunteer_id NOT IN (
                SELECT volunteer_id FROM kindOfVol WHERE volunteer_id IS NOT NULL
            )
            AND V.volunteer_id NOT IN (
                SELECT volunteer_id FROM event WHERE volunteer_id IS NOT NULL
            )
        """

        # מחיקת נסיעות של נהגים
        cur.execute(f"""
            DELETE FROM ride
            WHERE driver_id IN (
                SELECT volunteer_id FROM ({delete_condition}) AS ToDelete
                INTERSECT
                SELECT volunteer_id FROM driver
            )
        """)

        # ניתוק עוזרים
        cur.execute(f"""
            UPDATE ride
            SET assistant_id = NULL
            WHERE assistant_id IN (
                SELECT volunteer_id FROM ({delete_condition}) AS ToDelete
                INTERSECT
                SELECT volunteer_id FROM transport_assistant
            )
        """)

        # מחיקת השתתפות באירועים
        cur.execute(f"""
            DELETE FROM event_participation
            WHERE volunteer_id IN ({delete_condition})
        """)

        # מחיקת השתתפות בהתנדבות
        cur.execute(f"""
            DELETE FROM volunteering_participation
            WHERE volunteer_id IN ({delete_condition})
        """)

        # מחיקת נהגים
        cur.execute(f"""
            DELETE FROM driver
            WHERE volunteer_id IN ({delete_condition})
        """)

        # מחיקת עוזרים
        cur.execute(f"""
            DELETE FROM transport_assistant
            WHERE volunteer_id IN ({delete_condition})
        """)

        # מחיקת המתנדבים עצמם
        cur.execute(f"""
            DELETE FROM volunteer
            WHERE volunteer_id IN ({delete_condition})
        """)

        conn.commit()

    except Exception as e:
        conn.rollback()
        return f"<h3 style='color:red;'>❌ Failed to delete: {e}</h3>"
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("volunteers"))
@app.route("/volunteering", methods=["GET", "POST"])
def volunteering():
    conn = get_db_connection()
    cur = conn.cursor()

    error_message = None
    volunteering_data = None

    if request.method == "POST":
        action = request.form.get("action")

        date = request.form.get("date")
        hour = request.form.get("hour")
        location = request.form.get("location")

        if action == "search":
            if not (date and hour and location):
                error_message = "Date, hour, and location are required to search."
            else:
                cur.execute("""
                    SELECT volunteering_id, date, hour, duration, location, patient_id, type, report
                    FROM volunteering
                    WHERE date = %s AND hour = %s AND location = %s
                """, (date, hour, location))
                results = cur.fetchall()

                if len(results) == 0:
                    error_message = "No volunteering found for the given details."
                elif len(results) > 1:
                    error_message = "Multiple matches found. Please refine your search."
                else:
                    v = results[0]
                    volunteering_data = {
                        'volunteering_id': v[0],
                        'date': v[1],
                        'hour': v[2],
                        'duration': v[3],
                        'location': v[4],
                        'patient_id': v[5],
                        'type': v[6],
                        'report': v[7]
                    }

        elif action == "update":
            volunteering_id = request.form.get("volunteering_id")
            duration = request.form.get("duration")
            patient_id = request.form.get("patient_id")
            type_ = request.form.get("type")
            report = request.form.get("report")

            if not all([date, hour, duration, location, patient_id, type_]):
                error_message = "All fields are required to update or add a volunteering."
            else:
                try:
                    if volunteering_id:
                        # עדכון שורה קיימת
                        cur.execute("""
                            UPDATE volunteering
                            SET date = %s, hour = %s, duration = %s, location = %s, 
                                patient_id = %s, type = %s, report = %s
                            WHERE volunteering_id = %s
                        """, (date, hour, duration, location, patient_id, type_, report, volunteering_id))
                    else:
                        # יצירת ID חדש רק אם כל השדות תקינים
                        cur.execute("SELECT nextval('public.volunteering_volunteering_id_seq')")
                        new_id = cur.fetchone()[0]

                        # הכנסת שורה חדשה עם ID ידני
                        cur.execute("""
                            INSERT INTO volunteering (volunteering_id, date, hour, duration, location, 
                                patient_id, type, report)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (new_id, date, hour, duration, location, patient_id, type_, report))

                    conn.commit()
                    return redirect(url_for("volunteering"))

                except psycopg2.Error as e:
                    conn.rollback()
                    error_message = str(e).split("\n")[0]

        elif action == "delete":
            volunteering_id = request.form.get("volunteering_id")
            if volunteering_id:
                cur.execute("DELETE FROM ride WHERE volunteering_id = %s", (volunteering_id,))
                cur.execute("DELETE FROM volunteering_participation WHERE volunteering_id = %s", (volunteering_id,))
                cur.execute("DELETE FROM volunteering WHERE volunteering_id = %s", (volunteering_id,))
                conn.commit()

    # הצגת הטבלה
    cur.execute("""
        SELECT volunteering_id, date, hour, duration, location, patient_id, type, report
        FROM volunteering
        ORDER BY volunteering_id
    """)
    volunteering_raw = cur.fetchall()

    volunteering = []
    for v in volunteering_raw:
        volunteering_id = v[0]
        cur.execute("SELECT 1 FROM ride WHERE volunteering_id = %s", (volunteering_id,))
        has_ride = cur.fetchone() is not None
        volunteering.append(v + (has_ride,))

    cur.execute("SELECT name FROM city ORDER BY name")
    city_ids = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT patient_id FROM patient ORDER BY patient_id")
    patient_ids = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT type FROM KindOfVol ORDER BY type")
    kindOfVol_ids = [r[0] for r in cur.fetchall()]

    conn.close()
    return render_template("volunteering.html",
                           volunteering=volunteering,
                           volunteering_data=volunteering_data,
                           city_ids=city_ids,
                           patient_ids=patient_ids,
                           kindOfVol_ids=kindOfVol_ids,
                           error_message=error_message)
@app.route("/rides", methods=["GET", "POST"])
def rides():
    conn = get_db_connection()
    cur = conn.cursor()

    js_alert = None
    ride_data = None
    available_drivers = []
    available_vehicles = []
    available_assistants = []
    selected_destination = None

    # רשימת כל היעדים להצגה בטופס
    cur.execute(
        "SELECT destination_name, destination_address, destination_city FROM destination ORDER BY destination_name")
    destinations = cur.fetchall()

    if request.method == "POST":
        action = request.form.get("action")
        pickup_time = request.form.get("pickup_time")
        destination_val = request.form.get("destination")
        selected_destination = destination_val
        driver_id = request.form.get("driver_id")
        vehicle_id = request.form.get("vehicle_id")
        assistant_id = request.form.get("assistant_id") or None

        try:
            dest_name, dest_address, dest_city = destination_val.split("|", 2)
        except Exception:
            dest_name = dest_address = dest_city = ""

        if action == "search":
            cur.execute("""
                SELECT volunteering_id, pickup_time, destination_name, destination_address,
                       vehicle_id, driver_id, assistant_id
                FROM ride
                WHERE pickup_time = %s
                  AND destination_name = %s
                  AND destination_address = %s
                  AND driver_id = %s
            """, (pickup_time, dest_name, dest_address, driver_id))
            result = cur.fetchone()

            if result:
                ride_data = {
                    'volunteering_id': result[0],
                    'pickup_time': result[1],
                    'destination_name': result[2],
                    'destination_address': result[3],
                    'vehicle_id': result[4],
                    'driver_id': result[5],
                    'assistant_id': result[6]
                }

                # שליפת תאריך ההתנדבות
                cur.execute("SELECT date, duration FROM volunteering WHERE volunteering_id = %s",
                            (ride_data['volunteering_id'],))
                vol_info = cur.fetchone()
                if vol_info:
                    vol_date, vol_duration = vol_info

                    # נהגים זמינים + הנהג הנוכחי
                    cur.execute("""
                        SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
                        FROM driver d
                        JOIN volunteer v ON d.volunteer_id = v.volunteer_id
                        WHERE v.volunteer_id NOT IN (
                            SELECT r.driver_id
                            FROM ride r
                            JOIN volunteering vol USING (volunteering_id)
                            WHERE vol.date = %s
                              AND (
                                  %s::time < r.pickup_time + (vol.duration * INTERVAL '1 minute')
                                  AND r.pickup_time < %s::time + (%s * INTERVAL '1 minute')
                              )
                        )
                        UNION
                        SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
                        FROM volunteer v
                        WHERE v.volunteer_id = %s
                        ORDER BY volunteer_id
                    """, (vol_date, pickup_time, pickup_time, vol_duration, ride_data['driver_id']))
                    available_drivers = cur.fetchall()

                    # רכבים זמינים + הרכב הנוכחי
                    cur.execute("""
                        SELECT vehicle_id, license_plate, type, capacity
                        FROM vehicle
                        WHERE vehicle_id NOT IN (
                            SELECT r.vehicle_id
                            FROM ride r
                            JOIN volunteering vol USING (volunteering_id)
                            WHERE vol.date = %s
                              AND (
                                  %s::time < r.pickup_time + (vol.duration * INTERVAL '1 minute')
                                  AND r.pickup_time < %s::time + (%s * INTERVAL '1 minute')
                              )
                        )
                        UNION
                        SELECT vehicle_id, license_plate, type, capacity
                        FROM vehicle
                        WHERE vehicle_id = %s
                        ORDER BY vehicle_id
                    """, (vol_date, pickup_time, pickup_time, vol_duration, ride_data['vehicle_id']))
                    available_vehicles = cur.fetchall()

                    # עוזרים זמינים + העוזר הנוכחי
                    cur.execute("""
                        SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
                        FROM transport_assistant ta
                        JOIN volunteer v ON ta.volunteer_id = v.volunteer_id
                        WHERE NOT EXISTS (
                            SELECT 1
                            FROM ride r
                            JOIN volunteering vol ON r.volunteering_id = vol.volunteering_id
                            WHERE vol.date = %s
                              AND r.assistant_id = v.volunteer_id
                              AND (
                                  %s::time < r.pickup_time + (vol.duration * INTERVAL '1 minute')
                                  AND r.pickup_time < %s::time + (%s * INTERVAL '1 minute')
                              )
                              AND r.volunteering_id != %s
                        )
                        UNION
                        SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
                        FROM volunteer v
                        WHERE v.volunteer_id = %s
                        ORDER BY volunteer_id
                    """, (
                        vol_date,
                        pickup_time,
                        pickup_time,
                        vol_duration,
                        ride_data['volunteering_id'],
                        ride_data['assistant_id']
                    ))
                    available_assistants = cur.fetchall()

        elif action == "update":
            volunteering_id = request.form.get("volunteering_id")
            js_alert = None
            try:
                cur.execute("""
                    UPDATE ride
                    SET pickup_time = %s,
                        destination_name = %s,
                        destination_address = %s,
                        driver_id = %s,
                        vehicle_id = %s,
                        assistant_id = %s
                    WHERE volunteering_id = %s
                """, (
                    pickup_time,
                    dest_name,
                    dest_address,
                    driver_id,
                    vehicle_id,
                    assistant_id,
                    volunteering_id
                ))
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                # ניקח רק את השורה הראשונה של השגיאה
                js_alert = str(e).splitlines()[0]
        elif action == "delete":
            volunteering_id = request.form.get("volunteering_id")
            try:
                cur.execute("DELETE FROM ride WHERE volunteering_id = %s", (volunteering_id,))
                conn.commit()
                js_alert = "Ride deleted successfully."
                ride_data = None  # מנקה את הנתונים אחרי מחיקה
            except psycopg2.Error as e:
                conn.rollback()
                js_alert = "❌ Delete failed: " + str(e).split("\n")[0]

    if not ride_data:
        cur.execute("""
            SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
            FROM driver d
            JOIN volunteer v ON d.volunteer_id = v.volunteer_id
            ORDER BY v.volunteer_id
        """)
        available_drivers = cur.fetchall()

    cur.execute("""
        SELECT volunteering_id, pickup_time, destination_name, destination_address,
               vehicle_id, driver_id, assistant_id
        FROM ride
        ORDER BY volunteering_id
    """)
    rides = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("rides.html",
                           rides=rides,
                           destinations=destinations,
                           ride_data=ride_data,
                           selected_destination=selected_destination,
                           available_drivers=available_drivers,
                           available_vehicles=available_vehicles,
                           available_assistants=available_assistants,
                           js_alert=js_alert)
@app.route("/assign_assistants", methods=["POST"])
def assign_assistants():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL assign_assistants_to_future_rides();")
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"<h3 style='color:red;'>❌ Failed to assign: {str(e)}</h3>"
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("rides"))
@app.route("/ride/<int:volunteering_id>")
def view_ride(volunteering_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # נסיעה
    cur.execute("""
        SELECT pickup_time, destination_name, destination_address,
               vehicle_id, driver_id, assistant_id
        FROM ride
        WHERE volunteering_id = %s
    """, (volunteering_id,))
    ride = cur.fetchone()

    if not ride:
        cur.close()
        conn.close()
        return f"<h3>No ride found for volunteering ID {volunteering_id}</h3>"

    # נהג
    driver = None
    cur.execute("SELECT volunteer_id, first_name, last_name, phone FROM volunteer WHERE volunteer_id = %s", (ride[4],))
    driver = cur.fetchone()

    # עוזר
    assistant = None
    if ride[5]:
        cur.execute("SELECT volunteer_id, first_name, last_name, phone FROM volunteer WHERE volunteer_id = %s",
                    (ride[5],))
        assistant = cur.fetchone()

    # רכב
    vehicle = None
    if ride[3]:
        cur.execute("SELECT vehicle_id, license_plate, type, capacity FROM vehicle WHERE vehicle_id = %s", (ride[3],))
        vehicle = cur.fetchone()

    # מתנדבים בהתנדבות
    cur.execute("""
        SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
        FROM volunteering_participation vp
        JOIN volunteer v ON vp.volunteer_id = v.volunteer_id
        WHERE vp.volunteering_id = %s
    """, (volunteering_id,))
    participants = cur.fetchall()

    # פרטי ההתנדבות עצמה
    cur.execute("""
        SELECT volunteering_id, date, hour, location,patient_id
        FROM volunteering
        WHERE volunteering_id = %s
    """, (volunteering_id,))
    volunteering_details = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("ride_details.html",
                           ride=ride,
                           driver=driver,
                           assistant=assistant,
                           vehicle=vehicle,
                           participants=participants,
                           volunteering_details=volunteering_details)
@app.route("/add_ride/<int:volunteering_id>", methods=["GET", "POST"])
def add_ride(volunteering_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # שליפת פרטי ההתנדבות
    cur.execute("""
        SELECT date, hour, location, duration
        FROM volunteering
        WHERE volunteering_id = %s
    """, (volunteering_id,))
    volunteering_info = cur.fetchone()
    if volunteering_info is None:
        cur.close()
        conn.close()
        return f"<h3 style='color:red;'>No volunteering found with ID {volunteering_id}.</h3>"

    cur.execute("SELECT destination_name, destination_address, destination_city FROM destination")
    destinations = cur.fetchall()

    pickup_time = request.form.get("pickup_time")
    selected_destination = request.form.get("destination")
    selected_driver_id = request.form.get("selected_driver_id")
    selected_vehicle_id = request.form.get("selected_vehicle_id")

    # המרה ל-int עם טיפול בשגיאות
    try:
        selected_driver_id = int(selected_driver_id) if selected_driver_id else None
    except ValueError:
        selected_driver_id = None

    try:
        selected_vehicle_id = int(selected_vehicle_id) if selected_vehicle_id else None
    except ValueError:
        selected_vehicle_id = None

    available_drivers = []
    available_vehicles = []
    available_assistants = []

    volunteering_date = volunteering_info[0]
    volunteering_duration = volunteering_info[3]

    action = request.form.get("form_action")

    if action == "search_staff":
        # נבדוק ש-picked_destination לא ריק לפני הפרדה
        try:
            dest_name, dest_address, city_name = selected_destination.split("|", 2)
        except Exception:
            dest_name = dest_address = city_name = ""

        if pickup_time:
            cur.execute("""
                SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
                FROM driver d
                JOIN volunteer v ON d.volunteer_id = v.volunteer_id
                WHERE v.volunteer_id NOT IN (
                    SELECT r.driver_id
                    FROM ride r
                    JOIN volunteering vol USING (volunteering_id)
                    WHERE vol.date = %s
                    AND (
                        %s::time < r.pickup_time + (vol.duration * INTERVAL '1 minute')
                        AND r.pickup_time < %s::time + (%s * INTERVAL '1 minute')
                    )
                )
                ORDER BY v.volunteer_id
            """, (volunteering_date, pickup_time, pickup_time, volunteering_duration))
            available_drivers = cur.fetchall()

            cur.execute("""
                SELECT vehicle_id, license_plate, type, capacity
                FROM vehicle
                WHERE vehicle_id NOT IN (
                    SELECT r.vehicle_id
                    FROM ride r
                    JOIN volunteering vol USING (volunteering_id)
                    WHERE vol.date = %s
                    AND (
                        %s::time < r.pickup_time + (vol.duration * INTERVAL '1 minute')
                        AND r.pickup_time < %s::time + (%s * INTERVAL '1 minute')
                    )
                )
                ORDER BY vehicle_id
            """, (volunteering_date, pickup_time, pickup_time, volunteering_duration))
            available_vehicles = cur.fetchall()

    elif action == "add_assistant":
        try:
            dest_name, dest_address, city_name = selected_destination.split("|", 2)
        except Exception:
            dest_name = dest_address = city_name = ""

        if pickup_time and selected_driver_id:
            cur.execute("""
                SELECT v.volunteer_id, v.first_name, v.last_name, v.phone
                FROM transport_assistant ta
                JOIN volunteer v ON ta.volunteer_id = v.volunteer_id
                WHERE v.volunteer_id != %s
                  AND NOT EXISTS (
                    SELECT 1
                    FROM ride r
                    JOIN volunteering vol USING (volunteering_id)
                    WHERE vol.date = %s
                      AND r.assistant_id = v.volunteer_id
                      AND (
                        %s::time < r.pickup_time + (vol.duration * INTERVAL '1 minute')
                        AND r.pickup_time < %s::time + (%s * INTERVAL '1 minute')
                      )
                  )
                ORDER BY v.volunteer_id
            """, (selected_driver_id, volunteering_date, pickup_time, pickup_time, volunteering_duration))
            available_assistants = cur.fetchall()
        else:
            print("⚠️ Missing pickup_time or driver selection")

    cur.close()
    conn.close()

    return render_template("add_ride.html",
                           volunteering_id=volunteering_id,
                           volunteering_info=volunteering_info,
                           destinations=destinations,
                           pickup_time=pickup_time,
                           selected_destination=selected_destination,
                           drivers=available_drivers,
                           vehicles=available_vehicles,
                           assistants=available_assistants,
                           selected_driver_id=selected_driver_id,
                           selected_vehicle_id=selected_vehicle_id)
@app.route('/confirm_ride/<int:volunteering_id>', methods=["POST"])
def confirm_ride(volunteering_id):
    try:
        pickup_time = request.form.get("pickup_time")
        driver_id = request.form.get("driver_id") or request.form.get("selected_driver_id")
        vehicle_id = request.form.get("vehicle_id") or request.form.get("selected_vehicle_id")
        destination = request.form.get("destination")
        assistant_id = request.form.get("assistant_id")  # יכול להיות None

        if not all([pickup_time, driver_id, vehicle_id, destination]):
            return "Missing required fields", 400

        dest_name, dest_address, _ = destination.split('|')

        conn = get_db_connection()
        cur = conn.cursor()

        if assistant_id:
            cur.execute("""
                INSERT INTO ride (volunteering_id, pickup_time, destination_name, destination_address, driver_id, vehicle_id, assistant_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                volunteering_id,
                pickup_time,
                dest_name,
                dest_address,
                int(driver_id),
                int(vehicle_id),
                int(assistant_id)
            ))
        else:
            cur.execute("""
                INSERT INTO ride (volunteering_id, pickup_time, destination_name, destination_address, driver_id, vehicle_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                volunteering_id,
                pickup_time,
                dest_name,
                dest_address,
                int(driver_id),
                int(vehicle_id)
            ))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('view_ride', volunteering_id=volunteering_id))

    except Exception as e:
        print("Error confirming ride:", e)
        return "An error occurred while confirming the ride."
@app.route("/volunteers_of_volunteering/<int:volunteering_id>", methods=["GET", "POST"])
def volunteers_of_volunteering(volunteering_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # שליפת פרטי ההתנדבות
    cur.execute("""
        SELECT v.date, v.hour, v.location, v.duration,
               p.first_name, p.last_name, v.type
        FROM volunteering v
        JOIN patient p ON v.patient_id = p.patient_id
        WHERE v.volunteering_id = %s
    """, (volunteering_id,))
    volunteering_info = cur.fetchone()

    # בדיקת קיום נסיעה
    cur.execute("SELECT COUNT(*) FROM ride WHERE volunteering_id = %s", (volunteering_id,))
    has_ride = cur.fetchone()[0] > 0

    # טיפול בפעולות POST
    if request.method == "POST":
        form_action = request.form.get("form_action")

        # הוספת מתנדב
        if form_action == "add_volunteer":
            volunteer_id = request.form.get("volunteer_id")
            shift = request.form.get("shift")
            if volunteer_id and shift:
                try:
                    cur.execute("""
                        INSERT INTO volunteering_participation (volunteering_id, volunteer_id, shift)
                        VALUES (%s, %s, %s)
                    """, (volunteering_id, volunteer_id, shift))
                    conn.commit()
                except Exception as e:
                    print("❌ Error adding volunteer:", e)

        # מחיקת מתנדב
        elif form_action == "delete_volunteer":
            volunteer_id = request.form.get("volunteer_id")
            if volunteer_id:
                try:
                    cur.execute("""
                        DELETE FROM volunteering_participation
                        WHERE volunteering_id = %s AND volunteer_id = %s
                    """, (volunteering_id, volunteer_id))
                    conn.commit()
                except Exception as e:
                    print("❌ Error deleting volunteer:", e)

        # עדכון משמרת לקטינים
        elif request.form.get("update_shift_for_minors") == "1":
            cur.execute("""
                UPDATE volunteering_participation vp
                SET shift = 'M'
                FROM volunteer v
                WHERE vp.volunteer_id = v.volunteer_id
                  AND EXTRACT(YEAR FROM AGE(CURRENT_DATE, v.birthday)) < 18
                  AND vp.volunteering_id = %s
            """, (volunteering_id,))
            conn.commit()

    # שליפת מתנדבים רשומים להתנדבות
    cur.execute("""
        SELECT vp.volunteer_id, v.first_name, v.last_name, v.phone,
               EXTRACT(YEAR FROM AGE(CURRENT_DATE, v.birthday)) AS age, vp.shift
        FROM volunteering_participation vp
        JOIN volunteer v ON vp.volunteer_id = v.volunteer_id
        WHERE vp.volunteering_id = %s
        ORDER BY vp.shift, v.last_name
    """, (volunteering_id,))
    volunteers = cur.fetchall()

    # שליפת מתנדבים שעדיין לא רשומים להתנדבות
    cur.execute("""
        SELECT volunteer_id
        FROM volunteer
        WHERE volunteer_id NOT IN (
            SELECT volunteer_id
            FROM volunteering_participation
            WHERE volunteering_id = %s
        )
        ORDER BY volunteer_id
    """, (volunteering_id,))
    volunteers_ids = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return render_template("volunteers_of_volunteering.html",
                           volunteering_id=volunteering_id,
                           volunteering_info={
                               "date": volunteering_info[0],
                               "hour": volunteering_info[1],
                               "location": volunteering_info[2],
                               "duration": volunteering_info[3],
                               "patient_name": f"{volunteering_info[4]} {volunteering_info[5]}",
                               "type": volunteering_info[6]
                           },
                           has_ride=has_ride,
                           volunteers=volunteers,
                           volunteers_ids=volunteers_ids)
if __name__ == "__main__":
    app.run(debug=True)
