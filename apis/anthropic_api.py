import os
import logging
from typing import Dict
from anthropic import Anthropic
from utils.open_contexts import get_random_contexts
from utils.open_manipulations import get_manipulation_tactics
from utils.generate_prompt import generate_prompts
from utils.save_outputs import save_outputs

logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "claude-3-5-sonnet-20240620"
MAX_TOKENS = 1000
TEMPERATURE = 0

def setup_anthropic_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("Anthropic API key not found in environment variables")
        raise ValueError("Anthropic API key not set")
    logger.info(f"Initializing Anthropic client with API key: {api_key[:8]}...")
    return Anthropic(api_key=api_key)

def create_message(prompt: str) -> Dict[str, str]:
    return {
        "role": "user",
        "content": [{"type": "text", "text": prompt}]
    }

def process_prompt(client: Anthropic, prompt: Dict) -> Dict:
    try:
        message = create_message(prompt["prompt"])
        logger.info(f"Processing prompt: {prompt['prompt'][:50]}...")
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[message]
        )
        output = prompt.copy()
        output["model"] = MODEL_NAME
        output["chat_completion"] = response.content[0].text
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
        client = setup_anthropic_client()
        outputs = []
        for prompt in prompts:
            output = process_prompt(client, prompt)
            outputs.append(output)
        save_outputs(outputs)
        logger.info(f"Saved {len(outputs)} outputs")
        logger.info("Model run completed successfully")
    except Exception as e:
        logger.error(f"Error in run_model: {str(e)}")
        raise
