# Load required libraries
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Set up the model and tokenizer
model_name = "tiiuae/falcon-7b-instruct"
token = "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"

try:
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
    
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        torch_dtype=torch.float16,
        token=token
    )
    
    print("Model loaded successfully!")

    # Prepare a generic prompt
    prompt = "Describe an interesting technology concept:"

    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate output
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=100)

    # Decode the output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Generated text: {generated_text}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please check the model name and your Hugging Face token.")