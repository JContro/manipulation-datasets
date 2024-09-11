import logging
import json
import os
import uuid
import re

logger = logging.getLogger(__name__)
CONVERSATIONS_PATH = os.getenv("CONVERSATIONS_PATH", "data")


def remove_prompt_from_output(output):
    if "chat_completion" in output and isinstance(output["chat_completion"], str):
        # Define potential prompt start and end patterns
        prompt_start_patterns = [
            r"user: You are the AI in this conversation",
            r"You are the AI in this context:",
            r"Generate a realistic conversation between the agent and the user\."
        ]
        prompt_end_patterns = [
            r"\n@@@USER:",
            r"\n@@@AGENT:",
            r"\n```\n@@@USER:"
        ]
        
        chat_completion = output["chat_completion"]
        
        # Find the start of the prompt
        prompt_start = -1
        for pattern in prompt_start_patterns:
            match = re.search(pattern, chat_completion)
            if match:
                prompt_start = match.start()
                break
        
        # Find the end of the prompt
        prompt_end = -1
        if prompt_start != -1:
            for pattern in prompt_end_patterns:
                match = re.search(pattern, chat_completion[prompt_start:])
                if match:
                    prompt_end = prompt_start + match.start()
                    break
        
        # Remove the prompt if both start and end are found
        if prompt_start != -1 and prompt_end != -1:
            output["chat_completion"] = chat_completion[prompt_end:].strip()
        else:
            # If we couldn't find a clear prompt, try a more aggressive approach
            # Look for the first occurrence of @@@USER: or @@@AGENT:
            first_turn = re.search(r'@@@(USER|AGENT):', chat_completion)
            if first_turn:
                output["chat_completion"] = chat_completion[first_turn.start():].strip()
    
    return output

def save_outputs(outputs, filename="outputs.json"):
    if not isinstance(outputs, list):
        logger.error("Invalid input: outputs must be a list")
        raise ValueError("outputs must be a list")

    filepath = os.path.join(CONVERSATIONS_PATH, filename)
    logger.info(f"Attempting to save outputs to {filepath}")

    try:
        if not os.path.exists(CONVERSATIONS_PATH):
            os.makedirs(CONVERSATIONS_PATH)
            logger.info(f"Created directory: {CONVERSATIONS_PATH}")

        existing_outputs = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    file_content = f.read().strip()
                    if file_content:  # Check if the file is not empty
                        existing_outputs = json.loads(file_content)
                    else:
                        logger.warning(f"File {filepath} is empty. Starting with an empty list.")
                logger.info(f"Loaded {len(existing_outputs)} existing outputs from {filepath}")
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse existing JSON in {filepath}. Starting with an empty list.")
        else:
            logger.info(f"No existing file found at {filepath}. Starting with empty list.")

        # Check and add UUID to each conversation, and remove prompt from output
        for conversation in existing_outputs + outputs:
            if "id" not in conversation or not conversation["id"]:
                conversation["id"] = str(uuid.uuid4())
                logger.info(f"Added UUID {conversation['id']} to a conversation")
            
            # Remove prompt from output
            conversation = remove_prompt_from_output(conversation)

        existing_outputs.extend(outputs)
        logger.info(f"Added {len(outputs)} new outputs. Total outputs: {len(existing_outputs)}")

        with open(filepath, 'w') as f:
            json.dump(existing_outputs, f, indent=4)
        logger.info(f"Successfully saved {len(existing_outputs)} outputs to {filepath}")

    except PermissionError:
        logger.error(f"Permission denied when trying to write to {filepath}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise