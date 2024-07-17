import argparse
import sys
from dotenv import load_dotenv
import os
import logging


from apis.openai_api import run_model as openai_run_model

def setup_logging(log_level):
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def get_input(prompt, options=None):
    while True:
        user_input = input(prompt).lower()
        if options is None or user_input in options:
            return user_input
        logger.warning(f"Invalid input. Please choose from {', '.join(options)}.")

def get_integer_input(prompt, min_value=1):
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            logger.warning(f"Please enter a number greater than or equal to {min_value}.")
        except ValueError:
            logger.warning("Invalid input. Please enter a valid integer.")

def load_env_variables():
    load_dotenv()
    required_vars = ['HUGGINGFACE_TOKEN', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    if missing_vars:
        logger.error(f"The following required environment variables are missing: {', '.join(missing_vars)}")
        logger.error("Please add them to your .env file.")
        sys.exit(1)
    logger.info("Environment variables loaded successfully.")

def main():
    parser = argparse.ArgumentParser(description="Software configuration script")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--api", action="store_true", help="Use API mode")
    group.add_argument("--local", action="store_true", help="Use local mode")
    parser.add_argument("--model", choices=["claude", "gemini", "gpt4", "huggingface"], help="Select API model (only if --api is used)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level")
    parser.add_argument("-n", type=int, default=1, help="Custom parameter (default: 1)")
    args = parser.parse_args()

    global logger
    logger = setup_logging(args.log_level)

    load_env_variables()

    if len(sys.argv) == 1:
        logger.info("Welcome to the interactive configuration mode.")
        mode = get_input("Choose mode (api/local): ", ["api", "local"])
        if mode == "api":
            model = get_input("Choose API model (claude/gemini/gpt4/huggingface): ", ["claude", "gemini", "gpt4", "huggingface"])
        n = get_integer_input("Enter the value for n: ")
    else:
        mode = "api" if args.api else "local"
        model = args.model if args.api else None
        n = args.n

    logger.info(f"Selected mode: {mode}")
    if mode == "api":
        logger.info(f"Selected model: {model}")
    logger.info(f"Value of n: {n}")

    if mode == "api" and model:
        api_key_map = {
            "claude": ("ANTHROPIC_API_KEY", "Anthropic"),
            "gemini": ("GOOGLE_API_KEY", "Google"),
            "gpt4": ("OPENAI_API_KEY", "OpenAI"),
            "huggingface": ("HUGGINGFACE_TOKEN", "Hugging Face")
        }
        env_var, provider = api_key_map[model]
        api_key = os.getenv(env_var)
        if api_key:
            logger.info(f"Using {provider} API key")
            logger.debug(f"{provider} API key: {api_key[:8]}...")
        else:
            logger.error(f"{provider} API key not found in environment variables.")

        if model == "gpt4":
            openai_run_model(n)
            
        


if __name__ == "__main__":
    main()