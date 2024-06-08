import streamlit as st


def generate_initial_training_plan(description, date):
    # Mock function to generate a training plan
    training_plan = f"""
    ## Day 1
    - Exercise: Light stretching
    - Duration: 10 minutes
    - Note: Start slow and easy.

    ## Day 2
    - Exercise: Walking
    - Duration: 20 minutes
    - Note: Keep a steady pace.

    ## Day 3
    - Exercise: Strength training
    - Duration: 30 minutes
    - Note: Focus on form.

    ## Day 4
    - Exercise: Yoga
    - Duration: 15 minutes
    - Note: Breathe deeply.

    ## Day 5
    - Exercise: Swimming
    - Duration: 20 minutes
    - Note: Keep it gentle.

    ## Day 6
    - Exercise: Rest day
    - Duration: N/A
    - Note: Recover and relax.

    ## Day 7
    - Exercise: Light jogging
    - Duration: 20 minutes
    - Note: Keep a moderate pace.
    """
    return training_plan


def main():
    st.title("Injury Recovery App")

    st.header("Welcome")
    description = st.text_input("Description of injury:")
    date = st.date_input("Date of injury:")

    if "training_plan" not in st.session_state:
        st.session_state.training_plan = ""

    if st.button("Generate Training Plan"):
        st.session_state.training_plan = generate_initial_training_plan(
            description, date
        )

    if st.session_state.training_plan:
        st.header("Training Plan")
        plan_days = st.session_state.training_plan.split("## Day")
        for day in plan_days[1:]:  # Skip the first empty element
            day_title = "## Day" + day.split("\n")[0]
            day_content = "\n".join(day.split("\n")[1:])
            with st.expander(day_title.strip()):
                st.markdown(day_content.strip())


if __name__ == "__main__":
    main()
