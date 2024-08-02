import streamlit as st
import requests
from typing import Optional
import json
import os
from dotenv import load_dotenv
from langflow.components.helpers.Memory import MemoryComponent

def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None,
             session_id: Optional[str] = None) -> dict:
    
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

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


def model_select(model):
    if model == "Llama3 8b":
        model_name = "llama3:latest"
        model_type = "llama"
    elif model == "GPT 4o":
        model_name = "gpt-4o"
        model_type = "openai"
    elif model == "GPT 4o mini":
        model_name = "gpt-4o-mini"
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
    

def load_session(session_id):
    # Create an instance of the MemoryComponent
    memory_component = MemoryComponent()

    # Set the necessary inputs
    memory_component.sender = "Machine and User"
    memory_component.session_id = session_id
    memory_component.n_messages = 100
    memory_component.order = "Ascending"
    memory_component.template = "{sender_name}: {text}"


    st.session_state.messages = []

    # Retrieve messages
    messages = memory_component.retrieve_messages()

    for message in messages:
        # Determine the role based on the sender
        role = "user" if message.sender == "User" else "assistant"
        
        # Append the message to session state
        st.session_state.messages.append({
            "role": role,
            "content": message.text,
        })




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

if st.sidebar.button("Upload", use_container_width=True):
    request_json(email, password, project_id)


if os.path.exists(current_dir + "/json_file_storage" + f"/{email}/{project_id}.json"):
    save_dir = current_dir + "/json_file_storage" + f"/{email}/{project_id}.json"
    st.success("File uploaded and processed successfully!")
    load_session(sessionID)
else:
    st.error("Please upload the json file first")
    

st.sidebar.header("Select for conversation")

model = st.sidebar.selectbox("Model", ["Llama3 8b", "GPT 4o", "GPT 4o mini"])
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
BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "78cfb727-3ea4-4a66-9eb6-b63162529573"
ENDPOINT = "" 

TWEAKS = {
  "Chroma-1eSTL": {
    "allow_duplicates": False,
    "chroma_server_cors_allow_origins": "",
    "chroma_server_grpc_port": None,
    "chroma_server_host": "",
    "chroma_server_http_port": None,
    "chroma_server_ssl_enabled": False,
    "collection_name": "langflow",
    "limit": None,
    "number_of_results": 5,
    "persist_directory": "",
    "search_query": "",
    "search_type": "Similarity"
  },
  "ChatInput-dDm2D": {
    "files": "",
    "sender": "User",
    "sender_name": "User",
    "session_id": sessionID
  },
  "ChatOutput-ogNUN": {
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "AI",
    "session_id": ""
  },
  "ParseData-1k9JW": {
    "sep": "\n",
    "template": "{text}"
  },
  "GroupNode-mM4mq": {
    "path": current_dir + "/json_file_storage" + f"/{email}/{project_id}.json",
    "code": "from typing import List\n\nfrom langchain_text_splitters import CharacterTextSplitter\n\nfrom langflow.custom import CustomComponent\nfrom langflow.schema import Data\nfrom langflow.utils.util import unescape_string\n\n\nclass CharacterTextSplitterComponent(CustomComponent):\n    display_name = \"CharacterTextSplitter\"\n    description = \"Splitting text that looks at characters.\"\n\n    def build_config(self):\n        return {\n            \"inputs\": {\"display_name\": \"Input\", \"input_types\": [\"Document\", \"Data\"]},\n            \"chunk_overlap\": {\"display_name\": \"Chunk Overlap\", \"default\": 200},\n            \"chunk_size\": {\"display_name\": \"Chunk Size\", \"default\": 1000},\n            \"separator\": {\"display_name\": \"Separator\", \"default\": \"\\n\"},\n        }\n\n    def build(\n        self,\n        inputs: List[Data],\n        chunk_overlap: int = 200,\n        chunk_size: int = 1000,\n        separator: str = \"\\n\",\n    ) -> List[Data]:\n        # separator may come escaped from the frontend\n        separator = unescape_string(separator)\n        documents = []\n        for _input in inputs:\n            if isinstance(_input, Data):\n                documents.append(_input.to_lc_document())\n            else:\n                documents.append(_input)\n        docs = CharacterTextSplitter(\n            chunk_overlap=chunk_overlap,\n            chunk_size=chunk_size,\n            separator=separator,\n        ).split_documents(documents)\n        data = self.to_data(docs)\n        self.status = data\n        return data\n",
    "silent_errors": False,
    "chunk_overlap": 200,
    "chunk_size": 1000,
    "separator": " "
  },
  "GroupNode-XBRJ3": {
    "code": "from langflow.custom import Component\nfrom langflow.helpers.data import data_to_text\nfrom langflow.io import DropdownInput, IntInput, MessageTextInput, MultilineInput, Output\nfrom langflow.memory import get_messages\nfrom langflow.schema import Data\nfrom langflow.schema.message import Message\n\n\nclass MemoryComponent(Component):\n    display_name = \"Chat Memory\"\n    description = \"Retrieves stored chat messages.\"\n    icon = \"message-square-more\"\n\n    inputs = [\n        DropdownInput(\n            name=\"sender\",\n            display_name=\"Sender Type\",\n            options=[\"Machine\", \"User\", \"Machine and User\"],\n            value=\"Machine and User\",\n            info=\"Type of sender.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"sender_name\",\n            display_name=\"Sender Name\",\n            info=\"Name of the sender.\",\n            advanced=True,\n        ),\n        IntInput(\n            name=\"n_messages\",\n            display_name=\"Number of Messages\",\n            value=100,\n            info=\"Number of messages to retrieve.\",\n            advanced=True,\n        ),\n        MessageTextInput(\n            name=\"session_id\",\n            display_name=\"Session ID\",\n            info=\"Session ID of the chat history.\",\n            advanced=True,\n        ),\n        DropdownInput(\n            name=\"order\",\n            display_name=\"Order\",\n            options=[\"Ascending\", \"Descending\"],\n            value=\"Ascending\",\n            info=\"Order of the messages.\",\n            advanced=True,\n        ),\n        MultilineInput(\n            name=\"template\",\n            display_name=\"Template\",\n            info=\"The template to use for formatting the data. It can contain the keys {text}, {sender} or any other key in the message data.\",\n            value=\"{sender_name}: {text}\",\n            advanced=True,\n        ),\n    ]\n\n    outputs = [\n        Output(display_name=\"Chat History\", name=\"messages\", method=\"retrieve_messages\"),\n        Output(display_name=\"Messages (Text)\", name=\"messages_text\", method=\"retrieve_messages_as_text\"),\n    ]\n\n    def retrieve_messages(self) -> Data:\n        sender = self.sender\n        sender_name = self.sender_name\n        session_id = self.session_id\n        n_messages = self.n_messages\n        order = \"DESC\" if self.order == \"Descending\" else \"ASC\"\n\n        if sender == \"Machine and User\":\n            sender = None\n\n        messages = get_messages(\n            sender=sender,\n            sender_name=sender_name,\n            session_id=session_id,\n            limit=n_messages,\n            order=order,\n        )\n        self.status = messages\n        return messages\n\n    def retrieve_messages_as_text(self) -> Message:\n        messages_text = data_to_text(self.template, self.retrieve_messages())\n        self.status = messages_text\n        return Message(text=messages_text)\n",
    "template": "{sender_name}: {text}",
    "context": "",
    "question": "",
    "n_messages": 100,
    "order": "Ascending",
    "sender": "Machine and User",
    "sender_name": "",
    "session_id": sessionID
  },
  "OllamaEmbeddings-pPT7t": {
    "base_url": "http://localhost:11434",
    "model": "llama3:latest",
    "temperature": 0
  },
  "CombineText-9KPCn": {
    "delimiter": " ",
    "text1": "",
    "text2": ""
  },
  "TextInput-habii": {
    "input_value": "This is the file explaintion\n" + feature_explaintion + "\n" + "Please read the explaintion and take look at \"x\",\"y\",\"imp\",\"co\". For every json object, x and y means two factors that x is a cause of y. The bigger imp(importance) value means x and y have strongger causation. If \"co\" value smaller than 0, that means the bigger x will make smaller y. If \"co\" value bigger than 0, that means the bigger x will make bigger y.\n"
  },
  "CombineText-08Zjg": {
    "delimiter": " ",
    "text1": "",
    "text2": ""
  }
  
}


if model_type == "llama":
    TWEAKS.pop("OpenAIModel-JrTmO", None)
    TWEAKS.pop("OllamaModel-4U6xk", None)
    TWEAKS["OllamaModel-4U6xk"] = {
        "base_url": "http://localhost:11434",
        "format": "",
        "input_value": "",
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
        "stream": True,
        "system": "",
        "system_message": "",
        "tags": "",
        "temperature": 0.2,
        "template": "",
        "tfs_z": None,
        "timeout": None,
        "top_k": None,
        "top_p": None,
        "verbose": False
    }
else:
    TWEAKS.pop("OpenAIModel-JrTmO", None)
    TWEAKS.pop("OllamaModel-4U6xk", None)
    TWEAKS["OpenAIModel-JrTmO"] = {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "input_value": "",
        "json_mode": False,
        "max_tokens": None,
        "model_kwargs": {},
        "model_name": model_name,
        "openai_api_base": "",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.1
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