import json
import requests
import warnings
from typing import Optional

try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "7e8a8e37-d2f0-47b4-8e33-a1730acdf001"
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
    "Prompt-0QWFL": {},
    "ChatOutput-jQUEF": {},
    "OpenAIModel-9HkXN": {},
    "ParseData-llizB": {},
    "File-tVaOh": {},
    "TextInput-MiiWE": {},
    "OpenAIModel-ylUFZ": {},
    "ChatInput-FcnMU": {},
    "CombineText-8PtjA": {}
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def format_message(message: str):
    lines = message.split('\n')
    for line in lines:
        print(line.strip())

def main():

    message = "Please explain the relationship between these factors in detail, including why it causes classification, reason and how to improve it."
    endpoint = ENDPOINT or FLOW_ID
    tweaks = TWEAKS
    api_key = None
    output_type = "chat"
    input_type = "chat"
    upload_file_path = None
    components = None

    if upload_file_path:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=upload_file_path, host=BASE_API_URL, flow_id=ENDPOINT, components=components, tweaks=tweaks)

    response = run_flow(
        message=message,
        endpoint=endpoint,
        output_type=output_type,
        input_type=input_type,
        tweaks=tweaks,
        api_key=api_key
    )


    main_message = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    format_message(main_message)

if __name__ == "__main__":
    main()
