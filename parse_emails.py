import json
from bs4 import BeautifulSoup

messages = []
def parse_emails():
    with open('messages.txt', 'r') as f:
        # Create a JSON decoder
        decoder = json.JSONDecoder()
        # Read the file content
        content = f.read()
        # Decode JSON objects one by one
        while content:
            try:
                # Decode the next object
                obj, idx = decoder.raw_decode(content)
                # Print the object
                messages.append(obj)
                # Skip the decoded object and whitespace characters
                content = content[idx:].lstrip()
            except ValueError:
                # Couldn't decode the JSON object
                break
    m = []
    for i in messages:
        soup = BeautifulSoup(i['body']['content'], 'html.parser')
        plain_text = soup.get_text()
        m.append({'subject':i['subject'],'body':plain_text})
        print(plain_text)
    return(m)

             
    
