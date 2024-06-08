from pydantic import BaseModel
from typing import List, Optional


class PatientBiomarkers(BaseModel):
    previous_day_activity_steps: int  # in steps
    previous_day_activity_energy_burned: float  # in calories
    sleep_in_bed_duration: float  # in hours


class PatientCheckup(BaseModel):
    current_mental_wellness: int  # score from 1 to 10
    current_physical_wellness: int  # score from 1 to 10
    current_pain_level: int  # score from 1 to 10
    other_feedback: Optional[str] = None


class PreviousDayFeedback(BaseModel):
    previous_day_exercise_rating: int  # score from 1 to 10
    previous_day_exercises: dict
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
    bod_checkup: PatientCheckup = None  # from day 2 onwards
    previous_day_feedback: PreviousDayFeedback = None  # from day 2 onwards
