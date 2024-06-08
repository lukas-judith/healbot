import streamlit as st
from typing import List


class DayInfo:
    def __init__(self):
        self.data_summary = None
        self.motivational_message = None
        self.exercises = []
        self.is_finished = False
        self.is_today = False
        self.feedback = None

    def update_data_summary(
        self,
        data_summary: str = None,
        motivational_message: str = None,
        exercises: List[str] = None,
    ):
        self.data_summary = data_summary
        self.motivational_message = motivational_message
        self.exercises = exercises

    def finish_day(self, feedback: str):
        self.is_finished = True
        self.feedback = feedback

    def __str__(self) -> str:
        out = ""

        if self.data_summary:
            out += f"Data Summary:\n{self.data_summary}\n"

        if self.motivational_message:
            out += f"Motivational Message:\n{self.motivational_message}\n"

        if self.exercises:
            out += "Exercises:\n"
            out += "\n".join(self.exercises) + "\n"

        if self.is_today:
            out += "\nStatus: Today\n"
        elif self.is_finished:
            out += "\nStatus: Finished\n"
        else:
            out += "\nStatus: Not Today\n"

        return out


class DailyProgression:
    def __init__(self, training_plan: str):
        self.day_idx = 0
        self.days = self.get_days_from_initial_training_plan(training_plan)
        if self.days:
            self.days[0].is_today = True

    def get_days_from_initial_training_plan(self, training_plan: str) -> List[DayInfo]:
        days = []
        for day in training_plan.split("## Day")[1:]:
            day_info = DayInfo()
            day_lines = day.strip().split("\n")
            day_info.data_summary = day_lines[0].strip() if day_lines else None
            day_info.motivational_message = (
                day_lines[1].strip() if len(day_lines) > 1 else None
            )
            day_info.exercises = [line.strip() for line in day_lines[2:]]
            days.append(day_info)
        return days

    def progress_to_next_day(self):
        if self.day_idx < len(self.days) - 1:
            self.days[self.day_idx].is_finished = True
            self.days[self.day_idx].is_today = False
            self.day_idx += 1
            self.days[self.day_idx].is_today = True


def generate_initial_training_plan(description, date):
    # Mock function to generate a training plan
    training_plan = f"""
    ## Day 1
    Light stretching
    Keep a positive mindset
    - Stretch arms
    - Stretch legs

    ## Day 2
    Walking
    Steady progress is key
    - Walk 20 minutes
    - Breathe deeply

    ## Day 3
    Strength training
    Focus on your goals
    - Push-ups
    - Squats

    ## Day 4
    Yoga
    Balance and calm
    - Sun salutation
    - Tree pose

    ## Day 5
    Swimming
    Smooth and steady
    - Swim 20 minutes

    ## Day 6
    Rest day
    Recovery is important
    - Relax and hydrate

    ## Day 7
    Light jogging
    Consistency is crucial
    - Jog 20 minutes
    """
    return training_plan


def welcome_page():
    st.header("Welcome")
    description = st.text_input("Description of injury:")
    date = st.date_input("Date of injury:")

    if st.button("Generate Training Plan"):
        st.session_state.training_plan = generate_initial_training_plan(
            description, date
        )
        st.session_state.progression = DailyProgression(st.session_state.training_plan)
        st.session_state.page = "training_plan"
        st.experimental_rerun()


def training_plan_page():
    st.header("Training Plan")
    progression = st.session_state.progression
    for idx, day in enumerate(progression.days):
        day_title = f"Day {idx + 1}" + (
            " (Today)" if day.is_today else " (Completed)" if day.is_finished else ""
        )
        with st.expander(day_title):
            st.markdown(str(day))
            if day.is_today and not day.is_finished:
                feedback = st.text_area(f"Feedback for Day {idx + 1}")
                if st.button(f"Finish Day {idx + 1}"):
                    day.finish_day(feedback)
                    progression.progress_to_next_day()
                    st.experimental_rerun()

    if st.button("Back to Welcome Page"):
        st.session_state.page = "welcome"
        st.experimental_rerun()


def main():
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "training_plan":
        training_plan_page()


if __name__ == "__main__":
    main()
