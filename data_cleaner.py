import json
import logging
import re
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_conversation(conversation):
    cleaned_conversation = []
    system_message = None
    for turn in conversation.split('@@@')[1:]:  # Skip the first empty element
        turn = turn.strip()
        
        # Check for system message
        if turn.lower().startswith("system"):
            system_message = turn
            continue
        
        # Use regex to find the role (AGENT or USER) and the content
        match = re.match(r'^(AGENT|USER)(.*)$', turn, re.DOTALL | re.IGNORECASE)
        if match:
            role, content = match.groups()
            content = content.strip()
            if content.startswith(':'):
                content = content[1:].strip()
            content = re.sub(r'<<\s*|\s*>>', '', content)  # Remove << >> and surrounding whitespace
            cleaned_conversation.append({
                "role": role.upper(),
                "content": content
            })
        else:
            logger.warning(f"Couldn't parse turn: {turn}")
    
    return cleaned_conversation, system_message

def process_json(input_path, output_path):
    try:
        # Read the input JSON file
        with open(input_path, 'r') as file:
            data = json.load(file)
        logger.info(f"Successfully read input file: {input_path}")

        # Process each item in the JSON array
        for item in data:
            if 'chat_completion' in item:
                item['cleaned_conversation'], item['system_message'] = process_conversation(item['chat_completion'])

        # Write the processed data to the output file
        with open(output_path, 'w') as file:
            json.dump(data, file, indent=2)
        logger.info(f"Successfully wrote processed data to: {output_path}")

    except FileNotFoundError:
        logger.error(f"Input file not found: {input_path}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in input file: {input_path}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    input_path = Path("data/outputs.json")
    output_path = Path("data/conversations.json")
    process_json(input_path, output_path)