import os
import subprocess
import socket  # For TCP connection
import webbrowser  # For opening URLs in a web browser
from datetime import datetime
from gtts import gTTS
import playsound
import speech_recognition as sr  # For voice recognition

def speak(text):
    """Convert text to speech."""
    tts = gTTS(text=text, lang='en', slow=False)
    filename = "temp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_command():
    """Capture voice input and convert it to lowercase text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("There was an error with the voice service.")
        return ""

def run_local_gpt(command):
    """Run the local GPT model and return the response."""
    try:
        result = subprocess.run(['tgpt', command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        speak("There was an error executing the command.")
        print(f"Error: {e}")
        return ""

def list_files():
    """List files in the current directory."""
    try:
        files = os.listdir('.')
        response = "Here are the files in the current directory:"
        print(response)
        speak(response)
        for file in files:
            print(file)
            speak(file)
    except Exception as e:
        response = "I couldn't access the files."
        print(f"Error: {e}")
        speak(response)

def open_directory():
    """Open the current directory."""
    speak("Opening the current directory.")
    try:
        if os.name == 'posix':  # Linux, macOS
            subprocess.call(['xdg-open', '.'])
        elif os.name == 'nt':  # Windows
            subprocess.call(['start', '.'], shell=True)
    except Exception as e:
        response = "I couldn't open the directory."
        print(f"Error: {e}")
        speak(response)

def start_listener():
    """Start the listener with user-provided lhost and lport."""
    lhost = input("Please enter the local host (lhost): ")
    lport = int(input("Please enter the local port (lport): "))  # Port must be int

    listener_command = f"demon -lh {lhost} -lp {lport} -e hex"

    try:
        # Start listener in a new terminal
        if os.name == 'posix':  # Linux, macOS
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', listener_command])
        elif os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'cmd', '/K', listener_command], shell=True)
        speak(f"Listener started at {lhost}:{lport}")
    except Exception as e:
        response = "I couldn't start the listener."
        print(f"Error: {e}")
        speak(response)

    # Create a TCP socket server to detect incoming connections
    try:
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.bind((lhost, lport))
        tcp_server.listen(1)  # Allow 1 connection at a time
        print(f"Listening for incoming connections on {lhost}:{lport}...")

        # Wait for a connection
        conn, addr = tcp_server.accept()  # This blocks until a connection is made
        speak("A host got hacked.")
        speak(f"The IP of the host is {addr[0]}")
        print(f"Connection established from {addr[0]}")

        conn.close()  # Close the connection after the announcement
        tcp_server.close()  # Stop the server

    except Exception as e:
        print(f"Error setting up TCP listener: {e}")
        speak("There was an issue setting up the TCP listener.")

def open_camphish():
    """Open CamPhish in a new terminal."""
    camphish_command = "camphish"  # Command to run CamPhish
    try:
        if os.name == 'posix':  # Linux, macOS
            # Open CamPhish command in a new terminal
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', camphish_command])
            speak("CamPhish is now running.")
        elif os.name == 'nt':  # Windows
            speak("This script is not supported on Windows.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't open CamPhish.")

def play_song_in_new_terminal(song_name):
    """
    Open a new terminal and play a song using the ytfxf command.

    Args:
        song_name (str): Name of the song to play.
    """
    if not song_name:
        print("No song name provided.")
        return

    ytfxf_command = f"ytfzf -t \"{song_name}\""

    try:
        if os.name == 'posix':  # Linux/MacOS
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', ytfxf_command])
        elif os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'cmd', '/K', ytfxf_command], shell=True)
        print(f"Playing {song_name} now.")
    except Exception as e:
        print(f"Error opening terminal: {e}")

def mouse():
    """Open CamPhish in a new terminal."""
    mouse = "python3 hand-mouse.py"  # Command to run CamPhish
    try:
        if os.name == 'posix':  # Linux, macOS
            # Open CamPhish command in a new terminal
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', mouse ])
            speak("mouse is now running.")
        elif os.name == 'nt':  # Windows
            speak("This script is not supported on Windows.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't open mouse.")

def perform_search(search_term):
    """Open Firefox and search for the given term."""
    url = f"https://www.google.com/search?q={search_term}"
    webbrowser.get('firefox').open(url)
    speak(f"Searching for {search_term} in Firefox.")

def run_terminal_command(command):
    """Open a new terminal and run the specified command."""
    try:
        if os.name == 'posix':  # Linux
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command])
        elif os.name == 'nt':  # Windows
            subprocess.Popen(['start', 'cmd', '/K', command], shell=True)
        speak(f"Running command: {command} in a new terminal.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't run the command in a new terminal.")

def close_current_window():
    """Close the current terminal window."""
    speak("Closing the current window.")
    if os.name == 'posix':  # Linux
        os.system("xdotool getactivewindow windowclose")  # Ensure xdotool is installed
    elif os.name == 'nt':  # Windows
        os.system("taskkill /F /IM cmd.exe")  # Adjust as needed for your terminal

def perform_action(command):
    """Perform actions based on user commands."""
    if "juli" in command:
        command = command.replace("juli", "").strip()

        if "date" in command:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = f"The current date and time is {current_date}"
            print(response)
            speak(response)

        elif "list files" in command:
            list_files()

        elif "open" in command:
            open_directory()

        elif "search" in command:
            # Extract the search term from the command
            search_term = command.replace("search", "").strip()
            if search_term:
                perform_search(search_term)
            else:
                speak("Please provide a search term.")

        elif "ma" in command:
            # Extract the command after "ma"
            terminal_command = command.replace("ma", "").strip()
            if terminal_command:
                run_terminal_command(terminal_command)
            else:
                speak("Please provide a command to run.")

        elif "shutdown" in command:
            speak("Shutting down the system.")
            os.system("shutdown now")

        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            exit()

        elif "code" in command:
            response = run_local_gpt(command)
            if response:
                print(f"Here is the response: {response}")
                speak(response)

        elif "listener" in command:
            start_listener()

        elif "camphish" in command:
            open_camphish()

        elif "song" in command:
            # Extract song name and play
            song_name = command.replace("song", "").strip()
            play_song_in_new_terminal(song_name)

        elif "mouse" in command:
            mouse()
    else:
        speak("Please say 'juli' before your command.")


def main():
    """Main function to choose between voice or command-line mode."""
    speak("Welcome! Would you like to use voice commands or the command line?")
    print("Choose mode:\n1. Voice Commands\n2. Command Line")

    mode = input("Enter your choice (1 for Voice, 2 for Command Line): ").strip()

    if mode == "1":
        speak("You have selected voice commands. I am ready to listen.")
        while True:
            command = get_command()
            if command:
                perform_action(command)
    elif mode == "2":
        speak("You have selected command line mode. Please enter your commands.")
        while True:
            command = input("Enter your command: ").strip()
            if command:
                perform_action(command)
    else:
        speak("Invalid choice. Please restart the program and choose a valid option.")
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    while True:
        # Get the command from the user
        command = get_command()

        # If the command is empty or invalid, continue listening for valid input
        if command:
            perform_action(command)
        else:
            speak("I couldn't hear your command clearly, please try again.")
