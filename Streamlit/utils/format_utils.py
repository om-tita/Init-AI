from typing import Dict

def format_chat_message(role: str, content: str) -> Dict[str, str]:
    """
    Format a chat message for the OpenAI API.

    Args:
        role (str): The role of the message sender, "user", "assistant", or "system"
        content (str): The content of the message

    Returns:
        Dict[str, str]: A formatted message dictionary
    """
    return {"role": role, "content": content}
