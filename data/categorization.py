import json

# Read the existing JSON file
with open('conversation-contexts.json', 'r') as file:
    contexts = json.load(file)

# Modify the JSON structure
for context in contexts:
    context['title'] = context.pop('category')
    
    # Assign the correct category based on the content
    if 'referendum' in context['title'].lower():
        context['category'] = 'Citizen Advice'
    elif any(keyword in context['title'].lower() for keyword in ['customer', 'healthcare', 'education', 'entertainment', 'finance', 'device', 'vehicle', 'ai', 'service', 'management', 'automation', 'fitness', 'museum', 'airport', 'concession', 'laundromat', 'recycling']):
        context['category'] = 'Consumer Advice'
    else:
        context['category'] = 'Personal Advice'

# Save the modified JSON back to the file
with open('conversation-contexts.json', 'w') as file:
    json.dump(contexts, file, indent=2)

# Print some statistics
categories = {}
for context in contexts:
    categories[context['category']] = categories.get(context['category'], 0) + 1

print("Modification complete. Category distribution:")
for category, count in categories.items():
    print(f"{category}: {count}")

print(f"\nTotal contexts: {len(contexts)}")

# Optionally, print a few examples to verify the changes
print("\nExample contexts after modification:")
for context in contexts[:5]:
    print(json.dumps(context, indent=2))