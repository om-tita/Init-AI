from utils.open_ai_utils import get_chat_completion
from utils.prompt_utils import (
    SYSTEM_PRODUCT_REQUIREMENT_PROMPT,
    USER_PRODUCT_REQUIREMENT_PROMPT,
)
import json as JSON
import logging


class ChatProcessService:
    def __init__(self):
        pass

    def process_chat(messages, current_product_data):
        """
        Handles the user input, constructs the prompt, and gets the response from OpenAI.

        Args:
            messages: List of message history
            prompt: User input prompt
            system_prompt: System's predefined instructions

        Returns:
            Tuple (response, messages) where response is the assistant's reply and messages are the updated list of messages.
        """
        try:

            last_question = messages[-2]["content"] if len(messages) > 1 else ""
            last_answer = messages[-1]["content"] if len(messages) > 0 else ""
            user_prompt = USER_PRODUCT_REQUIREMENT_PROMPT(
                last_question=last_question,
                last_answer=last_answer,
                current_product_data=current_product_data,
            )
            system_prompt = SYSTEM_PRODUCT_REQUIREMENT_PROMPT()

            messages_to_send = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            # Get the chat completion from OpenAI API
            response = get_chat_completion(messages_to_send, model="gpt-4")
            output = JSON.loads(response)
           
            # Append the assistant's response to the messages
            if output:
                messages.append(
                    {
                        "role": "assistant",
                        "content": output.get("output").get("new_question"),
                    }
                )

            # next_question, updated_messages, updated_current_product_data
            next_question = output.get("output").get("new_question")
            updated_current_product_data = output.get("output").get(
                "current_product_data"
            )
            return next_question, messages, updated_current_product_data
        except Exception as e:
            logging.error(f"Error in processing chat: {e}")
            return None, messages, None
