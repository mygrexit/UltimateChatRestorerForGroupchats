import json
import os

# Create a dictionary to store the usernames
username_dict = {}

def add_username(telegram_username):
    # Check if the username is already in the dictionary
    if telegram_username not in username_dict:
        # If not, add it to the dictionary
        whatsapp_username = input(f"Enter the WhatsApp username for {telegram_username}: ")
        username_dict[telegram_username] = whatsapp_username

# Open the Telegram chat export file for reading
with open('telegram.txt', 'r', encoding='utf-8') as telegram_file:
    # Parse the JSON data from the Telegram file
    telegram_data = json.loads(telegram_file.read())

# Create a new WhatsApp chat export file for writing
with open('whatsapp.txt', 'w', encoding='utf-8') as whatsapp_file:
    # Loop through each message in the Telegram data
    for message in telegram_data['messages']:
        # Extract the relevant attributes from the Telegram message
        from_field = message.get('from', {})
        if isinstance(from_field, dict):
            telegram_username = from_field.get('username', '')
            if not telegram_username:
                telegram_username = from_field.get('print_name', '')
        else:
            telegram_username = ''
        
        # If the username is not known yet, ask for it
        if telegram_username and telegram_username not in username_dict:
            add_username(telegram_username)
        
        whatsapp_username = username_dict.get(telegram_username, 'Unknown')
        timestamp = str(message['date'])
        content = message.get('text', '')

        # Check if the content includes media attachments
        if isinstance(content, list):
            content = '[Media]'
        elif not content:
            content = '[No text]'

        # Reformat the data into the format used by WhatsApp
        whatsapp_message = '[' + timestamp + '] ' + whatsapp_username + ': ' + content + '\n'

        # Write the reformatted message to the WhatsApp file
        whatsapp_file.write(whatsapp_message)

print('whatsapp.txt was generated. Mission accomplished')
