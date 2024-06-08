import re
import json


def clean_json(input_str):
    # Use regex to find the JSON content within the input string
    match = re.search(r"\{.*\}", input_str, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            # Parse the cleaned JSON string to ensure it's valid
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print("No valid JSON found")
        return None


if __name__ == "__main__":
    input_str = """
```json
{
  "rehab-plan-message": "You're doing great! Let's continue to build on your progress.",
  "rehab-plan-exercise": {
    "Deep Breathing Exercises": {
      "reason": "To improve oxygen flow to the brain and promote relaxation.",
      "description": "Sit or lie down in a comfortable position. Inhale deeply through your nose, hold for a few seconds, and then exhale slowly through your mouth. Repeat.",
      "number of sets": 3,
      "number of reps": 10
    },
    "Neck Stretches": {
      "reason": "To relieve tension and improve blood circulation to the brain.",
      "description": "Gently tilt your head towards your shoulder and hold for 15-20 seconds. Repeat on the other side.",
      "number of sets": 3,
      "number of reps": 5
    },
    "Seated Marching": {
      "reason": "To improve blood circulation and maintain lower body strength.",
      "description": "While seated, lift your knees alternately as if you are marching. Keep your back straight and engage your core.",
      "number of sets": 3,
      "number of reps": 15
    }
  },
  "rehab-advice": "Continue to monitor your pain levels and mental wellness. Ensure you are getting adequate rest and hydration. Avoid any strenuous activities and follow your doctor's advice.",
  "motivational-quote": "The journey of a thousand miles begins with one step. - Lao Tzu"
}
```
    """
    json_data = clean_json(input_str)
    assert isinstance(json_data, dict), "JSON data should be a dictionary"
    print(json_data)
