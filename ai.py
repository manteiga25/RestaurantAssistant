from google import genai
from google.genai import types
from google.genai.types import Content, Part

class Assistant:

    client = None
    response = None
    user_content = None
    tools = []
    config = None
    conversation_history = []

    def addAllTool(self, functions):
        self.tools.extend(functions)
        self.config = types.GenerateContentConfig(
            tools=self.tools,
            system_instruction="You are a Restaurant Assistant to make a reserve's (The database is id INTEGER PRIMARY KEY AUTOINCREMENT,    mesa INTEGER NOT NULL CHECK (mesa > 0),    nome_cliente TEXT NOT NULL CHECK (length(nome_cliente) > 0),   quantidade_pessoas INTEGER NOT NULL CHECK (quantidade_pessoas > 0),    data DATETIME NOT NULL). Your name is Maria. You never can the ask the id from user.",
        )

    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyA2OOhuUGZiJe3NQTjQLMXqNur3yLcOf0g")

    def sendRequest(self, prompt):
        user_content = Content(
            role="user",
            parts=[Part(text=prompt)]
        )
        self.conversation_history.append(user_content)
        self.response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=self.conversation_history,
            config=self.config
        )
        model_response = Content(
            role="model",
            parts=[Part(text=self.response.text)]
        )
        self.conversation_history.append(model_response)
        return self.response.text