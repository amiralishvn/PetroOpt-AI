class ConversationMemory:

    def __init__(self, max_history=20):

        self.max_history = max_history
        self.messages = []

    def add_user_message(self, message):

        self.messages.append({
            "role": "user",
            "content": message
        })

        self._trim()

    def add_assistant_message(self, message):

        self.messages.append({
            "role": "assistant",
            "content": message
        })

        self._trim()

    def get_history(self):

        return self.messages

    def clear(self):

        self.messages = []

    def last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]

    def _trim(self):

        if len(self.messages) > self.max_history:

            self.messages = self.messages[-self.max_history:]