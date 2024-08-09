import logging
import json
import os
import uuid

logger = logging.getLogger(__name__)
CONVERSATIONS_PATH = os.getenv("CONVERSATIONS_PATH", "data")

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

        # Check and add UUID to each conversation
        for conversation in existing_outputs + outputs:
            if "id" not in conversation or not conversation["id"]:
                conversation["id"] = str(uuid.uuid4())
                logger.info(f"Added UUID {conversation['id']} to a conversation")

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