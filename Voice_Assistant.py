import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyscreenshot as ps


# this method is for taking the commands
# and recognizing the command from the speech_Recognition module we will use the recongizer method for recognizing
def takeCommand():
    r = sr.Recognizer()

    # from the speech_Recognition module we will use the Microphone module for listening the command
    with sr.Microphone() as source:
        print("Listening")

        # seconds of non-speaking audio before
        # a phrase is considered complete
        r.pause_threshold = 0.7
        audio = r.listen(source)

        # Now we will be using the try and catch
        # method so that if sound is recognized
        # it is good else we will have exception
        # handling
        try:
            print("Recognizing")

            Query = r.recognize_google(audio, language="en-in")
            print("the command is printed=", Query)

        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"

        return Query


def speak(audio):
    engine = pyttsx3.init()
    # getter method(gets the current value of engine property)
    voices = engine.getProperty("voices")

    # setter method .[0]=male voice and
    # [1]=female voice in set Property.
    engine.setProperty("voice", voices[0].id)

    # Method for the speaking of the assistant
    engine.say(audio)

    # Blocks while processing all the currently queued commands
    engine.runAndWait()


def tellDay():
    # This function is for telling the day of the week
    day = datetime.datetime.today().weekday() + 1

    # this line tells us about the number
    # that will help us in telling the day
    Day_dict = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday",
    }

    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)


def tellTime():
    # This method will give the time
    time = str(datetime.datetime.now())

    # the time will be displayed like
    # this "2020-06-05 17:50:14.582630"
    # And then after slicing we can get time
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak("The time is sir" + hour + "Hours and" + min + "Minutes")


def Hello():
    # This function is for when the assistant is called it will say hello and then take query
    speak("hello sir I am your desktop assistant tell me how may I help you")


def Take_query():
    # calling the Hello function for making it more interactive
    Hello()

    # This loop is infinite as it will take our queries continuously until and unless we do not say bye to exit or terminate the program
    while True:
        # taking the query and making it into lower case so that most of the times query matches and we get the perfect output
        query = takeCommand().lower()

        if "open google" in query:
            speak("Opening Google ")
            webbrowser.open("www.google.com")
            continue

        elif "which day it is" in query:
            tellDay()
            continue

        elif "tell me the time" in query:
            tellTime()
            continue

        elif "tell me your name" in query:
            speak("I am Jarvis. Your desktop Assistant")

        elif "take screenshot" in query:
            speak("Taking a screenshot")
            im = ps.grab()
            im.save("fullscreen.png")

        # this will exit and terminate the program
        elif "go back to sleep" in query:
            speak("Bye")
            exit()


if __name__ == "__main__":
    # main method for executing the functions
    Take_query()
