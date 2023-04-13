import json
import html2text

def read_json_objects(file_path):
    with open(file_path, 'r') as file:
        file_contents = ""
        objects = []

        for line in file:
            file_contents += line.strip()

            if line.startswith('}'):
                objects.append(json.loads(file_contents))
                file_contents = ""

    return objects

def convert_html_to_text(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    return h.handle(html)

def save_messages_to_json_file(messages, output_file):
    with open(output_file, 'w') as file:
        json.dump(messages, file, indent=2)

file_path = "messages.txt"
output_file = "messages.txt"
messages = read_json_objects(file_path)

for message in messages:
    html_content = message['body']['content']
    plain_text = convert_html_to_text(html_content)
    message['body']['content'] = plain_text

save_messages_to_json_file(messages, output_file)
