import json
from collections import Counter

# Open and load the JSON file
with open('conversation-contexts.json', 'r') as file:
    data = json.load(file)

# Count the occurrences of each category
category_counts = Counter(item['category'] for item in data)

# Print the statistics
print("Number of entries by category:")
for category, count in category_counts.items():
    print(f"{category}: {count}")

# Print the total number of entries
print(f"\nTotal number of entries: {len(data)}")