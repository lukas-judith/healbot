from typing import List, Dict


class DayInfo:
    def __init__(self):

        self.data_summary = None
        self.motivational_message = None
        self.exercises = None

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
            out += f"Exercises:\n{self.exercises}\n"

        return out


class DailyProgression:

    def __init__(self, training_plan: str):
        self.day_idx = 0
        self.days = self.get_days_from_initial_training_plan(training_plan)

    def get_days_from_initial_training_plan(self, training_plan: str) -> List[DayInfo]:
        days = []
        for day in training_plan.split("## Day")[1:]:
            day_info = DayInfo()
            day_lines = day.strip().split("\n")
            day_info.data_summary = day_lines[0].strip()
            day_info.motivational_message = day_lines[1].strip()
            for line in day_lines[2:]:
                if line.strip():
                    day_info.exercises.append(line.strip())
            days.append(day_info)
        return days

    def progress_to_next_day(self):

        # set current day to finished
        self.days[self.day_idx].is_finished = True

        # increment day index
        self.day_idx += 1

        # set new day to is_today
        self.days[self.day_idx].is_today = True
