import sys
import time
import argparse

import subprocess
import threading
import requests
import json
import time
from bs4 import BeautifulSoup
from gpt_chat import chat_with_gpt
from parse_emails import parse_emails
from web_search import web_search
from voice_assistant import (
    recognize_speech_vosk,
    text_to_speech,
    play_audio,
    wait_for_keyphrase,
    get_user_input
)



model_path = "../vosk-model-small"

# Setup Audio Files
input_file = "output.mp3"
output_file = "output_modulated.mp3"

# Increase speed by a factor of 1.5
speed_factor = 1.2

# Increase pitch by a factor of 1.2
pitch_factor = .6

def run_mail_read():
    subprocess.run(["python", "mail_read.py"])

def read_emails():
    with open('messages.txt', 'r') as f:
        # Load the JSON data into a Python dictionary
        emails = json.load(f)
        return(emails)
    

begin_prompt = """You are an expert CEO administrative assistnant.
You have the ability to read and write emails and do web searches along with your other capabilities.
If the user/CEO requests you to read the email please put the 'READ_EMAILS' command in your response.
If the user/CEO requests that you do a web search please put the 'WEB_SEARCH:{search query text}' in your respons. with the {search query text} being the text for the websearch.
Please try to respond in as few as words as possible unless asked to provide a longer response.
"""

messages=[{"role": "system", "content": begin_prompt}]

text = "Booting Up TaskForceAI"
text_to_speech(text)

keyphrase = 'question'
closing_argument = "thank you task force"

def save_code_to_file(code, filename):
    with open(filename, 'w') as f:
        f.write(code)

def filter_code(code):
    better = ''
    for i,x in enumerate(code.split('\n')):
        if '```' not in x and i > 0:
            better += '\n'+x
        elif '```' not in x:
            better += x


def parse_arguments():
    parser = argparse.ArgumentParser(description="A simple CLI program with progress animation.")
    parser.add_argument("-a", "--arg1", help="First argument", type=str, required=False)
    parser.add_argument("-b", "--arg2", help="Second argument", type=int, default=0)
    return parser.parse_args()

def progress_animation(duration=5, speed=0.1):
    animation_chars = "|/-\\"
    print("Processing:", end=" ", flush=True)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for char in animation_chars:
            sys.stdout.write(char)
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(speed)

def main():
    global model_path
    args = parse_arguments()

    # Process the arguments
    if args:
        for i, (key, value) in enumerate(vars(args).items()):
            if value is not None:
                print(f"Argument {i}: {key} = {value}")

    # Run the progress animation
    progress_animation()

    print("Processing complete!")

    # ---- main -----
    while True:
        if wait_for_keyphrase(model_path):
            while True:
                user_input = get_user_input(model_path)
                if user_input.lower() == "quit":
                    break
                if closing_argument.lower() in user_input.lower():
                    break
                prompt = f"User: {user_input}\nAI:"
                response = chat_with_gpt(prompt,messages)
                print(f"TFAI: {response}\n")
                # Play the response using text_to_speech function
                text_to_speech(response)
                messages.append({"role":"assistant","content":response})
                if 'PYTHON_COMMANDS:' in response:
                    code = response.split('PYTHON_COMMANDS:')[1]
                    code = filter_code(code)
                    try:
                        exec(code)
                    except:
                        print('exec failed: ',code)
                if 'READ_EMAILS' in response:
                    text_to_speech('Pulling up your emails now...')
                    mail_read_thread = threading.Thread(target=run_mail_read)
                    mail_read_thread.start()
                    mail = requests.get("http://127.0.0.1:5000")
                    time.sleep(10)
                    emails = parse_emails()
                    for i in emails:
                        text_to_speech(i['subject'])
                if 'WEB_SEARCH' in response:
                    search_query = response.split('WEB_SEARCH:')[1]
                    text_to_speech(f'searching for {search_query}')
                    print('need to program web search')

if __name__ == "__main__":
    main()
