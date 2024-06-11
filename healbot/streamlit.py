import streamlit as st
from typing import Optional
from pydantic import BaseModel
import random
import json

from llm_text_generation import generate_recovery_plan_info, ModelPayload
from data_models import PatientBiomarkers, PatientCheckup, PreviousDayFeedback
from database import (
    create_connection,
    create_table,
    enter_data_into_database,
    retrieve_most_recent_data,
)

# Importing external functions (assuming they are defined in another module)
# from external_module import generate_recovery_plan_info, ModelPayload, PatientBiomarkers

AGENT_ID = "a4dcef11-857a-48aa-ba91-95a3df092226"


class PatientCheckup(BaseModel):
    current_mental_wellness: Optional[int] = None  # score from 1 to 10
    current_physical_wellness: Optional[int] = None  # score from 1 to 10
    current_pain_level: Optional[int] = None  # score from 1 to 10
    other_feedback: Optional[str] = None


class PreviousDayFeedback(BaseModel):
    previous_day_exercise_rating: Optional[int] = None  # score from 1 to 10
    previous_day_exercises: Optional[dict] = None
    other_feedback: Optional[str] = None


# Function to load the main interface
def load_interface():

    # Custom CSS to inject into the Streamlit interface for styling
    st.markdown(
        """
        <style>
        # .stMarkdown { background: #f0f2f6; }
        # .st-emotion-cache-1r4qj8v { background: #0794FF !important;
        # }
        .st-emotion-cache-1kyxreq {
        justify-content: center !important;
        }
        .block-container st-emotion-cache-13ln4jf ea3mdgi5 { background-color: #0794FF !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # TODO: REMOVE RANDOM DATA (Update with live data from SahhaAi)
    previous_day_activity_steps = random.randint(2000, 10000)
    previous_day_activity_energy_burned = round(random.uniform(1800, 3500), 1)
    sleep_in_bed_duration = round(random.uniform(6.0, 9.0), 1)

    bod_checkup = PatientCheckup(
        current_mental_wellness=st.session_state.current_mental_wellness,
        current_physical_wellness=st.session_state.current_physical_wellness,
        current_pain_level=st.session_state.current_pain_level,
    )

    biomarkers = PatientBiomarkers(
        previous_day_activity_steps=previous_day_activity_steps,
        previous_day_activity_energy_burned=previous_day_activity_energy_burned,
        sleep_in_bed_duration=sleep_in_bed_duration,
    )

    previous_day_feedback = PreviousDayFeedback(
        previous_day_exercise_rating=st.session_state.previous_day_exercise_rating,
        previous_day_exercises=st.session_state.previous_day_exercises,
    )

    pload = ModelPayload(
        surgery_type=st.session_state.surgery_type,
        surgery_name=st.session_state.surgery_name,
        surgery_date=st.session_state.surgery_date,
        days_since_surgery=st.session_state.day_count,
        biomarkers=biomarkers.model_dump(),
        bod_checkup=bod_checkup.model_dump(),
        previous_day_feedback=previous_day_feedback.model_dump(),
    )

    if st.session_state.generate_new_data:
        st.session_state.generate_new_data = False
        if not st.session_state.interface_loaded:
            print(
                f"UPDATING USING PAYLOAD \n{json.dumps(pload.model_dump(), indent=2)}"
            )
            recovery_plan = generate_recovery_plan_info(pload.model_dump(), AGENT_ID)
            st.session_state.interface_loaded = True
        else:
            recovery_plan = {}
    else:
        recovery_plan = {}

    # Ensure recovery_plan is a dictionary
    recovery_plan = recovery_plan if isinstance(recovery_plan, dict) else {}

    rehab_plan_message = recovery_plan.get("rehab-plan-message")
    rehab_plan_exercises = recovery_plan.get("rehab-plan-exercise")
    rehab_advice = recovery_plan.get("rehab-advice")
    motivation_quote = recovery_plan.get("motivational-quote")
  
  

    # remember exercises for next day
    if rehab_plan_exercises is not None and len(rehab_plan_exercises) > 0:
        print("REMEMBERING EXERCISES FOR NEXT DAY")
        st.session_state.previous_day_exercises = rehab_plan_exercises

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

    rehab_plan_exercises_str = ""

    if recovery_plan:
        for exercise, items in rehab_plan_exercises.items():
            rehab_plan_exercises_str += f"""
    **{exercise}**:
    - {items['reason']}
    - {items['description']}
    - number of sets: {items['number of sets']}
    - number of reps: {items['number of reps']}
    """

    # Column 2 for injury rehab plan
    with col2:
        st.header("🩹Injury Rehab Plan")
        st.write(f"Day #{st.session_state.day_count} since surgery")
        st.write(rehab_plan_message)
        st.write(rehab_plan_exercises_str)
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
    other_feedback_previous_day = st.text_area("Other Feedback for Yesterday:")

    if st.button("Submit Feedback"):
        st.session_state.current_mental_wellness = current_mental_wellness
        st.session_state.current_physical_wellness = current_physical_wellness
        st.session_state.current_pain_level = current_pain_level
        st.session_state.other_feedback_patient = other_feedback_patient

        st.session_state.previous_day_exercise_rating = previous_day_exercise_rating
        st.session_state.other_feedback_previous_day = other_feedback_previous_day

        st.session_state.day_count += 1
        st.session_state.page = "main"
        st.success("Thank you for your feedback! Recovery plan will be generated.")
        st.rerun()

from PIL import Image
# import streamlit as st

def surgery_info_page():
    logo_path = r"C:\Users\jorge\OneDrive\Documents\Work\RehabWise\healbot\healbot\logo.png"
    logo = Image.open(logo_path)

    # Custom CSS to center all HTML elements
    st.markdown(
        """
        <style>
        .css-1d391kg { text-align: center; }
        /* Additional custom CSS */
        # .stMarkdown { background: #f0f2f6; }
        # .st-emotion-cache-1r4qj8v { background: #0794FF !important;
        # }
        .st-emotion-cache-1h7x1t2 {
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .st-emotion-cache-1kyxreq {
        justify-content: center !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create columns for layout
    col1, col2, col3 = st.columns([1, 3, 1])

    # Display the logo in the middle column with a specific width
    with col1:
        st.image(logo, width=200)  # Adjust width as needed
    # st.image(logo, caption='Logo')

    with col2:
        st.header("Welcome to RehabWise!")
        st.subheader("Enter Surgery Information")

    # flag for generating a new recovery plan
    st.session_state.generate_new_data = False

    st.session_state.current_mental_wellness = None
    st.session_state.current_physical_wellness = None
    st.session_state.current_pain_level = None
    st.session_state.other_feedback_patient = None

    st.session_state.previous_day_exercise_rating = None
    st.session_state.other_feedback_previous_day = None

    if not "previous_day_exercises" in st.session_state:
        print("INIT EXERCISES")
        st.session_state.previous_day_exercises = {}

    surgery_type = st.text_input(
        "Surgery Type", "Knee Surgery"
    )
    surgery_name = st.text_input(
        "Surgery Name", "ACL Reconstruction and Meniscus Repair"
    )
    surgery_date = st.text_input("Surgery Date", "2024-06-08")

    # Set what day to start on
    st.session_state.day_count = 200
    st.session_state.patient_id = "pat-001"

    if st.button("Submit Surgery Info"):
        st.session_state.surgery_type = surgery_type
        st.session_state.surgery_name = surgery_name
        st.session_state.surgery_date = surgery_date

        st.session_state.page = "main"
        st.rerun()

def landing_page():
    st.title("Welcome to HealBot!")
    st.write("Your companion for post-surgery recovery.")
    # Set the page configuration

    # Custom CSS to center the content
    st.markdown(
        """
        <style>
        .st-emotion-cache-1v0mbdj {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .enter-button {
            justify-content: center;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: flex;
            font-size: 16px;
            margin-top: 20px;
            cursor: pointer;
            border: none;
            border-radius: 5px;
        }
        .enter-button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # # Centered content
    # st.markdown('<div class="centered-content">', unsafe_allow_html=True)

    # Display the logo
    logo_path = r"C:\Users\jorge\OneDrive\Documents\Work\RehabWise\healbot\healbot\logo.png"
    logo = Image.open(logo_path)
    st.image(logo, caption="RehabWise", use_column_width=True)

    # Display the button
    if  st.button("Enter", key="enter", help="Click to enter the application", use_container_width=True):
        st.write("Welcome to RehabWise!")
        st.session_state.page = "surgery_info"
        st.experimental_rerun()

    # st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "RehabWise"

    if "day_count" not in st.session_state:
        st.session_state.day_count = 200

    if "interface_loaded" not in st.session_state:
        st.session_state.interface_loaded = False

    if st.session_state.page == "RehabWise":
        landing_page()
    elif st.session_state.page == "surgery_info":
        surgery_info_page()
    elif st.session_state.page == "main":
        st.session_state.generate_new_data = True
        load_interface()
    elif st.session_state.page == "feedback":
        feedback_page()
    
