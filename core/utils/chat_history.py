import json
import os
from core.utils.dialogue import Message

default_chat_history_file = "chat_history.txt"

class ChatHistory:
    def __init__(self):
        self.chat_history_file = "data/." + default_chat_history_file
        self.user_message = None
        self.assistant_message = None

    def update_chat_history(self, query, response_message):
        self.user_message = Message(role="user", content=query)
        self.assistant_message = Message(role="assistant", content="".join(response_message))
        # self.dialogue.put(self.chat_history.user_message)
        # self.dialogue.put(self.chat_history.assistant_message)
        self.save_chat_history()
        
    def load_chat_history(self, dialogue):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    try:
                        data = json.loads(line)
                        role = data.get("role")
                        content = data.get("content")
                        if role and content:
                            dialogue.put(Message(role=role, content=content))
                    except json.JSONDecodeError:
                        self.logger.error(f"Failed to decode chat history line: {line}")

    def save_chat_history(self):
        mode = "a" if os.path.exists(self.chat_history_file) else "w"
        with open(self.chat_history_file, mode, encoding="utf-8") as f:
            if self.user_message:
                f.write(json.dumps({"role": self.user_message.role, "content": self.user_message.content}) + "\n")
            if self.assistant_message:
                f.write(json.dumps({"role": self.assistant_message.role, "content": self.assistant_message.content}) + "\n")