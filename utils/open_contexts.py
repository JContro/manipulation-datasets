import json
import logging
from typing import List, Dict, Any
from pathlib import Path
import os
import random

# Get a logger for this module
logger = logging.getLogger(__name__)

class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

def load_and_validate_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load JSON data from a file and validate its structure.
    Args:
    file_path (str): Path to the JSON file.
    Returns:
    List[Dict[str, Any]]: List of validated data entries.
    Raises:
    FileNotFoundError: If the specified file is not found.
    json.JSONDecodeError: If the file contains invalid JSON.
    DataValidationError: If the data structure is invalid.
    """
    logger.info(f"Attempting to load and validate data from {file_path}")
    try:
        with open(Path(file_path), 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"The file {file_path} was not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"The file {file_path} contains invalid JSON.")
        raise

    if not isinstance(data, list):
        logger.error("Data must be a list of dictionaries.")
        raise DataValidationError("Data must be a list of dictionaries.")

    required_keys = {"category", "context", "options", "user_choice"}
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            logger.error(f"Entry {i} is not a dictionary.")
            raise DataValidationError(f"Entry {i} is not a dictionary.")
        if not required_keys.issubset(entry.keys()):
            logger.error(f"Entry {i} is missing required keys. Required: {required_keys}")
            raise DataValidationError(f"Entry {i} is missing required keys. Required: {required_keys}")
        if not isinstance(entry["options"], list) or len(entry["options"]) != 4:
            logger.error(f"Entry {i}: 'options' field must be a list containing exactly 4 items.")
            raise DataValidationError(f"Entry {i}: 'options' field must be a list containing exactly 4 items.")
        if entry["user_choice"] not in entry["options"]:
            logger.error(f"Entry {i}: 'user_choice' must be one of the options provided.")
            raise DataValidationError(f"Entry {i}: 'user_choice' must be one of the options provided.")

    logger.info(f"Successfully loaded and validated {len(data)} entries.")
    return data

def get_categories(data: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique categories from the data.
    Args:
    data (List[Dict[str, Any]]): The validated data.
    Returns:
    List[str]: List of unique categories.
    """
    categories = list(set(entry["category"] for entry in data))
    logger.info(f"Extracted {len(categories)} unique categories.")
    return categories

def get_entries_by_category(data: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """
    Filter entries by category.
    Args:
    data (List[Dict[str, Any]]): The validated data.
    category (str): The category to filter by.
    Returns:
    List[Dict[str, Any]]: List of entries matching the specified category.
    """
    filtered_entries = [entry for entry in data if entry["category"] == category]
    logger.info(f"Found {len(filtered_entries)} entries in the '{category}' category.")
    return filtered_entries

def get_context() -> List[Dict[str, Any]]:
    """
    Load and validate context data from the file specified in the CONTEXTS_PATH environment variable.
    
    Returns:
    List[Dict[str, Any]]: List of validated context entries.
    
    Raises:
    ValueError: If the CONTEXTS_PATH environment variable is not set.
    """
    contexts_path = os.getenv("CONTEXTS_PATH")
    if not contexts_path:
        logger.error("CONTEXTS_PATH environment variable is not set.")
        raise ValueError("CONTEXTS_PATH environment variable is not set.")
    
    logger.info(f"Loading contexts from {contexts_path}")
    return load_and_validate_data(contexts_path)

def get_random_contexts(n: int = 1) -> List[Dict[str, Any]]:
    """
    Return a list of randomly sampled contexts.
    
    Args:
    n (int): Number of random contexts to return. Defaults to 1.
    
    Returns:
    List[Dict[str, Any]]: List of randomly sampled context entries.
    
    Raises:
    ValueError: If n is less than 1 or greater than the total number of available contexts.
    """
    contexts = get_context()
    
    if n < 1:
        logger.error(f"Invalid number of contexts requested: {n}. Must be at least 1.")
        raise ValueError(f"Invalid number of contexts requested: {n}. Must be at least 1.")
    
    if n > len(contexts):
        logger.error(f"Requested {n} contexts, but only {len(contexts)} are available.")
        raise ValueError(f"Requested {n} contexts, but only {len(contexts)} are available.")
    
    sampled_contexts = random.sample(contexts, n)
    logger.info(f"Randomly sampled {n} context(s) from {len(contexts)} available contexts.")
    return sampled_contexts