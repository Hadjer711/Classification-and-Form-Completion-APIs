import requests
import json

base_url = "http://localhost:8000"

def test_streaming_post(endpoint: str, payload: dict):
    print(f"--- Testing {endpoint} ---")
    try:
        response = requests.post(f"{base_url}{endpoint}", json=payload, stream=True)

        print("Status code:", response.status_code)
        if response.status_code != 200:
            print("Non-200 response received.")
            print(response.text)
            return

        print("Streamed chunks:")
        for line in response.iter_lines():
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                    parsed = json.loads(decoded_line)
                    print(parsed)
                except Exception as e:
                    print("Failed to parse line:", decoded_line)
                    print("Error:", e)
    except Exception as e:
        print("Request failed:", e)


def test_post(endpoint: str, payload: dict):
    """
    Sends a POST request to the specified endpoint with the given payload
    and prints the parsed JSON response.

    Args:
        endpoint (str): The API endpoint to test (e.g., "/classify_prob").
        payload (dict): The JSON payload to send in the POST request.
    """
    print(f"--- Testing {endpoint} ---")
    try:
        response = requests.post(f"{base_url}{endpoint}", json=payload)

        print("Status code:", response.status_code)

        if response.status_code != 200:
            print("Non-200 response received.")
            print("Response text:", response.text)
            return

        try:
            response_json = response.json()
            print("Response JSON:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("Failed to decode JSON response.")
            print("Raw response text:", response.text)

    except Exception as e:
        print("Request failed:", e)

# Payload for /classify
classify_payload = {
    "text": "I am calling because I have a problem with my internet connection",
    "themes": [
        {
            "title": "Technical support",
            "description": "The customer is calling for technical support"
        },
        {
            "title": "Billing",
            "description": "The customer is calling for billing issues"
        },
        {
            "title": "Refund",
            "description": "The customer is calling for a refund"
        }
    ]
}

# Payload for /form_completion
form_payload = {
    "text": """Agent: Good morning! Thank you for reaching out. I’ll need to collect some basic details to assist you better. Could you please provide your first and last name?
Customer: Sure! My name is John Doe.
Agent: Thank you, John. May I also ask for your gender?
Customer: I'd prefer not to share that at the moment.
Agent: No problem at all. Now, for contact purposes, could you share your email address?
Customer: Yes, my email is johndoe@example.com.
Agent: Great! Do you have a phone number where we can reach you?
Customer: I’d rather not provide that right now.
Agent: That’s completely fine. How would you prefer us to contact you—by email or phone?
Customer: Please contact me via Email.
Agent: Understood! Lastly, can you share the reason for your call today?
Customer: I’m not ready to specify that just yet.
Agent: That’s okay, John! I’ve noted everything down. If you need any further assistance, feel free to reach out. Have a great day!"""
}

# Run tests
test_streaming_post("/classify", classify_payload)
print("\n")
test_streaming_post("/form_completion", form_payload)
print("\n")
test_post("/classify_prob", classify_payload)