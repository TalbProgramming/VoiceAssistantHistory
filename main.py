
"""
Required installations (pip):
* pyttsx3
* SpeechRecognition
* pyAudio (needed for the SpeechRecognition functionality,
  if you get and error with "wheels", install directly from PYPI
* openAI

** payment for openAI "davinci" model usage - https://openai.com/api/pricing/
"""

import pyttsx3
import speech_recognition as sr
import openai


def read_string(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# connection with openAI API
openai.api_key = "MY_API_KEY"
openai.api_key = "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"
# setup audio and speech recognizer instance
r = sr.Recognizer()


with sr.Microphone() as source:
    with open('name.txt') as f:
        while True:
            audio = r.listen(source)  # starts and stops recording by default silence time

            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`

                # generating the text from recording
                generated_text = r.recognize_google(audio)
                print(f"The program thinks you said: \n>>>\t\t {generated_text}")

                # if the user called the AI name (inside 'name.txt')
                if f"hey {f.readlines()}" in generated_text:
                    read_string("Hey. ask me anything!")

                    # Sending the received text to chatGPT
                    response = openai.Completion.create(
                        model="text-davinci-003",  # chatGPT model
                        prompt=generated_text,
                        temperature=0.3,  # creativeness
                        max_tokens=150,
                        frequency_penalty=0.0,  # recurrence of sentences
                        presence_penalty=0.6,  # less repetitiveness
                    )

                    print(response.choices[0].text)
                    read_string(response.choices[0].text)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                read_string("I could not understand you")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                read_string("Error, restart the app please")
