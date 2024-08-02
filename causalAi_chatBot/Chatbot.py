import streamlit as st
import requests
from typing import Optional
import json
import os
from dotenv import load_dotenv


def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None,
             session_id: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
        "session_id": session_id,
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


def remove_json_object(json_data):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    if not isinstance(json_data, dict) or 'edges' not in json_data:
        st.error("Project does not exsist")
        return None

    edges = json_data['edges']
    updated_edges = []

    for edge in edges:
        if isinstance(edge, dict):
            updated_edge = {
                "x": edge.get('x', ''),
                "y": edge.get('y', ''),
                "imp": round(edge.get('imp', 0), 2),
                "co": round(edge.get('co', 0), 2) if edge.get('co') is not None else None
            }
            if updated_edge['imp'] != 0:
                updated_edges.append(updated_edge)

    return updated_edges


def try_upload_json(file_content,email,project_id):
    save_dir = f"json_file_storage/{email}"
    file_content = remove_json_object(file_content)  # filter out json objects

    if file_content is None:
        if os.path.exists(current_dir + "/json_file_storage" + f"/{email}/{project_id}.json"):
            os.remove(current_dir + "/json_file_storage" + f"/{email}/{project_id}.json")
        return None
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    saved_file_path = os.path.join(save_dir, f"{project_id}.json")

    with open(saved_file_path, 'w') as file:
        json.dump(file_content, file, indent=2, ensure_ascii=False)

    # except json.JSONDecodeError:
    #     st.error("Invalid JSON file. Please upload a valid JSON file.")
    #     # if os.path.exists(current_dir + "/json_file_storage" + f"/{email}/{project_id}.json"):
    #     #     os.remove(current_dir + "/json_file_storage" + f"/{email}/{project_id}.json")


def model_select(model):
    if model == "Llama 3 70b":
        model_name = "llama3:70b"
        model_type = "llama"
    elif model == "Llama 3 8b":
        model_name = "llama3:latest"
        model_type = "llama"
    elif model == "GPT 4o":
        model_name = "gpt-4o"
        model_type = "openai"
    elif model == "GPT 3.5-turbo":
        model_name = "gpt-3.5-turbo"
        model_type = "openai"
    return model_name, model_type


def delete_session(session_id):

    url = f"http://127.0.0.1:7860/api/v1/monitor/messages/session/{session_id}"


    response = requests.delete(url)

    if response.status_code != 204:
        print(f"Failed to clear session messages: {response.status_code} - {response.text}")


def request_login(email, password):
    url = "http://192.168.50.3:25000/api/v1/user/login"
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        token = response.json()
        return token['access_token']
    except:
        st.error("Wrong email or password")
        return None


def request_json(email, password, project_id):
    url = f"http://192.168.50.3:25000/api/v1/dataset_groups/{project_id}/causal_graph/edges"
    access_token = request_login(email, password)
    if access_token is None:
        return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    content = response.json()
    try_upload_json(content,email,project_id)
    
    
    





load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))


# -----------------------------------------------UI--------------------------------------------------------#

st.title("Causal AI Chat Bot")

feature_explaintion = st.text_area("Explain your csv file or features here (Not required)", placeholder="Type something")  # Can Store it to database

st.sidebar.header("Information to Access")

email = st.sidebar.text_input("Email", placeholder="Email")
password = st.sidebar.text_input("Password", placeholder="Password")
project_id = st.sidebar.text_input("Project ID", placeholder="Project ID")
sessionID = f"{email}-{project_id}"

if st.sidebar.button("Upload Json File", use_container_width=True):
    request_json(email, password, project_id)
    

if os.path.exists(current_dir + "/json_file_storage" + f"/{email}/{project_id}.json"):
    save_dir = current_dir + "/json_file_storage" + f"/{email}/{project_id}.json"
    st.success("File uploaded and processed successfully!")
else:
    st.error("Please upload the json file first")
    

st.sidebar.header("Select for conversation")

model = st.sidebar.selectbox("Model", ["Llama 3 70b", "Llama 3 8b", "GPT 4o", "GPT 3.5-turbo"])
model_name, model_type = model_select(model)

sidebar = st.sidebar.container()
col1, col2 = sidebar.columns(2)




with col1:
    if st.button("Clear Dialogue", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("New Chat", type="primary", use_container_width=True):
        delete_session(sessionID)
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask me about the causal graph")

# ----------------------------------------Langflow----------------------------------------------------------#
BASE_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "b40bf1e6-686d-4bb9-96b4-4e766face139"
ENDPOINT = ""
TWEAKS = {
    "ChatOutput-XKzcM": {
        "data_template": "{text}",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": sessionID
    },
    "ParseData-nc2eq": {
        "sep": "\n",
        "template": "This is the explaintion\n" + feature_explaintion + "\n" + "{text}\n Please read the explaintion and take look at \"x\",\"y\",\"imp\",\"co\". For every json object, x and y means two factors that x is a cause of y. The bigger imp(importance) value means x and y have strongger causation. If \"co\" value smaller than 0, that means the bigger x will make smaller y. If \"co\" value bigger than 0, that means the bigger x will make bigger y.\n" + "Anwser user's question base on the flie but use your domain knowledge to interpret and anwser user's question.\n" + " Don't mention about how you found the anwser like Based on the provided JSON objects.\n",
    },
    "File-QXhLH": {
        "path": current_dir + "/json_file_storage" + f"/{email}/{project_id}.json",
        "silent_errors": False
    },
    "ChatInput-zhi0V": {
        "files": "",
        "sender": "User",
        "sender_name": "User",
        "session_id": sessionID
    },
    "CombineText-pJHHM": {
        "delimiter": "",
        "text1": "",
        "text2": ""
    },
    "Prompt-nKfg6": {
        "context": "Use your domain knowledge to anwser User's question below. But output base on provided data. Don't confuse co value with imp value.",
        "template": "{context}\n\nUser: {user_message}\nAI: ",
        "user_message": ""
    },
    
    "CombineText-IGgKp": {
        "delimiter": " ",
        "text1": "",
        "text2": ""
    },
    "Memory-kITEr": {
        "n_messages": 8,
        "order": "Ascending",
        "sender": "Machine and User",
        "sender_name": "User",
        "session_id": sessionID,
        "template": "{sender_name}: {text}"
    },
    "Prompt-lWzlq": {
        "context": "",
        "template": "{context}\n\nUser: {user_message}\nAI: ",
        "user_message": ""
    }
}


if model_type == "llama":
    TWEAKS.pop("OpenAIModel-OWsv2", None)
    TWEAKS.pop("OllamaModel-0W5Bx", None)
    TWEAKS["OllamaModel-0W5Bx"] = {
        "base_url": "http://localhost:11434",
        "format": "",
        "metadata": {},
        "mirostat": "Disabled",
        "mirostat_eta": None,
        "mirostat_tau": None,
        "model": model_name,
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
        "temperature": 0,
        "template": "",
        "tfs_z": None,
        "timeout": None,
        "top_k": None,
        "top_p": None,
        "verbose": True
    }
else:
    TWEAKS.pop("OpenAIModel-OWsv2", None)
    TWEAKS.pop("OllamaModel-0W5Bx", None)
    TWEAKS["OpenAIModel-OWsv2"] = {
        "json_mode": False,
        "max_tokens": None,
        "model_kwargs": {},
        "model_name": model_name,
        "openai_api_base": "",
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0
    }



# -----------------------------------------------------------------------------------------------------------#

if prompt:
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
                api_key=api_key,
                session_id=sessionID,
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