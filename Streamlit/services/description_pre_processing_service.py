from utils.open_ai_utils import get_chat_completion
from utils.format_utils import format_chat_message
from utils.decorator_utils import check_data_variables
from utils.prompt_utils import (
    DESCRIPTION_PRE_PROCESSING_SYSTEM_PROMPT,
    DESCRIPTION_PRE_PROCESSING_USER_PROMPT,
)


class DescriptionPreProcessingService:
    def __init__(self):
        pass

    # @check_data_variables("description", "title")
    def description_pre_processing(self, description,title):

        user_prompt = DESCRIPTION_PRE_PROCESSING_USER_PROMPT(
            description, title
        )
        messages = [
            format_chat_message("system", DESCRIPTION_PRE_PROCESSING_SYSTEM_PROMPT()),
            format_chat_message("user", user_prompt),
        ]
        response = get_chat_completion(messages)
        return response
