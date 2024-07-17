import os
import logging
import google.generativeai as genai
from typing import Dict
from utils.open_contexts import get_random_contexts
from utils.open_manipulations import get_manipulation_tactics
from utils.generate_prompt import generate_prompts
from utils.save_outputs import save_outputs

logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "gemini-1.5-pro"

def setup_gemini_client() -> genai.GenerativeModel:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("Google API key not found in environment variables")
        raise ValueError("Google API key not set")
    logger.info(f"Initializing Google Gemini client with API key: {api_key[:8]}...")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)

def create_message(prompt: str) -> str:
    return prompt

def process_prompt(model: genai.GenerativeModel, prompt: Dict) -> Dict:
    try:
        message = create_message(prompt["prompt"])
        logger.info(f"Processing prompt: {prompt['prompt'][:50]}...")
        response = model.generate_content(message)
        output = prompt.copy()
        output["model"] = MODEL_NAME
        output["chat_completion"] = response.text
        logger.info("Prompt processed successfully")
        return output
    except Exception as e:
        logger.error(f"Error processing prompt: {str(e)}")
        raise

def run_model(n: int):
    logger.info(f"Starting model run with n={n}")
    try:
        contexts = get_random_contexts(n)
        logger.info(f"Generated {len(contexts)} random contexts")
        manipulation_tactics = get_manipulation_tactics()
        logger.info(f"Retrieved {len(manipulation_tactics)} manipulation tactics")
        prompts = generate_prompts(contexts=contexts, manipulation_types=manipulation_tactics, n=n)
        logger.info(f"Generated {len(prompts)} prompts")
        model = setup_gemini_client()
        outputs = []
        for prompt in prompts:
            output = process_prompt(model, prompt)
            outputs.append(output)
        save_outputs(outputs)
        logger.info(f"Saved {len(outputs)} outputs")
        logger.info("Model run completed successfully")
    except Exception as e:
        logger.error(f"Error in run_model: {str(e)}")
        raise