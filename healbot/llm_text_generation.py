import json
import requests
import time
from time import sleep

from data_models import ModelPayload
from utils import clean_json
from config import project_id, authorization_token, region, base_url, headers  # Import configuration




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
    content = None
    start_time = time.time()  # Record the start time

    while not role == "agent" or content is None:
        if time.time() - start_time > 20:  # Check if 10 seconds have passed
            print("Timeout: No response from agent within 20 seconds.")
            return "No response within timeout period."
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

        # import pdb

        # pdb.set_trace()

        conversation_messages = response.json()["results"]

        message = conversation_messages[0]["data"]["message"]

        role = message.get("role")
        content = message.get("content")

    return content


def generate_recovery_plan_info(model_pload: dict, agent_id: str) -> dict:
    """
    Generate information for a new daily recovery plan.
    """

    # print(f"RECEIVED MODEL PAYLOAD:\n{json.dumps(model_pload, indent=2)}")

    # data validation
    payload = ModelPayload(**model_pload).model_dump()

    prompt = json.dumps(payload, indent=2)

    output_str = get_agent_response(agent_id, prompt)

    output_json = clean_json(output_str)

    return output_json


if __name__ == "__main__":

    # testing

    # agent_id = "a4dcef11-857a-48aa-ba91-95a3df092226"
    # prompt = "Hello! I hurt my left brain"

    # ans = get_agent_response(agent_id, prompt)
    # print(ans)

    model_pload = {
        "surgery_type": "Brain Surgery",
        "surgery_name": "Left Brain Surgery",
        "surgery_date": "2022-01-01",
        "days_since_surgery": 5,
        "biomarkers": {
            "previous_day_activity_steps": 5000,
            "previous_day_activity_energy_burned": 200.5,
            "sleep_in_bed_duration": 8.0,
        },
        "bod_checkup": {
            "current_mental_wellness": 8,
            "current_physical_wellness": 7,
            "current_pain_level": 3,
        },
        "previous_day_feedback": None,
    }

    agent_id = "a4dcef11-857a-48aa-ba91-95a3df092226"

    # response = generate_recovery_plan_info(model_pload, agent_id)

    response = generate_recovery_plan_info(model_pload, agent_id)

    print(response)
