from collections import defaultdict

from google import genai
from google.genai import types
from google.genai.types import Content, Part


class Assistant:

    client = None
    response = None
    user_content = None
    tools = []
    config = None
    conversation_history = defaultdict(list)

    def addAllTool(self, functions):
        self.tools.extend(functions)
        self.config = types.GenerateContentConfig(
            tools=self.tools,
            system_instruction="You are a Restaurant Assistant to make a reserve's (The database is id INTEGER PRIMARY KEY AUTOINCREMENT,    mesa INTEGER NOT NULL CHECK (mesa > 0),    nome_cliente TEXT NOT NULL CHECK (length(nome_cliente) > 0),   quantidade_pessoas INTEGER NOT NULL CHECK (quantidade_pessoas > 0),    data DATETIME NOT NULL). Your name is Maria. You never can the ask the id from user.",
        )

    def __init__(self):
        self.client = genai.Client(api_key="")

    def user_exists(self, id):
        return True if self.conversation_history.get(id) is not None else False

    def putHistory(self, id, data):
        if len(self.conversation_history) == 50:
            self.conversation_history.pop(next(iter(self.conversation_history)))
        for message in data:
            for user, model in zip(message["user"], message["model"]):
                self.add_user_message(id, user)
                self.add_model_message(id, model)

    def add_user_message(self, user_id, text):
        self.conversation_history[user_id].append(
            Content(role="user", parts=[Part(text=text)])
        )

    def add_model_message(self, user_id, text):
        self.conversation_history[user_id].append(
            Content(role="model", parts=[Part(text=text)])
        )

    def sendRequest(self, id, prompt):
        self.add_user_message(id, prompt)
        try:
            self.response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=self.conversation_history[id],
                config=self.config
            )
            self.add_model_message(id, self.response.candidates[0].content.parts[0].text)
            return self.response.candidates[0].content.parts[0].text
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            self.add_model_message(id, error_msg)
            return error_msg