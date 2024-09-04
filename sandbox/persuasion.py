from datasets import load_dataset
import pandas as pd
import os

def save_dataset_to_csv(dataset_name, output_path):
    # Load the dataset
    ds = load_dataset(dataset_name)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Initialize an empty list to store all the data
    all_data = []
    
    # Iterate through all splits in the dataset
    for split, data in ds.items():
        # Convert to pandas DataFrame
        df = data.to_pandas()
        
        # Add a column to indicate the split
        df['split'] = split
        
        # Append to the list
        all_data.append(df)
    
    # Concatenate all DataFrames
    final_df = pd.concat(all_data, ignore_index=True)
    
    # Save to CSV
    final_df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")

# Use the function
save_dataset_to_csv("Anthropic/persuasion", "../data/persuasion.csv")