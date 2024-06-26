from pydantic import BaseModel, Field
from typing import List, Optional
import uuid


class PatientDetails(BaseModel):
    patient_id: str = Field(default_factory=lambda: "pat-" + str(uuid.uuid4()))
    patient_name: Optional[str] = None
    patient_age: Optional[int] = None


class PatientBiomarkers(BaseModel):
    previous_day_activity_steps: int  # in steps
    previous_day_activity_energy_burned: float  # in calories
    sleep_in_bed_duration: float  # in hours


class PatientCheckup(BaseModel):
    current_mental_wellness: Optional[int] = None  # score from 1 to 10
    current_physical_wellness: Optional[int] = None  # score from 1 to 10
    current_pain_level: Optional[int] = None  # score from 1 to 10
    other_feedback: Optional[str] = None


class PreviousDayFeedback(BaseModel):
    previous_day_exercise_rating: Optional[int] = None  # score from 1 to 10
    previous_day_exercises: Optional[dict] = None
    other_feedback: Optional[str] = None


class DailyPatientInfo(BaseModel):
    day_number: int
    bod_checkup: PatientCheckup
    biomarkers: PatientBiomarkers
    previous_day_feedback: PreviousDayFeedback


class ModelPayload(BaseModel):
    surgery_type: str
    surgery_name: str
    surgery_date: str
    days_since_surgery: int
    biomarkers: PatientBiomarkers
    bod_checkup: Optional[PatientCheckup] = None  # from day 2 onwards
    previous_day_feedback: Optional[PreviousDayFeedback] = None  # from day 2 onwards


# EXAMPLE:
# {
#     "rehab_plan_message": "You seen to be doing better, I increased the reps of the exercises. Keep it up!",
#     "rehab_plan_exercises": [
#         // list of exercises from the previous day, in the JSON format you use
#     ],
#     "rehab_advice": "Make sure to take your medication on time and get enough rest.",
#     "motivational_message": "You're doing great! Keep up the good work!",
#     "biomarkers_summary_message": "Your sleep duration is good, but try to increase your activity levels.",
# }
