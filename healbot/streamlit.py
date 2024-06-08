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

AGENT_ID = "a4dcef11-857a-48aa-ba91-95a3df092226"


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
def load_interface():
    previous_day_activity_steps = random.randint(2000, 10000)
    previous_day_activity_energy_burned = round(random.uniform(1800, 3500), 1)
    sleep_in_bed_duration = round(random.uniform(6.0, 9.0), 1)

    pload = ModelPayload(
        surgery_type=st.session_state.surgery_type,
        surgery_name=st.session_state.surgery_name,
        surgery_date=st.session_state.surgery_date,
        days_since_surgery=st.session_state.day_count,
        biomarkers=PatientBiomarkers(
            previous_day_activity_steps=previous_day_activity_steps,
            previous_day_activity_energy_burned=previous_day_activity_energy_burned,
            sleep_in_bed_duration=sleep_in_bed_duration,
        ),
        bod_checkup=None,
        previous_day_feedback=None,
    )

    if st.session_state.generate_new_data:
        st.session_state.generate_new_data = False
        if not st.session_state.interface_loaded:
            recovery_plan = generate_recovery_plan_info(pload.model_dump(), AGENT_ID)
            # Place the resource-intensive function here
            st.session_state.interface_loaded = True
        else:
            recovery_plan = {}
    else:
        recovery_plan = {}

    rehab_plan_message = recovery_plan.get("rehab-plan-message")
    rehab_plan_exercises = recovery_plan.get("rehab-plan-exercise")
    rehab_advice = recovery_plan.get("rehab-advice")
    motivation_quote = recovery_plan.get("motivational-quote")

    col1, col2, col3 = st.columns([1, 2, 1])

    # Column 1 for fitness data
    with col1:
        st.header("🏃Fitness Data")
        st.metric(label="👟 Steps taken", value=f"{previous_day_activity_steps} steps")
        st.metric(label="🌙 Sleep duration", value=f"{sleep_in_bed_duration} hours")
        st.metric(
            label="🔥 Calories burned",
            value=f"{previous_day_activity_energy_burned} calories",
        )

    # Column 2 for injury rehab plan
    with col2:
        st.header("🩹Injury Rehab Plan")
        st.write(f"Day #{st.session_state.day_count} since surgery")
        st.write(rehab_plan_message)
        st.write(rehab_plan_exercises)
        st.write(rehab_advice)

    # Column 3 for motivational quotes
    with col3:
        st.header("💪Motivation for the Day")
        st.write(motivation_quote)

    # Add "End Day" button at the bottom
    if st.button("End Day"):
        st.session_state.page = "feedback"
        st.session_state.interface_loaded = (
            False  # Reset flag when navigating to feedback
        )
        st.rerun()


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
        st.session_state.current_mental_wellness = current_mental_wellness
        st.session_state.current_physical_wellness = current_physical_wellness
        st.session_state.current_pain_level = current_pain_level
        st.session_state.other_feedback_patient = other_feedback_patient

        st.session_state.previous_day_exercise_rating = previous_day_exercise_rating
        st.session_state.previous_day_exercises = previous_day_exercises
        st.session_state.other_feedback_previous_day = other_feedback_previous_day

        st.session_state.day_count += 1
        st.session_state.page = "main"
        st.success("Thank you for your feedback! Recovery plan will be generated.")
        st.rerun()


def surgery_info_page():
    st.header("Enter Surgery Information")

    # flag for generating a new recovery plan
    st.session_state.generate_new_data = False

    surgery_type = st.text_input("Surgery Type", "Knee Surgery")
    surgery_name = st.text_input(
        "Surgery Name", "ACL Reconstruction and Meniscus Repair"
    )
    surgery_date = st.text_input("Surgery Date", "2024-06-08")

    st.session_state.day_count = 1
    st.session_state.patient_id = "pat-001"

    if st.button("Submit Surgery Info"):
        st.session_state.surgery_type = surgery_type
        st.session_state.surgery_name = surgery_name
        st.session_state.surgery_date = surgery_date

        st.session_state.page = "main"
        st.rerun()


if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "surgery_info"

    if "day_count" not in st.session_state:
        st.session_state.day_count = 1

    if "interface_loaded" not in st.session_state:
        st.session_state.interface_loaded = False

    if st.session_state.page == "surgery_info":
        surgery_info_page()
    elif st.session_state.page == "main":
        st.session_state.generate_new_data = True
        load_interface()
    elif st.session_state.page == "feedback":
        feedback_page()
