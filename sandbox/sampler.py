import json
import random

# Input and output file paths
input_file = '../data/comments.jsonl'
output_file = '../data/sampled_comments.json'

# Read the JSONL file and store all entries
entries = []
with open(input_file, 'r') as file:
    for line in file:
        entry = json.loads(line)
        # Extract only the required fields
        filtered_entry = {
            'id': entry['id'],
            'persuasiveness': entry['persuasiveness'],
            'comments': []
        }
        for comment in entry['comments']:
            filtered_comment = {
                'preprocessed_comment': comment.get('preprocessed_comment'),
                'comment_frames': comment.get('comment_frames')
            }
            filtered_entry['comments'].append(filtered_comment)
        entries.append(filtered_entry)

# Sample 200 random entries
sampled_entries = random.sample(entries, min(200, len(entries)))

# Write the sampled entries to a new JSON file
with open(output_file, 'w') as file:
    json.dump(sampled_entries, file, indent=2)

print(f"Sampled {len(sampled_entries)} entries and saved to {output_file}")
