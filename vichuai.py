import smtplib
import os
import sys
import json
import subprocess
import socket
import webbrowser
import threading
import time
import traceback
from datetime import datetime
from email.message import EmailMessage

import speech_recognition as sr
import pyautogui
import psutil
import pytesseract
from gtts import gTTS
import playsound
from PIL import ImageGrab, Image
from pynput import mouse as pyn_mouse, keyboard as pyn_keyboard

# ================= CONFIGURATION =================
pyautogui.FAILSAFE = False

# File paths
APPOINTMENTS_FILE = "appointments.txt"
PAYMENT_FILE = "payments.txt"
ERROR_LOG = "system_errors.log"
DEFAULT_RECEIVER = "balajigpro121@gmail.com"

# Email credentials (should be set as environment variables)
EMAIL_SENDER = os.getenv("JULI_EMAIL")
EMAIL_PASSWORD = os.getenv("JULI_EMAIL_PASS")

# Macro variables
macro_events = []
macro_start_time = 0
MACRO_STOP = False

# Key mapping for macro playback
KEY_MAP = {
    "Key.enter": "enter",
    "Key.space": "space",
    "Key.backspace": "backspace",
    "Key.tab": "tab",
    "Key.esc": "esc",
    "Key.shift": "shift",
    "Key.shift_r": "shift",
    "Key.ctrl": "ctrl",
    "Key.ctrl_l": "ctrl",
    "Key.ctrl_r": "ctrl",
    "Key.alt": "alt",
    "Key.alt_l": "alt",
    "Key.alt_r": "alt",
}

# ================= TEXT-TO-SPEECH FUNCTIONS =================

def speak(text):
    """Convert text to speech."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        filename = "temp.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Speech error: {e}")

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

# ================= EMAIL FUNCTIONS =================

def draft_email_with_deepseek(prompt_text):
    system_prompt = (
        "Write ONLY the email body.\n"
        "No thinking.\n"
        "No explanation.\n"
        "No subject.\n"
        "Plain text.\n"
        "5 to 8 lines."
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-r1:7b"],
            input=system_prompt + "\n\n" + prompt_text,
            text=True,
            capture_output=True,
            check=True
        )

        body = result.stdout.strip()

        # Remove leaked reasoning if any
        for tag in ["<think>", "</think>", "```"]:
            body = body.replace(tag, "")

        return body.strip()

    except Exception as e:
        print("DeepSeek error:", e)
        speak("Failed to draft email.")
        return ""

def send_email(sender, password, to_email, subject, body):
    try:
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)

        print("✅ EMAIL SENT SUCCESSFULLY")
        speak("Mail sent successfully.")
        return True

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
        speak("Email failed. Check terminal for error.")
        return False

def send_mail(prompt_text):
    """
    Drafts an email using DeepSeek, auto-generates subject,
    and sends it to the default receiver.
    """
    if not prompt_text or not prompt_text.strip():
        print("❌ No mail content provided")
        return False

    sender = EMAIL_SENDER
    password = EMAIL_PASSWORD

    if not sender or not password:
        print("❌ JULI_EMAIL or JULI_EMAIL_PASS not set")
        return False

    # Generate subject
    subject = prompt_text.strip().capitalize()
    if len(subject) > 60:
        subject = subject[:57] + "..."

    # Draft body with DeepSeek
    body = draft_email_with_deepseek(prompt_text)
    if not body:
        return False

    # Send email
    return send_email(sender, password, DEFAULT_RECEIVER, subject, body)

# ================= APPOINTMENT & PAYMENT FUNCTIONS =================

def record_appointment():
    speak("Let's record an appointment.")

    date = input("Enter appointment date (YYYY-MM-DD): ").strip()
    speak("What is the date?")

    time_val = input("Enter appointment time (HH:MM): ").strip()
    speak("What is the time?")

    content = input("Enter appointment content: ").strip()
    speak("What is the appointment about?")

    entry = f"{date} | {time_val} | {content}\n"

    with open(APPOINTMENTS_FILE, "a") as f:
        f.write(entry)

    speak("Appointment recorded successfully.")
    print("Saved:", entry)

def create_payment_request():
    amount = input("Enter amount: ")
    purpose = input("Purpose: ")

    entry = f"{datetime.now()} | {amount} | {purpose}\n"

    with open(PAYMENT_FILE, "a") as f:
        f.write(entry)

    speak(f"Payment request recorded for {amount}")

def bus_ticket_request():
    frm = input("From city: ")
    to = input("To city: ")
    date = input("Travel date: ")

    entry = f"{datetime.now()} | {frm}->{to} | {date}\n"

    with open("bus_requests.txt", "a") as f:
        f.write(entry)

    speak("Bus ticket request saved. Ready for API processing.")

def create_support_request():
    """Create a support/grievance request."""
    issue = input("Please describe your issue: ")
    priority = input("Priority (High/Medium/Low): ")

    entry = f"{datetime.now()} | Priority: {priority} | {issue}\n"

    with open("support_requests.txt", "a") as f:
        f.write(entry)

    speak("Support request has been recorded. We'll get back to you soon.")

# ================= CODE GENERATION & AI FUNCTIONS =================

def extract_code_only(text):
    """
    Extract ONLY the text between the first pair of triple backticks.
    Returns empty string if not found.
    """
    start = text.find("```")
    if start == -1:
        return ""

    end = text.find("```", start + 3)
    if end == -1:
        return ""

    block = text[start + 3:end].strip()

    # Remove optional language tag (e.g. python)
    lines = block.splitlines()
    if lines and lines[0].strip().isalpha():
        lines = lines[1:]

    return "\n".join(lines).strip()

def run_ollama_and_generate_code(prompt):
    system_prompt = (
        "You are a code generator.\n"
        "Generate ONLY valid Python code.\n"
        "Put the code inside triple backticks.\n"
        "No explanations.\n"
        "Output code only."
    )

    full_prompt = f"{system_prompt}\n\n{prompt}"

    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-r1:7b"],
            input=full_prompt,
            text=True,
            capture_output=True,
            check=True
        )

        raw_output = result.stdout
        code = extract_code_only(raw_output)

        if not code:
            speak("No code was generated.")
            return

        filename = "generated_code.py"
        with open(filename, "w") as f:
            f.write(code)

        speak("Code generated. Opening new terminal and running it.")

        subprocess.Popen([
            "gnome-terminal",
            "--",
            "bash",
            "-c",
            f"python3 {filename}; echo; echo '--- Program finished ---'; exec bash"
        ])

    except Exception as e:
        print("Error:", e)
        speak("Failed to run the generated code.")

def ask_model_text(prompt):
    system_prompt = (
        "You are a helpful assistant. "
        "Answer clearly and directly."
    )

    full_prompt = f"{system_prompt}\n\n{prompt}"

    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-r1:7b"],
            input=full_prompt,
            text=True,
            capture_output=True
        )

        answer = result.stdout.strip()
        print("\nModel Answer:\n", answer)
        speak(answer[:500])  # avoid overly long speech
        return answer

    except Exception as e:
        print("Model error:", e)
        speak("I could not get an answer from the model.")
        return ""

def emotional_response(user_text, mode="emotional"):
    """
    Generate ONLY emotional output (no thinking, no explanation).
    """
    system_prompt = f"""
You are Juli, an emotional assistant.

Mode: {mode}

STRICT RULES:
- Output ONLY the final emotional response
- No reasoning
- No analysis
- No explanation
- No bullet points
- Speak like a caring human
- 3 to 5 sentences max
"""

    full_prompt = f"""
User says:
"{user_text}"

Respond emotionally.
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-r1:7b"],
            input=system_prompt + "\n\n" + full_prompt,
            text=True,
            capture_output=True
        )

        response = result.stdout.strip()

        # HARD SAFETY: remove any thinking if model leaks it
        for tag in ["<think>", "</think>", "THINKING:", "Analysis:", "Reasoning:"]:
            response = response.replace(tag, "")

        response = response.strip()

        print("\n💙 Juli:\n", response)
        speak(response[:500])
        return response

    except Exception as e:
        speak("I am here with you. You are not alone.")
        return ""

# ================= SCREEN & TEXT FUNCTIONS =================

def read_screen_text():
    """
    GNOME Wayland screen capture using xdg-desktop-portal (correct DBus API)
    """
    try:
        # Call the Screenshot portal (this shows permission popup)
        subprocess.run([
            "gdbus", "call",
            "--session",
            "--dest", "org.freedesktop.portal.Desktop",
            "--object-path", "/org/freedesktop/portal/desktop",
            "--method", "org.freedesktop.portal.Screenshot.Screenshot",
            "",
            "{}"
        ], check=True)

        # Portal saves screenshots in ~/Pictures
        pictures_dir = os.path.expanduser("~/Pictures")

        screenshots = sorted(
            [
                os.path.join(pictures_dir, f)
                for f in os.listdir(pictures_dir)
                if f.lower().startswith("screenshot")
            ],
            key=os.path.getmtime,
            reverse=True
        )

        if not screenshots:
            raise RuntimeError("No screenshot found")

        latest = screenshots[0]

        text = pytesseract.image_to_string(Image.open(latest))
        return text.strip()

    except Exception as e:
        print("Screen read error:", e)
        speak("GNOME blocked the screenshot. Permission is required.")
        return ""

def summarize_screen_with_deepseek(screen_text):
    """Summarize screen text using DeepSeek."""
    if not screen_text:
        speak("I couldn't read any text from the screen.")
        return ""

    prompt = f"Summarize this screen text in 2-3 sentences:\n\n{screen_text}"
    summary = ask_model_text(prompt)
    return summary

def read_and_explain_screen():
    speak("Reading the screen.")
    screen_text = read_screen_text()
    summarize_screen_with_deepseek(screen_text)

# ================= FILE & SYSTEM FUNCTIONS =================

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

def monitor_system():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    return cpu, mem

def log_error(err):
    with open(ERROR_LOG, "a") as f:
        f.write("\n==== ERROR ====\n")
        f.write(str(datetime.now()) + "\n")
        f.write(str(err) + "\n")
        f.write(traceback.format_exc())
        f.write("\n")

def analyze_error_log():
    if not os.path.exists(ERROR_LOG):
        speak("No error log found.")
        return

    with open(ERROR_LOG) as f:
        data = f.read()[-4000:]

    ask_model_text("Analyze these system errors and explain simply:\n" + data)

# ================= SECURITY & NETWORK FUNCTIONS =================

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
    camphish_command = "camphish"
    try:
        if os.name == 'posix':  # Linux, macOS
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', camphish_command])
            speak("CamPhish is now running.")
        elif os.name == 'nt':  # Windows
            speak("This script is not supported on Windows.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't open CamPhish.")

# ================= EDUCATION & GUIDANCE FUNCTIONS =================

def education_guidance():
    """
    Provide education / studies / career guidance using DeepSeek.
    """
    speak("Let's plan your education.")

    level = input("Enter your current class or degree (e.g. 10th, 12th, B.Tech, Diploma): ").strip()
    interest = input("Enter your interests or stream (e.g. science, computers, commerce): ").strip()
    goal = input("Enter your career goal (optional, press Enter to skip): ").strip()

    prompt = f"""
You are an expert education and career guidance counselor.

Student details:
- Current level: {level}
- Interests: {interest}
- Career goal: {goal if goal else "Not decided"}

Give:
1. Best subjects to focus on
2. Study roadmap (short-term + long-term)
3. Free and paid learning resources
4. Career options after this path
5. Practical advice in simple language
"""

    speak("Analyzing your education path.")
    answer = ask_model_text(prompt)
    return answer

def handle_health_query(command):
    query = command.replace("health", "").strip()

    if not query:
        speak("Please ask your health question.")
        return

    speak("Checking health information.")
    ask_model_text(f"Health question: {query}")

# ================= MEDIA & ENTERTAINMENT FUNCTIONS =================

def play_song_in_new_terminal(song_name):
    """
    Open a new terminal and play a song using mpv with YouTube search.
    """
    if not song_name:
        print("No song name provided.")
        speak("Please tell me the song name.")
        return

    # Clean up the song name
    song_name = song_name.strip()

    # Create the mpv command with YouTube search
    mpv_command = f'mpv "ytdl://ytsearch:{song_name}"'

    # Alternative: Play in background and show player controls
    full_command = f'{mpv_command} || echo "Failed to play song. Make sure mpv is installed."; echo "Press Enter to close..."; read'

    try:
        if os.name == 'posix':  # Linux/MacOS
            # Open new terminal with mpv player
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', full_command])
            print(f"Playing '{song_name}' using mpv...")
            speak(f"Playing {song_name}")
        elif os.name == 'nt':  # Windows
            # For Windows, use different approach
            windows_command = f'start cmd /K "echo Playing {song_name}... && mpv "ytdl://ytsearch:{song_name}""'
            subprocess.Popen(windows_command, shell=True)
            speak(f"Playing {song_name}")
    except Exception as e:
        print(f"Error opening terminal: {e}")
        speak(f"I couldn't play {song_name}. Make sure mpv is installed.")

        # Provide installation instructions
        if os.name == 'posix':
            print("\nTo install mpv on Ubuntu/Debian:")
            print("sudo apt-get install mpv youtube-dl")
            print("\nOn Arch Linux:")
            print("sudo pacman -S mpv youtube-dl")

# ================= MACRO FUNCTIONS =================

def macro_record(filename):
    global macro_events, macro_start_time
    macro_events = []
    macro_start_time = time.time()

    speak("Macro recording started. Press escape to stop.")

    def on_move(x, y):
        macro_events.append({
            "type": "move",
            "x": x,
            "y": y,
            "time": time.time() - macro_start_time
        })

    def on_click(x, y, button, pressed):
        macro_events.append({
            "type": "click",
            "x": x,
            "y": y,
            "pressed": pressed,
            "time": time.time() - macro_start_time
        })

    def on_press(key):
        macro_events.append({
            "type": "key",
            "key": str(key),
            "pressed": True,
            "time": time.time() - macro_start_time
        })

    def on_release(key):
        macro_events.append({
            "type": "key",
            "key": str(key),
            "pressed": False,
            "time": time.time() - macro_start_time
        })
        if key == pyn_keyboard.Key.esc:
            return False

    mouse_listener = pyn_mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = pyn_keyboard.Listener(on_press=on_press, on_release=on_release)

    mouse_listener.start()
    keyboard_listener.start()
    keyboard_listener.join()
    mouse_listener.stop()

    with open(filename, "w") as f:
        json.dump(macro_events, f, indent=2)

    speak("Macro saved.")
    print("Macro saved:", filename)

def macro_stop_listener(key):
    global MACRO_STOP
    if key == pyn_keyboard.Key.f8:
        MACRO_STOP = True
        return False

def macro_play(filename):
    global MACRO_STOP
    MACRO_STOP = False

    if not os.path.exists(filename):
        speak("Macro file not found.")
        return

    with open(filename) as f:
        actions = json.load(f)

    speak("Replaying macro in three seconds.")
    time.sleep(3)

    listener = pyn_keyboard.Listener(on_press=macro_stop_listener)
    listener.start()

    last = 0

    for a in actions:
        if MACRO_STOP:
            break

        time.sleep(max(0, a["time"] - last))
        last = a["time"]

        if a["type"] == "move":
            pyautogui.moveTo(a["x"], a["y"])

        elif a["type"] == "click":
            if a["pressed"]:
                pyautogui.mouseDown(a["x"], a["y"])
            else:
                pyautogui.mouseUp(a["x"], a["y"])

        elif a["type"] == "key":
            raw_key = a["key"]

            # Normal character (a, b, 1, etc.)
            if raw_key.startswith("'") and raw_key.endswith("'"):
                char = raw_key.strip("'")
                if a["pressed"]:
                    pyautogui.write(char)

            else:
                key = KEY_MAP.get(raw_key)

                if not key:
                    return  # ignore unsupported keys safely

                if a["pressed"]:
                    pyautogui.keyDown(key)
                else:
                    pyautogui.keyUp(key)

    listener.stop()
    speak("Macro replay finished.")

# ================= UTILITY FUNCTIONS =================

def mouse():
    """Open hand mouse control."""
    mouse = "python3 hand-mouse.py"
    try:
        if os.name == 'posix':  # Linux, macOS
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', mouse])
            speak("Mouse control is now running.")
        elif os.name == 'nt':  # Windows
            speak("This script is not supported on Windows.")
    except Exception as e:
        print(f"Error: {e}")
        speak("I couldn't open mouse control.")

def perform_search(search_term):
    """Open Firefox and search for the given term."""
    url = f"https://www.google.com/search?q={search_term}"
    try:
        webbrowser.get('firefox').open(url)
        speak(f"Searching for {search_term} in Firefox.")
    except:
        webbrowser.open(url)
        speak(f"Searching for {search_term} in default browser.")

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

# ================= SCHEDULER FUNCTIONS =================

def background_watchdog():
    while True:
        monitor_system()
        time.sleep(60)

def add_interval_job(name, func, seconds):
    """Add a job to run at intervals."""
    threading.Thread(target=lambda: run_interval_job(func, seconds), daemon=True).start()

def add_cron_job(name, func, hour, minute):
    """Add a cron-like job (simplified version)."""
    threading.Thread(target=lambda: run_cron_job(func, hour, minute), daemon=True).start()

def run_interval_job(func, seconds):
    """Run a function at regular intervals."""
    while True:
        func()
        time.sleep(seconds)

def run_cron_job(func, hour, minute):
    """Run a function at a specific time daily (simplified)."""
    while True:
        now = datetime.now()
        if now.hour == hour and now.minute == minute:
            func()
            time.sleep(60)  # Sleep for a minute to avoid multiple executions
        time.sleep(30)

# ================= BROWSER AGENT =================

class BrowserAgent:
    """Simple browser agent for web operations."""
    def search_google(self, query):
        """Search Google with the given query."""
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Searching for {query} on Google.")

browser_agent = BrowserAgent()

# ================= PLUGIN SYSTEM =================

def load_plugins():
    """Load plugin modules (placeholder)."""
    return []

def dispatch(command, plugins):
    """Dispatch command to plugins."""
    for p in plugins:
        if hasattr(p, 'commands'):
            for key in p.commands():
                if key in command:
                    p.handle(command)
                    return True
    return False

def safe_run(func, *args):
    try:
        return func(*args)
    except Exception as e:
        log_error(e)
        speak("An error occurred. I logged it.")
        return None

# ================= MAIN ACTION HANDLER =================

def perform_action(command):
    """Perform actions based on user commands."""
    # Try plugin dispatch first
    plugins = load_plugins()
    if dispatch(command, plugins):
        return

    # Check if "juli" is in command
    if "juli" in command:
        command = command.replace("juli", "").strip()

        if "date" in command:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = f"The current date and time is {current_date}"
            print(response)
            speak(response)
        elif "analyze errors" in command:
            analyze_error_log()
        elif "payment" in command:
            create_payment_request()
        elif "bus ticket" in command:
            bus_ticket_request()
        elif "system status" in command:
            cpu, mem = monitor_system()
            speak(f"CPU usage is {cpu} percent. Memory usage is {mem} percent.")
        elif "list files" in command:
            list_files()
        elif "open directory" in command:
            open_directory()
        elif "search" in command:
            # Extract the search term from the command
            search_term = command.replace("search", "").strip()
            if search_term:
                perform_search(search_term)
            else:
                speak("Please provide a search term.")
        elif "ma " in command:
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
        elif "mail" in command or "send email" in command:
            send_mail(command)
        elif command.startswith("code "):
            code_prompt = command.replace("code ", "").strip()
            if not code_prompt:
                speak("Tell me what code to run.")
            else:
                run_ollama_and_generate_code(code_prompt)
        elif "read screen" in command or "what's on screen" in command:
            read_and_explain_screen()
        elif "smile" in command or "emotional" in command or "comfort" in command or "motivate" in command:
            if "smile" in command:
                mode = "cheerful"
                text = command.replace("smile", "").strip()
            elif "comfort" in command:
                mode = "comforting"
                text = command.replace("comfort", "").strip()
            elif "motivate" in command:
                mode = "motivational"
                text = command.replace("motivate", "").strip()
            else:
                mode = "emotional"
                text = command

            emotional_response(text, mode)
        elif "record macro" in command:
            name = command.replace("record macro", "").strip() or "macro.json"
            safe_run(macro_record, name)
        elif "play macro" in command:
            name = command.replace("play macro", "").strip() or "macro.json"
            safe_run(macro_play, name)
        elif "rec appointment" in command:
            record_appointment()
        elif "health" in command:
            handle_health_query(command)
        elif "support" in command or "grievance" in command:
            create_support_request()
        elif "song" in command:
            # Extract song name and play
            song_name = command.replace("song", "").strip()
            play_song_in_new_terminal(song_name)
        elif "education" in command or "studies" in command or "career guidance" in command:
            education_guidance()
        elif "mouse" in command:
            mouse()
        elif "camphish" in command:
            open_camphish()
        elif "listener" in command:
            start_listener()
        elif "browser search" in command:
            q = command.replace("browser search", "").strip()
            browser_agent.search_google(q)
        elif "close" in command:
            close_current_window()
        else:
            speak("I didn't understand that command. Please try again.")
    else:
        speak("Please say 'juli' before your command.")

# ================= MAIN FUNCTION =================

def main():
    """Main function to choose between voice or command-line mode."""
    speak("Welcome! Would you like to use voice commands or the command line?")
    print("Choose mode:\n1. Voice Commands\n2. Command Line")

    mode = input("Enter your choice (1 for Voice, 2 for Command Line): ").strip()

    # Start background monitoring
    threading.Thread(target=background_watchdog, daemon=True).start()

    # Add scheduled jobs
    add_interval_job("system monitor", monitor_system, 60)
    add_cron_job("error analysis", analyze_error_log, 9, 0)

    if mode == "1":
        speak("You have selected voice commands. I am ready to listen.")
        while True:
            command = get_command()
            if command:
                perform_action(command)
    elif mode == "2":
        speak("You have selected command line mode. Please enter your commands.")
        while True:
            command = input("Enter your command: ").strip().lower()
            if command:
                perform_action(command)
    else:
        speak("Invalid choice. Please restart the program and choose a valid option.")
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
