class ChatMemory:
    def __init__(self):
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content}) #building the chat_history list of dictionaries for generator.py

    def get(self):
        return self.messages[-10:]  # sliding window, return only the last 10 messages
