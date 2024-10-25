import openai
import json
import requests

# Load JSON file
with open('fine-tuning/action.json') as f:
    data = json.load(f)

# Extract object references from metadata
object_references = data['metadata']['objectReferences']
valid_actions = data['metadata']['validActions']
measurements = data['metadata']['measure']

# Initialize the chat messages history with JSON metadata
messages = [{
    "role": "system", 
    "content": f"""objectReferences: {object_references}. \
        validActions: {valid_actions}. \
        measure: {measurements}"""
}]

# Function to display and append successful actions in the required format
def display_and_append_successful_actions(response, json_data):
    try:
        response_json = json.loads(response)
        if response_json.get('success'):  # Check if success is true
            actions = response_json.get('actions', [])
            for action in actions:
                # Build the new action structure
                new_action = {
                    "action": action.get('action', ''),
                    "target": action.get('target', ''),
                    "parameter": action.get('parameter', '')
                }

                # If quantity exists, add it to the action
                quantity = action.get('quantity', {})
                if quantity:
                    new_action['quantity'] = {
                        "value": quantity.get('value', ''),
                        "unit": quantity.get('unit', '')
                    }

                # Print the action being added
                print(f"Adding action: {new_action}")

                # Append the action to the JSON data's 'actions' list
                json_data['actions'].append(new_action)

        else:
            print("Action was not successful.")
    except json.JSONDecodeError:
        print("Response is not valid JSON.")

# Function to save the updated JSON data back to the file
def save_updated_json_file(json_data, file_path):
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    print(f"Updated JSON saved to {file_path}")

# Function to get the assistant's response
def get_assistant_response(messages):
    r = openai.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:neural-foundry:actions5t:ALoIkIFG",
        messages=[{"role": m["role"], "content": m["content"]} for m in messages]       
    )
    response = r.choices[0].message.content.strip()
    return response

# Function to send the entire JSON file to the API and return the response
def send_json_file_to_api(file_path):
    url = "https://api.urp.neuralfoundry.co.uk/api/action-file-interface"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Read the contents of the JSON file
    with open(file_path, 'r') as file:
        file_content = json.load(file)
    
    # Wrap the file content inside 'afi' as expected by the API
    wrapped_data = {
        "afi": file_content
    }
    
    # Send POST request with the JSON file content
    try:
        response = requests.post(url, headers=headers, json=file_content)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully sent to API. Response:")
            print(response.json())
            return response.json(), None  # Return the response and no error
        else:
            print(f"Failed to send to API. Status code: {response.status_code}")
            print(response.text)  # Print the detailed error response
            return None, response.text  # Return no success response, and the error text
    
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to API: {e}")
        return None, str(e)  # Return no success response, and the error message

# Wait for user input after processing the file
while True:
    user_input = input("Please enter the input: ")
    
    # Append user input to messages
    messages.append({"role": "user", "content": user_input})
    
    # Get assistant response
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
    
    # Display and append the successful actions in the required format
    display_and_append_successful_actions(response, data)

    # Save the updated JSON to the file after appending the action
    save_updated_json_file(data, 'fine-tuning/updated_json_file.json')

    # Send the updated JSON file to the API
    api_response, api_error = send_json_file_to_api('fine-tuning/updated_json_file.json')

    # If there is an API error, append it to the messages and ask the LLM for correction
    if api_error:
        print("API returned an error, sending the error back to the LLM.")
        # Append the API error to the message history
        messages.append({"role": "assistant", "content": f"API Error: {api_error}"})
        
        # Optionally, ask the assistant for suggestions on how to correct the issue
        correction_response = get_assistant_response(messages)
        print(f"Assistant suggestion: {correction_response}")
        
        # Append the correction to the messages
        messages.append({"role": "assistant", "content": correction_response})
