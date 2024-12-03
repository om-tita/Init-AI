import asyncio
import json
from exceptions import NotFoundException
from utils import prompt_utils, open_ai_utils

class StackSuggestionService:
    @staticmethod
    def stack_suggestion(enhanced_description): 
        system_prompt = prompt_utils.STACK_SUGGESTION_SYSTEM_PROMPT() 
        
        messages = [
            open_ai_utils.format_chat_message("system", system_prompt),
            open_ai_utils.format_chat_message("user", enhanced_description)
        ]
        response = open_ai_utils.get_chat_completion(messages)
        
        print(response)
        
        return json.loads(response)