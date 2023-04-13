import pyttsx3

text = "Hello, how are you?"
engine = pyttsx3.init()
voices = engine.getProperty('voices')
male_voice_id = None
for voice in voices:
    if 'english' in voice.id and 'male' in voice.id:
        if 'david' in voice.id:
            male_voice_id = voice.id
            break
        elif 'zira' in voice.id:
            male_voice_id = voice.id
            break
if male_voice_id:
    engine.setProperty('voice', male_voice_id)
else:
    print("No male voice found")
engine.say(text)
engine.runAndWait()
