import sqlite3
from healbot.data_models import ModelPayload, ModelResponse
from healbot.data_models import PatientBiomarkers, PatientCheckup, PreviousDayFeedback


# Create connection to SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return conn


# Create table if it doesn't exist
def create_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patient_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT NOT NULL,
        surgery_type TEXT,
        surgery_name TEXT,
        surgery_date TEXT,
        days_since_surgery INTEGER,
        previous_day_activity_steps INTEGER,
        previous_day_activity_energy_burned REAL,
        sleep_in_bed_duration REAL,
        current_mental_wellness INTEGER,
        current_physical_wellness INTEGER,
        current_pain_level INTEGER,
        previous_day_exercise_rating INTEGER
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")


# Function to insert data into the table
def enter_data_into_database(conn, patient_id: str, daily_info: ModelPayload) -> None:
    data = {
        "patient_id": patient_id,
        "surgery_type": daily_info.surgery_type,
        "surgery_name": daily_info.surgery_name,
        "surgery_date": daily_info.surgery_date,
        "days_since_surgery": daily_info.days_since_surgery,
        "previous_day_activity_steps": daily_info.biomarkers.previous_day_activity_steps,
        "previous_day_activity_energy_burned": daily_info.biomarkers.previous_day_activity_energy_burned,
        "sleep_in_bed_duration": daily_info.biomarkers.sleep_in_bed_duration,
        "current_mental_wellness": daily_info.bod_checkup.current_mental_wellness,
        "current_physical_wellness": daily_info.bod_checkup.current_physical_wellness,
        "current_pain_level": daily_info.bod_checkup.current_pain_level,
        "previous_day_exercise_rating": daily_info.previous_day_feedback.previous_day_exercise_rating,
    }

    placeholders = ", ".join("?" * len(data))
    columns = ", ".join(data.keys())
    sql = f"INSERT INTO patient_data ({columns}) VALUES ({placeholders})"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(data.values()))
        conn.commit()
        print("Data added successfully")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")


# list all data from table
def list_all_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_data")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Example usage
if __name__ == "__main__":
    # Define the database file
    db_file = "test_database.db"

    # Create a connection to the database
    conn = create_connection(db_file)

    # Create the table
    create_table(conn)

    # Example data
    biomarkers = PatientBiomarkers(
        previous_day_activity_steps=5000,
        previous_day_activity_energy_burned=200.5,
        sleep_in_bed_duration=8.0,
    )
    bod_checkup = PatientCheckup(
        current_mental_wellness=8,
        current_physical_wellness=7,
        current_pain_level=3,
    )
    previous_day_feedback = PreviousDayFeedback(
        previous_day_exercise_rating=9,
        previous_day_exercises={"exercise_1": "push-ups", "exercise_2": "sit-ups"},
    )
    daily_info = ModelPayload(
        surgery_type="Type A",
        surgery_name="Appendectomy",
        surgery_date="2024-01-01",
        days_since_surgery=10,
        biomarkers=biomarkers,
        bod_checkup=bod_checkup,
        previous_day_feedback=previous_day_feedback,
    )

    # Add data to the table
    enter_data_into_database(conn, "patient_001", daily_info)

    # print the data in the table
    list_all_data(conn)

    # Close the connection
    if conn:
        conn.close()
        print("The connection is closed")
