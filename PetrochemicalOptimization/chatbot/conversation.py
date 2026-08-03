from chatbot.memory import ConversationMemory


class Conversation:

    def __init__(self, assistant):

        self.assistant = assistant
        self.memory = ConversationMemory()

    def send_message(
        self,
        user_message,
        refinery=None,
        optimization_result=None,
        maintenance_schedule=None
    ):

        # Save user message
        self.memory.add_user_message(
            user_message
        )

        history = self.memory.get_history()

        last_intent = None

        for item in reversed(history):

            if item["role"] == "user":

                if item["content"] != user_message:

                    last_intent = self.assistant.detect_intent(
                        item["content"]
                    )

                    break

        # Generate assistant response
        response = self.assistant.generate_response(

            message=user_message,

            refinery=refinery,

            optimization_result=optimization_result,

            maintenance_schedule=maintenance_schedule,

            history=history,

            last_intent=last_intent

        )

        # Save assistant message
        self.memory.add_assistant_message(
            response
        )

        return response

    def get_history(self):

        return self.memory.get_history()

    def clear(self):

        self.memory.clear()