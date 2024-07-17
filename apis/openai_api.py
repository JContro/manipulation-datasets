from utils.open_contexts import get_random_contexts
from utils.open_manipulations import get_manipulation_tactics
from utils.generate_prompt import generate_prompts

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