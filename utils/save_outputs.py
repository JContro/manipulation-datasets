import logging
import json
import os

logger = logging.getLogger(__name__)

CONVERSATIONS_PATH = os.getenv("CONVERSATIONS_PATH", "data")

def save_outputs(outputs, filename=CONVERSATIONS_PATH):
    if not isinstance(outputs, list):
        logger.error("Invalid input: outputs must be a list")
        raise ValueError("outputs must be a list")

    filepath = os.path.join(CONVERSATIONS_PATH, filename)
    logger.info(f"Attempting to save outputs to {filepath}")

    try:
        if not os.path.exists(CONVERSATIONS_PATH):
            os.makedirs(CONVERSATIONS_PATH)
            logger.info(f"Created directory: {CONVERSATIONS_PATH}")

        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                existing_outputs = json.load(f)
            logger.info(f"Loaded {len(existing_outputs)} existing outputs from {filepath}")
        else:
            existing_outputs = []
            logger.info(f"No existing file found at {filepath}. Starting with empty list.")

        existing_outputs.extend(outputs)
        logger.info(f"Added {len(outputs)} new outputs. Total outputs: {len(existing_outputs)}")

        with open(filepath, 'w') as f:
            json.dump(existing_outputs, f, indent=4)
        logger.info(f"Successfully saved {len(existing_outputs)} outputs to {filepath}")

    except json.JSONDecodeError:
        logger.error(f"Failed to parse existing JSON in {filepath}. File may be corrupted.")
        raise
    except PermissionError:
        logger.error(f"Permission denied when trying to write to {filepath}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise
