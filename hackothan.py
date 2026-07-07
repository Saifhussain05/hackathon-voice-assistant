import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser
import os
import sys
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

recognizer = sr.Recognizer()

sleeping =False

def cmd():
    global sleeping
    with sr.Microphone() as source:
        print('Clearing background noises... Please wait')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything...')
        recorded_audio = recognizer.listen(source)

        try:
            print('Recognizing your message... Please wait')
            command = recognizer.recognize_google(recorded_audio, language='en-us')
            command = command.lower()
            print('Your message:', command)
            
            # Wake word if assistant is sleeping
            if sleeping:
                if "wake up" in command or "hey assistant" in command:
                    sleeping=False
                    engine.say("I am awake now.")
                    engine.runAndWait()
                else:
                    print("Assistant is sleeping... Say 'wake up' to activate.")
                    return
                
            # stop / exit
            if 'stop'in command or 'exit' in command or 'quit' in command:
                engine.say("Goodbye!")
                engine.runAndWait()
                sys.exit()
                
                # sleep mode
            elif 'sleep' in command:
                sleeping = True
                engine.say("Going to sleep. say 'wake up' to continue.")
                engine.runAndWait()

            # Commands
            if 'chrome' in command:
                a = 'Opening Chrome...'
                print(a)
                engine.say(a)
                engine.runAndWait()
                program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                subprocess.Popen([program])

            elif 'time' in command:
                time = datetime.datetime.now().strftime("%I:%M %p")
                print(time)
                engine.say(f"The time is {time}")
                engine.runAndWait()

            elif 'play' in command:
                b = 'Playing on YouTube...'
                print(b)
                engine.say(b)
                engine.runAndWait()
                pywhatkit.playonyt(command.replace("play", "").strip())
                
            elif 'open' in command:
                c='opening instagram...'
                print (c)
                engine.say(c)
                engine.runAndWait()
                try:
                    #Try to open instagram app (Microsoft store version)
                    os.system("start Instagram:")
                except Exception:
                    #Fallback: open in browser
                    webbrowser.open("https://www.Instagram.com")
                

            else:
                print("Command not recognized.")
                engine.say("Sorry, I didn't understand that.")
                engine.runAndWait()

        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        except Exception as ex:
            print("Error:", ex)

# Keep listening in a loop
while True:
    cmd()

# Note: Instagram is not opening in all devices and also the instagram should open when we will instagram while microsoft store
