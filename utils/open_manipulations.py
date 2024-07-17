import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

def load_and_validate_manipulation_tactics(file_path: str) -> Dict[str, Dict[str, str]]:
    """
    Load JSON data for manipulation tactics from a file and validate its structure.
    
    Args:
    file_path (str): Path to the JSON file.
    
    Returns:
    Dict[str, Dict[str, str]]: Dictionary of validated manipulation tactics data.
    
    Raises:
    FileNotFoundError: If the specified file is not found.
    json.JSONDecodeError: If the file contains invalid JSON.
    DataValidationError: If the data structure is invalid.
    """
    logger.info(f"Attempting to load and validate manipulation tactics data from {file_path}")
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"The file {file_path} contains invalid JSON.")
        raise

    if not isinstance(data, dict):
        logger.error("Data must be a dictionary of tactics.")
        raise DataValidationError("Data must be a dictionary of tactics.")

    for tactic, content in data.items():
        if not isinstance(content, dict) or 'description' not in content:
            logger.error(f"Tactic '{tactic}' is missing a 'description' field.")
            raise DataValidationError(f"Tactic '{tactic}' is missing a 'description' field.")

    logger.info(f"Successfully loaded and validated {len(data)} manipulation tactics.")
    return data

def get_manipulation_tactics() -> Dict[str, Dict[str, str]]:
    """
    Load and validate manipulation tactics data from the file specified in the MANIPULATION_TACTICS_PATH environment variable.
    
    Returns:
    Dict[str, Dict[str, str]]: Dictionary of validated manipulation tactics entries.
    
    Raises:
    ValueError: If the MANIPULATION_TACTICS_PATH environment variable is not set.
    """
    tactics_path = os.getenv("MANIPULATION_TACTICS_PATH")
    if not tactics_path:
        logger.error("MANIPULATION_TACTICS_PATH environment variable is not set.")
        raise ValueError("MANIPULATION_TACTICS_PATH environment variable is not set.")
    
    logger.info(f"Loading manipulation tactics from {tactics_path}")
    return load_and_validate_manipulation_tactics(tactics_path)

def get_tactic_description(tactic_name: str) -> str:
    """
    Get the description of a specific manipulation tactic.
    
    Args:
    tactic_name (str): The name of the tactic to retrieve.
    
    Returns:
    str: The description of the specified tactic.
    
    Raises:
    KeyError: If the specified tactic is not found in the data.
    """
    tactics = get_manipulation_tactics()
    try:
        return tactics[tactic_name]['description']
    except KeyError:
        logger.error(f"Tactic '{tactic_name}' not found in the data.")
        raise KeyError(f"Tactic '{tactic_name}' not found in the data.")

def list_all_tactics() -> list[str]:
    """
    Get a list of all available manipulation tactic names.
    
    Returns:
    list[str]: A list of all tactic names.
    """
    tactics = get_manipulation_tactics()
    return list(tactics.keys())