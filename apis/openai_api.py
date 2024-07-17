from utils.open_contexts import get_random_contexts
from utils.open_manipulations import get_manipulation_tactics
from utils.generate_prompt import generate_prompts
from utils.save_outputs import save_outputs

from openai import OpenAI

import os 

import logging
logger = logging.getLogger(__name__)



def run_model(n):
    logger.info(f"Running the model with n={n}")
    
    contexts = get_random_contexts(n)
    logger.debug(contexts)
    
    manipulation_tactics = get_manipulation_tactics()
    logger.debug(manipulation_tactics)
    
    prompt = generate_prompts(contexts=contexts, manipulation_types=manipulation_tactics, n=n)
    logger.debug(prompt)

    # use the prompt to call the api
    # log the useful information
    api_key = os.getenv("OPENAI_API_KEY")
    logger.debug(f"API key: {api_key[:8]}...")

    client = OpenAI(
        api_key=api_key
    )
    
    output = prompt.copy()
    output['model'] = "gpt-4o"
    message = [
            {
                "role": "system",
                "content": prompt["prompt"],
            }
        ]
    chat_completion = client.chat.completions.create(
        messages=message,
        model="gpt-4o",
        )
    
    output["chat_completion"] = chat_completion

    save_outputs(outputs=output)
    

