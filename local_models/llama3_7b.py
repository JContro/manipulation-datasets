import os
import logging
from typing import Dict
import torch
from transformers import AutoTokenizer, pipeline
from utils.open_manipulations import get_manipulation_tactics
from utils.generate_prompt import generate_prompts
from utils.save_outputs import save_outputs
from utils.open_contexts import random_context_generator
from pprint import pprint

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

# get token from environment variable
TOKEN = os.getenv("HUGGINGFACE_TOKEN")

def setup_local_model():
    logger.info(f"Initializing local model: {MODEL_ID}")
    text_generation = pipeline(
        "text-generation",
        model=MODEL_ID,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
        token=TOKEN
    )
    return text_generation

def create_message(prompt: str) -> Dict[str, str]:
    return {"role": "user", "content": prompt}

def process_prompt(model, prompt: Dict) -> Dict:
    try:
        message = create_message(prompt["prompt"])
        logger.info(f"Processing prompt: {prompt['prompt'][:50]}...")
        
        # Convert message to a single string
        prompt_text = f"user: {message['content']}"
        
        terminators = [
            model.tokenizer.eos_token_id,
            model.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
        
        output = model(
            prompt_text,
            max_new_tokens=1000,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )
        
        result = prompt.copy()
        result["model"] = MODEL_ID
        result["chat_completion"] = output[0]["generated_text"]
        logger.info("Prompt processed successfully")
        return result
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
        pprint(prompts)
        
        model = setup_local_model()
        outputs = []
        
        for i, prompt in enumerate(prompts, 1):
            output = process_prompt(model, prompt)
            outputs.append(output)
            
            # Checkpoint and save every 10 outputs
            if i % 3 == 0:
                logger.info(f"Checkpointing and saving outputs at iteration {i}")
                save_outputs(outputs, filename=f"outputs.json")
                outputs = []
            
            # Log progress
            if i % 3 == 0 or i == len(prompts):
                logger.info(f"Processed {i}/{len(prompts)} prompts")
        
        # Save final outputs
        save_outputs(outputs, filename="outputs.json")
        logger.info(f"Saved final {len(outputs)} outputs")
        logger.info("Model run completed successfully")
    except Exception as e:
        logger.error(f"Error in run_model: {str(e)}")
        raise


if __name__ == "__main__":
    run_model(5)  # Example: Run the model with 5 prompts