import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
from dotenv import load_dotenv
import os
from newspaper import Article
from langchain.chat_models import ChatGooglePalm
from langchain.schema import HumanMessage
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import LEFT, BOTH, SUNKEN
from PIL import Image, ImageTk
from threading import Thread

load_dotenv()
chat = ChatGooglePalm(google_api_key=os.getenv("GOOGLE_API_KEY"))

# Constants for custom styling
BG_COLOR = "#D2C6E2"
BUTTON_COLOR = "#F9F4F2"
BUTTON_FONT = ("Arial", 14, "bold")
BUTTON_FOREGROUND = "black"
HEADING_FONT = ("white", 24, "bold")
INSTRUCTION_FONT = ("Helvetica", 14)


# this method is for taking the commands
# and recognizing the command from the
# speech_Recognition module we will use
# the recongizer method for recognizing
def takeCommand():
    r = sr.Recognizer()

    # from the speech_Recognition module
    # we will use the Microphone module
    # for listening the command
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

            # for Listening the command in indian
            # english we can also use 'hi-In'
            # for hindi recognizing
            Query = r.recognize_google(audio, language="en-in")
            print("the command is printed=", Query)

        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"

        return Query


def speak(audio):
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty("voices")

    # setter method .[0]=male voice and
    # [1]=female voice in set Property.
    engine.setProperty("voice", voices[0].id)

    # Method for the speaking of the assistant
    engine.say(audio)

    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()


entry = None
stop_flag = False  # Define the stop_flag variable at the top of the script


def tellDay():
    # This function is for telling the
    # day of the week
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
    # nd then after slicing we can get time
    print(time)
    hour = time[11:13]
    min = time[14:16]
    speak("The time is sir" + hour + "Hours and" + min + "Minutes")


def articleNarration():
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    article_url = "https://www.gadgets360.com/news"
    print("\n")

    session = requests.Session()

    try:
        response = session.get(article_url, headers=headers, timeout=10)

        if response.status_code == 200:
            article = Article(article_url)
            article.download()
            article.parse()

            print(f"Title: {article.title}")
            # print(f"Text: {article.text}")

        else:
            print(f"Failed to fetch article at {article_url}")

    except Exception as e:
        print(f"Error occured while fetching article at {article_url}: {e}")

    article_title = article.title
    article_text = article.text

    template = """You are a very good assistant that summarizes online articles.

    Here's the article you want to summarize.

    ==================
    Title: {article_title}

    {article_text}
    ==================

    Now, provide a summarized version of the article in a bulleted list format.
    """

    prompt = template.format(article_title=article.title, article_text=article.text)

    messages = [HumanMessage(content=prompt)]
    summary = chat(messages)
    sum_content = summary.content
    print(sum_content.replace("*", ""))
    speak(summary.content)


def Hello():
    # This function is for when the assistant
    # is called it will say hello and then
    # take query
    speak("hello sir I am your desktop assistant. Tell me how may I help you")


def Take_query():
    # calling the Hello function for
    # making it more interactive
    Hello()
    global stop_flag

    # This loop is infinite as it will take
    # our queries continuously until and unless
    # we do not say bye to exit or terminate
    # the program
    # while True:
    while not stop_flag:
        # taking the query and making it into
        # lower case so that most of the times
        # query matches and we get the perfect
        # output
        query = takeCommand().lower()

        if "open google" in query:
            speak("Opening Google ")
            webbrowser.open("www.google.com")
            continue

        elif "show me some videos" in query:
            speak("Opening videos")
            webbrowser.open("www.youtube.com/@MrBeast")
            continue

        elif "I want to read some tech news" in query:
            speak("Opening news")
            webbrowser.open("https://www.gadgets360.com/news")
            continue

        elif "coffee shop near me" in query:
            speak("These are the coffee shop near you.")
            webbrowser.open("https://www.google.com/maps/search/coffee+shop+near+me")
            continue

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("user asked to locate")
            speak(location)
            webbrowser.open(
                "https://www.google.nl/maps/search/" + location.replace(" ", "+")
            )
            continue

        elif "which day is today" in query:
            tellDay()
            continue

        elif "tell me the time" in query:
            tellTime()
            continue

        elif "from wikipedia" in query:
            # if any one wants to have a information
            # from wikipedia
            speak("Checking the wikipedia ")
            query = query.replace("wikipedia", "")

            # it will give the summary of 4 lines from
            # wikipedia we can increase and decrease
            # it also.
            result = wikipedia.summary(query, sentences=4)
            speak("According to wikipedia")
            print(result)
            speak(result)

        elif "tell me your name" in query:
            speak("I am Jarvis. Your desktop Assistant")

        elif "today's tech news" in query:
            articleNarration()
            continue

        # this will exit and terminate the program
        elif "go back to sleep" in query:
            speak("Bye Sir")
            exit()


def stop_voice_assistant():
    global stop_flag
    speak("Stopping the Voice Assistant.")
    stop_flag = True


def start_voice_assistant():
    global stop_flag
    Take_query()
    stop_flag = False  # Reset the flag to False when starting the voice assistant


def main():
    # Create the main GUI window
    root = tk.Tk()
    root.resizable(True, True)
    root.title("Voice Assistant")
    root.geometry("500x700")
    root.configure(bg=BG_COLOR)

    def on_button_click():
        global stop_flag
        if not stop_flag:
            stop_flag = (
                False  # Reset the flag to False when starting the voice assistant
            )
            Thread(target=start_voice_assistant).start()
        else:
            stop_voice_assistant()

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        label.config(image = photo)
        label.image = photo #avoid garbage collection

    # Load and set the background image
    background_image = Image.open("/home/angkul/Desktop/JarvisAI/3425171.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = ttk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    f1 = ttk.Frame(root)
    f1.pack(pady=100)  # Add some padding to the frame to center it vertically

    # Heading
    heading_label = ttk.Label(
        root, text="Voice Assistant", font=HEADING_FONT, background=BG_COLOR
    )
    heading_label.pack(pady=20)

    global entry
    f1 = ttk.Frame(root)
    f1.pack()
    entry = ttk.Entry(f1, width=30)
    entry.pack(pady=10)

    # Instruction
    instruction_label = ttk.Label(
        root,
        text="Click the button below to start the Voice Assistant.",
        font=INSTRUCTION_FONT,
        background=BG_COLOR,
    )
    instruction_label.pack(pady=10)

    # Create and place a button on the GUI
    button = ttk.Button(
        root,
        text="Start Voice Assistant",
        command=on_button_click,
        style="VoiceAssistant.TButton",
    )
    button.pack(pady=20)

    # Style the button
    style = ttk.Style(root)
    style.configure(
        "VoiceAssistant.TButton",
        font=BUTTON_FONT,
        background=BUTTON_COLOR,
        foreground=BUTTON_FOREGROUND,
    )

    # Run the GUI main loop
    root.mainloop()


if __name__ == "__main__":
    # main method for executing
    # the functions
    main()
