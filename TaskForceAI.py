#main
from gpt_chat import chat_with_gpt
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

begin_prompt = """You are part of an advanced Team of python programmers in an automated system and are in charge of helping the whichever task you are given by running one of your built-in functions or creating new ones.
Here are your functions: save_code_to_file(code, filename), web_search(query), and list_files(). Please append the answer at the end with one of these commands if it is applicable using 'PYTHON_COMMANDS:' You can also use the PYTHON_COMMANDS: section to interact directly with the REPL environment if asked to.
Here is an example save_code_to_file response.
user: can you help me write a hello world python program?
assistant: Yes, I would be happy to help you. First we will create a python file and save it but you will have to run it.
PYTHON_COMMANDS:
save_code_to_file('print("hello world!")',hello_world.py)
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
