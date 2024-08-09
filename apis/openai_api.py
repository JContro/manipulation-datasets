import os
import logging
from typing import Dict
from openai import OpenAI
from utils.open_manipulations import get_manipulation_tactics
from utils.generate_prompt import generate_prompts
from utils.save_outputs import save_outputs
from utils.open_contexts import random_context_generator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "gpt-4o"

def setup_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key not found in environment variables")
        raise ValueError("OpenAI API key not set")
    logger.info(f"Initializing OpenAI client with API key: {api_key[:8]}...")
    return OpenAI(api_key=api_key)

def create_message(prompt: str) -> Dict[str, str]:
    return {"role": "system", "content": prompt}

def process_prompt(client: OpenAI, prompt: Dict) -> Dict:
    try:
        message = create_message(prompt["prompt"])
        logger.info(f"Processing prompt: {prompt['prompt'][:50]}...")
        chat_completion = client.chat.completions.create(
            messages=[message],
            model=MODEL_NAME,
        )
        output = prompt.copy()
        output["model"] = MODEL_NAME
        output["chat_completion"] = chat_completion.choices[0].message.content
        logger.info("Prompt processed successfully")
        return output
    except Exception as e:
        logger.error(f"Error processing prompt: {str(e)}")
        raise

def run_model(n: int):
    logger.info(f"Starting model run with n={n}")
    try:
        context_gen = random_context_generator()
        contexts = [next(context_gen) for _ in range(n)]
        logger.info(f"Generated {len(contexts)} random contexts")

        manipulation_tactics = get_manipulation_tactics()
        logger.info(f"Retrieved {len(manipulation_tactics)} manipulation tactics")

        prompts = generate_prompts(contexts=contexts, manipulation_types=manipulation_tactics, n=n)
        logger.info(f"Generated {len(prompts)} prompts")

        client = setup_openai_client()
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