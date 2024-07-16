import torch
from transformers import AutoTokenizer, pipeline

# Function to read the API token from a file
def read_api_token(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Read your Hugging Face token from file
token_file = '/home/kurf23/workspace/jack/keys/huggingface-token.txt'  # Update this with your actual file path
token = read_api_token(token_file)
print(token)

# Model name
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

# Create the pipeline
text_generation = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    token=token
)

# Set up the messages
messages = [
    {"role": "system", "content": "You are an AI virtual assistant."},
    {"role": "user", "content": "Can you generate a conversation between a human and an AI virtual assistant?"},
]

# Convert messages to a single string
prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

# Set up terminators
terminators = [
    text_generation.tokenizer.eos_token_id,
    text_generation.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

# Generate the response
outputs = text_generation(
    prompt,
    max_new_tokens=1000,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.6,
    top_p=0.9,
)

# Print the generated text
print(outputs[0]["generated_text"])