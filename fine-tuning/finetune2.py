import openai

# Initialize the chat messages history
messages = [{
    "role": "system", 
    "content": """objectReferences: 
            {'Bottle 1500ml': 'container-0', 
            'Beaker 500ml': 'container-2', 
            'Volumetric Flask 250ml': 'container-3', 
            'Location 1': 'location-0', 
            'Location 2': 'location-1', 
            'Location 3': 'location-2', 
            'Location 4': 'location-3', 
            'Active Bottle Point': 'location-4', 
            'Active Flask Point': 'location-5', 
            'Storage Bottle Point': 'location-6', 
            'Storage Flask Point': 'location-7', 
            'NaOH': 'liquid-0', 
            'Water': 'liquid-1', 
            'NaCl': 'liquid-2'}. \
            validActions: ['add', 'move', 'stir', 'measure']. \
            measure: ['pH', 'weight']"""
}]

# Function to display the assistant's responses
def display_chat_history(messages):
    for message in messages:
        if message['role'] == 'assistant':  # Only show assistant responses
            print(f"Response: {message['content']}")

# Function to get the assistant's response
def get_assistant_response(messages):
    r = openai.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:neural-foundry:actions4t:ALUozvhQ",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages]       
    )
    response = r.choices[0].message.content + "\n"  
    return response

# Wait for user input after processing the file
while True:
    user_input = input("Please enter the input: ")
    
    # Append user input to messages
    messages.append({"role": "user", "content": user_input})
    
    # Get assistant response
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
    
    # Display the latest assistant response 
    display_chat_history([messages[-1]])
