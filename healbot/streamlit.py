import streamlit as st
from typing import Optional
from pydantic import BaseModel
import random
import json

from healbot.llm_text_generation import generate_recovery_plan_info, ModelPayload
from healbot.data_models import PatientBiomarkers, PatientCheckup, PreviousDayFeedback
from healbot.database import (
    create_connection,
    create_table,
    enter_data_into_database,
    retrieve_most_recent_data,
)

# Importing external functions (assuming they are defined in another module)
# from external_module import generate_recovery_plan_info, ModelPayload, PatientBiomarkers

DAY_COUNT = 1
PATIENT_ID = "pat-001"
AGENT_ID = "a4dcef11-857a-48aa-ba91-95a3df092226"

db_file = "data.db"

SURGERY_TYPE = "Knee Surgery"
SURGERY_NAME = "ACL Reconstruction and Meniscus Repair"
SURGERY_DATE = "2024-06-08"


class PatientCheckup(BaseModel):
    current_mental_wellness: int  # score from 1 to 10
    current_physical_wellness: int  # score from 1 to 10
    current_pain_level: int  # score from 1 to 10
    other_feedback: Optional[str] = None


class PreviousDayFeedback(BaseModel):
    previous_day_exercise_rating: int  # score from 1 to 10
    previous_day_exercises: dict
    other_feedback: Optional[str] = None


# Function to load the main interface
def load_interface(steps, sleep_length, cal_burn, rehab_plan, motivation_quote):

    # load data from database

    conn = create_connection(db_file)

    # Retrieve the most recent data from the database
    recovery_plan_info = retrieve_most_recent_data(conn, PATIENT_ID)

    col1, col2, col3 = st.columns([1, 2, 1])

    # Column 1 for fitness data
    with col1:
        st.header("🏃Fitness Data")
        # Display metrics with emojis as icons
        st.metric(label="👟 Steps taken", value=f"{steps} steps")
        st.metric(label="🌙 Sleep duration", value=f"{sleep_length} hours")
        st.metric(label="🔥 Calories burned", value=f"{cal_burn} calories")

    # Column 2 for injury rehab plan
    with col2:
        st.header("🩹Injury Rehab Plan")
        st.write(rehab_plan)

    # Column 3 for motivational quotes
    with col3:
        st.header("💪Motivation for the Day")
        st.write(motivation_quote)

    # Add "End Day" button at the bottom
    if st.button("End Day"):
        st.session_state.page = "feedback"
        st.experimental_rerun()


# Function to load the feedback page
def feedback_page():
    st.header("Good Morning! Let's start your day with a checkup.")

    st.subheader("How are you feeling today?")
    current_mental_wellness = st.slider("Current Mental Wellness", 1, 10, 5)
    current_physical_wellness = st.slider("Current Physical Wellness", 1, 10, 5)
    current_pain_level = st.slider("Current Pain Level", 1, 10, 5)
    other_feedback_patient = st.text_area("Other Feedback for Patient Checkup:")

    st.subheader("How did you feel yesterday during the exercises?")
    previous_day_exercise_rating = st.slider("Previous Day Exercise Rating", 1, 10, 5)
    previous_day_exercises = {
        "Exercise 1": st.number_input(
            "Exercise 1 Reps", min_value=0, max_value=100, value=10
        ),
        "Exercise 2": st.number_input(
            "Exercise 2 Reps", min_value=0, max_value=100, value=10
        ),
        # Add more exercises as needed
    }
    other_feedback_previous_day = st.text_area("Other Feedback for Yesterday:")

    if st.button("Submit Feedback"):
        patient_checkup = PatientCheckup(
            current_mental_wellness=current_mental_wellness,
            current_physical_wellness=current_physical_wellness,
            current_pain_level=current_pain_level,
            other_feedback=other_feedback_patient,
        )

        previous_day_feedback = PreviousDayFeedback(
            previous_day_exercise_rating=previous_day_exercise_rating,
            previous_day_exercises=previous_day_exercises,
            other_feedback=other_feedback_previous_day,
        )

        global DAY_COUNT
        DAY_COUNT += 1

        model_payload = ModelPayload(
            surgery_type=SURGERY_TYPE,
            surgery_name=SURGERY_NAME,
            surgery_date=SURGERY_DATE,
            days_since_surgery=DAY_COUNT,
            biomarkers=PatientBiomarkers(
                previous_day_activity_steps=5000,
                previous_day_activity_energy_burned=200.5,
                sleep_in_bed_duration=8.0,
            ),
            bod_checkup=patient_checkup.model_dump(),
            previous_day_feedback=previous_day_feedback.model_dump(),
        )

        # Create a connection to the database
        conn = create_connection(db_file)

        # Create the table
        create_table(conn)

        # Add data to the table
        enter_data_into_database(conn, patient_id=PATIENT_ID, daily_info=model_payload)

        st.session_state.page = "main"
        st.success("Thank you for your feedback! Recovery plan generated.")
        # st.write(recovery_plan_info)  # Display the generated recovery plan info
        st.experimental_rerun()


if __name__ == "__main__":
    # Initialize session state if not already done
    if "page" not in st.session_state:
        st.session_state.page = "main"

    # Assuming these variables are fetched or computed elsewhere in your code
    steps = random.randint(2000, 10000)  # Realistic range for daily steps
    sleep_length = round(
        random.uniform(6.0, 9.0), 1
    )  # Realistic range for sleep in hours
    cal_burn = random.randint(1800, 3500)  # Realistic calorie burn range for a day

    rehab_plan = """
    ### Day 1: Gentle Range of Motion
    - Focus on slowly moving the injured joint through the full range of motion.
    - Do three sets of ten repetitions, twice a day.
    """

    motivation_quote = (
        "“It does not matter how slowly you go as long as you do not stop.” – Confucius"
    )

    # Load the appropriate page based on the session state
    if st.session_state.page == "main":
        load_interface(steps, sleep_length, cal_burn, rehab_plan, motivation_quote)
    elif st.session_state.page == "feedback":
        feedback_page()
