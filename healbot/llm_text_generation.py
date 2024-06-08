import requests
from time import sleep

from healbot.data_models import ModelPayload, ModelResponse


# TODO: move to config file
project_id = "d3724316f161-4d3e-ba20-5bf617b83967"
authorization_token = f"d3724316f161-4d3e-ba20-5bf617b83967:sk-YWE1MTQxOWYtN2Y2Yi00OGE4LTkxYWEtNWU2NTJmOTdjOTQw"
region = "f1db6c"
base_url = f"https://api-{region}.stack.tryrelevance.com/latest"
headers = {
    "Authorization": authorization_token,
}


def get_agent_response(agent_id: str, prompt: str) -> str:
    """
    Get text response from Relevance.ai agent.
    """

    # start conversation with agent
    trigger_response = requests.post(
        base_url + "/agents/trigger",
        headers=headers,
        json={"message": {"role": "user", "content": prompt}, "agent_id": agent_id},
    )

    job = trigger_response.json()

    conversation_id = job["conversation_id"]

    role = None

    while not role == "agent":
        sleep(1)
        print("Waiting for agent message")

        # Send the POST request
        response = requests.post(
            base_url + "/knowledge/list",
            headers=headers,
            json={
                "knowledge_set": conversation_id,
                "filters": [],
                "sort": [{"insert_date_": "desc"}],
            },
        )

        conversation_messages = response.json()["results"]

        message = conversation_messages[0]["data"]["message"]

        role = message["role"]
        content = message["content"]

    return content


def generate_recovery_plan_info(model_pload: dict, agent_id: str) -> ModelResponse:
    """
    Generate information for a new daily recovery plan.
    """

    pload = ModelPayload(**model_pload)

    # # must format with payload accordingly
    # prompt = "..."

    # # get agent response
    # response = get_agent_response(agent_id, prompt)

    print("USING MOCK DATA FOR RESPONSE")

    # parse response
    ...

    # MOCK DATA:

    response = {
        "rehab_plan_message": "You seen to be doing better, I increased the reps of the exercises. Keep it up!",
        "rehab_plan_exercises": [
            # list of exercises from the previous day, in the JSON format you use
        ],
        "rehab_advice": "Make sure to take your medication on time and get enough rest.",
        "motivational_message": "You're doing great! Keep up the good work!",
        "biomarkers_summary_message": "Your sleep duration is good, but try to increase your activity levels.",
    }

    return ModelResponse(**response)


if __name__ == "__main__":

    # testing

    agent_id = "a4dcef11-857a-48aa-ba91-95a3df092226"
    prompt = "Hello! I hurt my left brain"

    ans = get_agent_response(agent_id, prompt)
    print(ans)
