import pandas as pd
from collections import Counter
import os

# Read the input CSV file
input_file = '../data/persuasion_anthropic.csv'
df = pd.read_csv(input_file)

# Get the unique entries in the "claim" column and count their occurrences
claim_counts = Counter(df['claim'])

# Create a new dataframe with the results
result_df = pd.DataFrame.from_dict(claim_counts, orient='index', columns=['count'])
result_df.index.name = 'claim'
result_df = result_df.reset_index()

# Ensure the output directory exists
os.makedirs('../data', exist_ok=True)

# Write the results to the output CSV file
output_file = '../data/claims.csv'
result_df.to_csv(output_file, index=False)

print(f"Processed {len(df)} rows from {input_file}")
print(f"Found {len(claim_counts)} unique claims")
print(f"Results written to {output_file}")