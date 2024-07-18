import streamlit as st
import requests
from typing import Optional


#-----------------------------------------------UI--------------------------------------------------------#

st.title("Causal AI Chat Bot")

# Information to Access
st.sidebar.header("Information to Access")
access_token = st.sidebar.text_input("Access Token")
project_id = st.sidebar.text_input("Project ID")

model = st.sidebar.selectbox("Model", ["Llama 3 70b", "Llama 3 8b", "GPT 4o", "GPT 3.5-turbo"])

# Setups
st.sidebar.header("Setups")
uploaded_file = st.sidebar.file_uploader("Choose a file for analyse... [Optional]", 
                                         type=["json"],
                                         help="Limit 1MB per file • json")

# Select for conversation
st.sidebar.header("Select for conversation")

target_value = st.sidebar.selectbox("Target Value... [Optional]", ["Option 1", "Option 2"],index=None,
                                 placeholder="Select a target value...")

feature_explaintion = st.text_area("Explain your csv file or features here (Not required)", "Type something") #Store it to database

if model == "Llama 3 70b":
    model_name = "llama3:70b"
elif model == "Llama 3 8b":
    model_name = "llama3:8b"
elif model == "GPT 4o":
    model_name = "gpt-4o"
else:
    model_name = "gpt-3.5-turbo"

#---------------------------------------------------------------------------------------------------------#


BASE_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "ad96b5e1-9bc3-4f42-a9dc-b3277e38c13e"
ENDPOINT = ""

TWEAKS = {
    "ChatOutput-e9Kry": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": ""
    },
    #Use your domain knowledge to detail interpretation user's questions, Don't just look the document. If user didn't ask you to you interpret, just don't output it.____ + "The target feature is "+ target + "\n""
    "ParseData-AOZWl": {
        "sep": "\n",
        "template": "This is explaintion\n" + feature_explaintion + "\n" +"{text}\n Please reed the explaintion and take look at \"x\",\"y\",\"imp\",\"co\". For every json object, please mention the object that imp(importance) value not equals to 0, means x is a cause of y. If \"co\" value smaller than 0 and imp(importance) value not equals to 0, that means the bigger x will make smaller y. If \"co\" value bigger than 0 and imp(importance) value not equals to 0, that means the bigger x will make bigger y.\n" +  "Please just anwser user's question, don't output the text if user didn't ask you to interpret the data.",
    },
    "File-QG5F0": {
        "path": "C:/Users/Moofon/桌面/Vizuro_Intern/causalAi_chatBot/output.json",#Here to change the file
        "silent_errors": False
    },
    "ChatInput-HLsyc": {
        "files": "",
        "input_value": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": ""
    },
    "CombineText-eUm9F": {
        "delimiter": "",
        "text1": "",
        "text2": ""
    },
    "Prompt-vK3e9": {
        "context": "",
        "template": "{context}\n\nUser: {user_message}\nAI: ",
        "user_message": ""
    },
    "OllamaModel-6HNmK": {
    "base_url": "http://localhost:11434",
    "format": "",
    "input_value": "",
    "metadata": {},
    "mirostat": "Disabled",
    "mirostat_eta": None,
    "mirostat_tau": None,
    "model": "llama3:70b",
    "num_ctx": None,
    "num_gpu": None,
    "num_thread": None,
    "repeat_last_n": None,
    "repeat_penalty": None,
    "stop_tokens": "",
    "stream": False,
    "system": "",
    "system_message": "",
    "tags": "",
    "temperature": 0.1,
    "template": "",
    "tfs_z": None,
    "timeout": None,
    "top_k": None,
    "top_p": None,
    "verbose": True
    }
}

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
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
    formatted_message = ""
    for line in lines:
        formatted_message += line.strip() + "\n"
    return formatted_message

# Streamlit UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("Ask me about the causal graph"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        endpoint = ENDPOINT or FLOW_ID
        tweaks = TWEAKS
        api_key = None
        output_type = "chat"
        input_type = "chat"

        try:
            response = run_flow(
            message=prompt,
            endpoint=endpoint,
            output_type=output_type,
            input_type=input_type,
            tweaks=tweaks,
            api_key=api_key
            )
    
            if 'outputs' not in response:
                st.error(f"Unexpected API response structure. Response: {response}")
            else:
                try:
                    main_message = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                    formatted_response = format_message(main_message)
                    st.markdown(formatted_response)
                    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                except KeyError as ke:
                    st.error(f"Error accessing response data: {ke}. Full response: {response}")
        except Exception as e:
            st.error(f"An error occurred while calling the API: {e}")

if __name__ == "__main__":
    pass