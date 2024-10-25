import openai

# Initialize the chat messages history
messages = [{
    "role": "system", 
    "content": """
            You are a software engineer who works in pharma. Your primary job is to listen to user query and convert it into action item which ALEX, a pharma automation system, can understand and also check against the `objectReferences` and 'validActions' given.
            objectReferences: 
            {'Bottle 2500ml': 'container-0', 
            'Beaker 1500ml': 'container-1', 
            'Volumetric Flask 300ml': 'container-2',
            'Conical Flask 100ml': 'container-3', 
            'Location 1': 'location-0', 
            'Location 2': 'location-1', 
            'Location 3': 'location-2', 
            'Location 4': 'location-3', 
            'Active Bottle Point': 'location-4', 
            'Active Flask Point': 'location-5', 
            'Storage Bottle Point': 'location-6', 
            'Storage Flask Point': 'location-7', 
            'NaOH': 'liquid-0', 
            'H2O': 'liquid-1',
            'NaCl': 'liquid-2'}.
            validActions :[add, move, stir, measure]. 
            measure: [pH, Weight].
            """
}]

# Function to display the assistant's responses
def display_chat_history(messages):
    for message in messages:
        if message['role'] == 'assistant':  # Only show assistant responses
            print(f"Response: {message['content']}")

# Function to get the assistant's response
def get_assistant_response(messages):
    r = openai.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:neural-foundry:actions5t:ALVrNGHN",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages],
    )
    response = r.choices[0].message.content + "\n"  
    return response

# Function to process tasks from the text file
def process_tasks_from_file(filename):
    with open(filename, 'r') as file:
        tasks = file.readlines()
        
    for task in tasks:
        task = task.strip()  # Remove any extra whitespace or newlines
        if task:
            print(f"Enter the input: {task}")
            
            # Append task (user input) to messages
            messages.append({"role": "user", "content": task})
            
            # Get assistant response
            response = get_assistant_response(messages)
            messages.append({"role": "assistant", "content": response})
            
            # Display the assistant's response
            display_chat_history([messages[-1]])

# Main execution
process_tasks_from_file('fine-tuning/test.txt')

# Wait for user input after processing the file
while True:
    user_input = input("Enter the input: ")
    
    # Append user input to messages
    messages.append({"role": "user", "content": user_input})
    
    # Get assistant response
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
    
    # Display the latest assistant response 
    display_chat_history([messages[-1]])