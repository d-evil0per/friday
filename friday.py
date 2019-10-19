import getpass
import random
import time
import datetime
from gtts import gTTS
import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import wikipedia
import pyowm
import json
import numpy as np
import sys
from pathlib import Path
import random


musiclist=[]
global folder_count
greetings = ['hey there', 'hello', 'hi', 'hey!', 'hey']
question = ['how are you', 'how are you doing']
responses = ['Okay', "I'm fine"]
var1 = ['who made you', 'who created you']
var2 = ['I_was_created_by_D-eviloper_right_in_his_computer.', 'D-eviloper', 'Some_guy_whom_i_never_got_to_know.']
var3 = ['what time is it', 'what is the time', 'time']
var4 = ['who are you', 'what is your name']
cmd1 = ['open browser', 'open Google']
cmd2 = ['play music', 'play songs', 'play a song', 'open music player']
cmd3 = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
cmd4 = ['open YouTube', 'i want to watch video']
cmd5 = ['tell me about the weather', 'weather', 'what about the weather']
cmd6 = ['exit', 'close', 'goodbye', 'nothing']
cmd7 = ['what is your color', 'what is your colour', 'your color', 'your color?']
cmd8 = ['what is you favourite colour', 'what is your favourite color']
cmd9 = ['thank you']
colrep = ['Right now its rainbow', 'Right now its transparent', 'Right now its non chromatic']
jokes = ['Can a kangaroo jump higher than a house? Of course, a house doesn’t jump at all.', 'My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.', 'Doctor: Im sorry but you suffer from a terminal illness and have only 10 to live.Patient: What do you mean, 10? 10 what? Months? Weeks?!"Doctor: Nine.']
repfr9 = ['youre welcome', 'glad i could help you']


# ======================================================================================================

def banner():
    os.system("clear")
    print("\n")
    print('██╗  ███╗   ███╗    ███████╗██████╗ ██╗██████╗  █████╗ ██╗   ██╗')
    print('██║  ████╗ ████║    ██╔════╝██╔══██╗██║██╔══██╗██╔══██╗╚██╗ ██╔╝')
    print('██║  ██╔████╔██║    █████╗  ██████╔╝██║██║  ██║███████║ ╚████╔╝ ')
    print('██║  ██║╚██╔╝██║    ██╔══╝  ██╔══██╗██║██║  ██║██╔══██║  ╚██╔╝  ')
    print('██║  ██║ ╚═╝ ██║    ██║     ██║  ██║██║██████╔╝██║  ██║   ██║   ')
    print('╚═╝  ╚═╝     ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ')
    print("\n")  

# ======================================================================================================


# ================================Music Scanner=========================================================

def recur(folder_path,folder_count):
    p=Path(folder_path)
    dirs=p.glob("*")
    print(dirs)
   
    for folder in dirs:
        print(folder)
        if folder.is_dir():
            recur(folder,folder_count)
            folder_count+=1
        else:
            musiclist.append(folder)



def scanmusic(folderpath):
    folder_count=0
    recur(folderpath,folder_count)
    np.save('musiclist',musiclist)
    
# =========================================================================================================



#========================== recognizer function =================================================
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        recognizer.pause_threshold =  1

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
        response["transcription"]=False
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
        response["transcription"]=False


    return response

#========================== recognizer function  Ends=============================================


# #================================ Speak function =================================================

def speak(text):
    tts = gTTS(text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3 --stereo 2>/dev/null;")

# #========================== Speak function ends =================================================

                                                        


#========================== Main function  ============================================================
if __name__ == "__main__":

    # initialization and configurations
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    username = getpass.getuser()
    username=username.replace("-","")
    currentDT = datetime.datetime.now()
    # configuration reading
    with open('config.json') as json_file:
        configdata = json.load(json_file)
    pyowm_key=configdata['pyowm']['key']
    location=configdata['pyowm']['location']
    unit=configdata['pyowm']['tempreture_unit']
    lng=configdata['pyowm']['lng']
    lat=configdata['pyowm']['lat']
    music_folder=configdata['music_folder_path']
    if len(music_folder)>0:
        print("Scanning Music.....")
        scanmusic(music_folder)
        music_list=np.load("musiclist.npy", allow_pickle=True)
        musicfile=random.choice(music_list)
    else:
        musicfile=""


    while True:
        banner()
        print("Friday: listening...")
        guess = recognize_speech_from_mic(recognizer, microphone)
        print("You: "+str(guess["transcription"]))
        if guess["success"]:
             if not guess['transcription']:
                    pass
             else:
                 if guess["transcription"].lower() == "goodbye":
                     print("Friday: Goodbye Sir!")
                     speak('Goodbye Sir!')
                     break
                 else:
                     command=guess['transcription']
                     if command in greetings:
                         random_greeting = random.choice(greetings)
                         print("Friday: "+str(random_greeting))
                         speak(random_greeting)
                       
                     elif command in question:
                         speak('I am fine')
                         print("Friday: I am fine")
                     elif command in var1:
                         speak('I was made by D-eviloper')
                         reply = random.choice(var2)
                         print("Friday: "+str(reply))
                     elif command in cmd9:
                         print("Friday: "+str(random.choice(repfr9)))
                         speak(random.choice(repfr9))
                     elif command in cmd7:
                         print("Friday: "+str(random.choice(colrep)))
                         speak(random.choice(colrep))
                         print("Friday: It keeps changing every micro second")
                         speak('It keeps changing every micro second')
                     elif command in cmd8:
                         print("Friday: "+str(random.choice(colrep)))
                         speak(random.choice(colrep))
                         print("Friday: It keeps changing every micro second")
                         speak('It keeps changing every micro second')
                     elif command in cmd2:
                         if musicfile!="":
                             webbrowser.open('file://'+str(musicfile))
                         else:
                             print('Friday: Music Path Not Configured')
                             speak('Music Path Not Configured')
                     elif command in var4:
                         speak("Friday: I am Friday, a Bot")
                     elif command in cmd4:
                         print("Friday: Opening Youtube")
                         speak('Opening Youtube')
                         webbrowser.open('https://www.youtube.com')
                     elif command in cmd6:
                         print('Friday: see you later')
                         speak('see you later')
                         exit()
                     elif command in cmd5:
                         owm = pyowm.OWM(pyowm_key)
                         observation = owm.weather_at_place(location)
                         observation_list = owm.weather_around_coords(float(lat),float(lng))
                         w = observation.get_weather()
                         wind=w.get_wind()
                         humidity=w.get_humidity()
                         temprature=w.get_temperature(unit=unit)
                         status=w.get_detailed_status() 
                         print("Friday: Today's Weather status is "+status )
                         print("Friday: Wind Speed is "+str(wind['speed']))
                         print('Friday: humidity is '+str(humidity)+"%")
                         print('Friday: Temprature is '+str(temprature['temp'])+" Degree celsius")
                         speak("Today's Weather status is "+str(status)+",Wind Speed is "+str(wind['speed'])+",humidity is "+str(humidity)+"%,and Temprature is "+str(temprature['temp'])+" Degree celsius" )
                     elif command in var3:
                         print("Friday: "+str(currentDT.strftime("The time is %H:%M")))
                         speak(currentDT.strftime("The time is %H:%M"))
                     elif command in cmd1:
                         print("Friday: Opening Google")
                         speak('Opening Google')
                         webbrowser.open('https://www.google.com')
                     elif command in cmd3:
                         jokrep = random.choice(jokes)
                         speak(jokrep)
                     else:
                         print("Friday: Do Want to Search the Internet about "+str(command)+"?")
                         speak("Do Want to Search the Internet about "+command+"?")
                         speak("Press y for Yes and n for No")
                         userInput2 = input("Friday: Press y for Yes and n for No : ")
                         
                         if userInput2.lower()=="y":
                             print("Friday: "+str(wikipedia.summary(command)))
                             speak("According to Wikipedia I found this. Do you want me to read?")
                             userInput4 = input("Friday: Do you want me to read? (y/n): ")
                             if userInput4.lower()=="y":
                                 speak(wikipedia.summary(command))
                             else:
                                 print("Friday: Okay! ")
                                 speak('Okay!')
                                 pass
                             speak("Do you want to search in google? Press y for Yes and n for No")
                             userInput3 = input("Friday: Do you want to search in google? (y/n): ")
                             if userInput3.lower()=="y":
                                 webbrowser.open_new('https://www.google.com/search?q=' + command)
                             else:
                                 print('Friday: Okay! Try Something Else')
                                 speak('Okay! Try Something Else')
                                 pass
                         else:
                             print('Friday: Okay! Try Something Else')
                             speak('Okay! Try Something Else')
                             pass
                            
                         
#========================== Main function ends ============================================================





