import requests
from time import sleep


# TODO: move to config file
project_id = "d3724316f161-4d3e-ba20-5bf617b83967"  # Can be found in the API Keys page
authorization_token = f"d3724316f161-4d3e-ba20-5bf617b83967:sk-YWE1MTQxOWYtN2Y2Yi00OGE4LTkxYWEtNWU2NTJmOTdjOTQw"  # Both values can be found in the API Keys page
region = "f1db6c"  # Can be found in the API Keys page
base_url = f"https://api-{region}.stack.tryrelevance.com/latest"
headers = {
    "Authorization": authorization_token,
}


def get_agent_response(agent_id: str, prompt: str) -> str:
    """
    Get response from Relevance.ai agent.
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


if __name__ == "__main__":

    # testing

    agent_id = "a4dcef11-857a-48aa-ba91-95a3df092226"
    prompt = "Hello! I hurt my left brain"

    ans = get_agent_response(agent_id, prompt)
    print(ans)
