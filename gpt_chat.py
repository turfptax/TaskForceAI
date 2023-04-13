import openai
from openai.error import RateLimitError
import os
# Read the API key from UnderThePillow.txt
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'UnderThePillow.txt'), 'r') as f:
    api_key = f.read().strip()



# Set the API key
openai.api_key = api_key
def chat_with_gpt(prompt, messages):
    messages.append({"role":"user","content":prompt})
    global begin_prompt 
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=600,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].message['content'].strip()
    except RateLimitError as e:
        retry_after = int(e.headers.get('Retry-After', 60))
        print(f"You have exceeded the API rate limit. Waiting for {retry_after} seconds before retrying...")
        time.sleep(retry_after)
        return chat_with_gpt(prompt)
