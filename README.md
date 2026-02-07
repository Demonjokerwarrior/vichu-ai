# JULI — Intelligent Voice & Command Line Automation Assistant

JULI is a modular AI-powered automation assistant designed for **voice control, system automation, pentest lab workflows, productivity tasks, OCR screen reading, macro recording, and AI-driven responses**.

It integrates speech recognition, TTS, system automation, browser control, email drafting, pentest lab tooling, and AI model interaction (via Ollama + DeepSeek).

Built for developers, security learners, automation engineers, and AI experimenters.

---

# 🚀 Features

## 🎤 Voice + Command Mode

* Voice command recognition
* Command line interaction mode
* Natural command routing
* Spoken responses using TTS

## 🤖 AI Capabilities

* AI text answers
* AI emotional responses
* AI email drafting
* AI education guidance
* AI screen summarization
* AI error log analysis
* AI code generation & execution

## 🖥 System Automation

* File listing
* Directory opening
* Terminal command execution
* Browser search
* App launching
* Macro recording & playback
* Mouse & keyboard automation

## 📧 Email Automation

* AI-generated email body
* Gmail SMTP sending
* Subject auto-generation

## 🧠 OCR Screen Reader

* Wayland/GNOME compatible screenshot capture
* OCR via Tesseract
* AI summarization

## 🎵 Media

* Play songs via mpv + YouTube search
* Gesture mouse support
* Sign-to-text project launcher

## 🛠 Pentest Lab Toolkit (Lab Use Only)

* Nmap scanning
* Web enumeration
* Linux privilege enum
* Exploit search
* Metasploit launcher
* OWASP ZAP spider & active scan
* CTF workspace builder
* Scan analysis with AI

## 📅 Productivity

* Appointment recorder
* Payment tracker
* Support ticket creator
* Bus ticket request logging
* Education & career guidance

## 🧩 Extensible

* Plugin system
* Scheduler system
* Background watchdog monitoring

---

# ⚠️ Legal & Ethical Notice

Pentesting and exploitation features are intended **ONLY for:**

* Personal labs
* CTF environments
* Authorized test systems

Do NOT use against unauthorized targets.

---

# 🧱 Architecture Overview

```
Voice Input → Command Parser → Action Router → Modules
                                     ├── AI Engine (Ollama)
                                     ├── Automation Layer
                                     ├── Pentest Tools
                                     ├── Email System
                                     ├── OCR Engine
                                     ├── Macro Engine
                                     └── Media Layer
```

---

# 📦 Requirements

## OS

* Linux recommended (GNOME tested)
* Wayland supported (portal screenshot method)
* Windows partially supported (no full feature parity)

---

## System Packages

Install core dependencies:

```bash
sudo apt update

sudo apt install -y \
python3 python3-venv python3-pip \
tesseract-ocr \
mpv yt-dlp \
nmap nikto gobuster whatweb \
searchsploit metasploit-framework \
zaproxy \
xdotool gnome-terminal
```

---

# 🐍 Python Dependencies

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install packages:

```bash
pip install \
psutil \
pyautogui \
pytesseract \
SpeechRecognition \
pillow \
gtts \
playsound \
pynput \
pyaudio
```

If PyAudio fails:

```bash
sudo apt install portaudio19-dev
pip install pyaudio
```

---

# 🧠 AI Model Setup (Ollama + DeepSeek)

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull model:

```bash
ollama pull deepseek-r1:7b
```

Test:

```bash
ollama run deepseek-r1:7b
```

---

# 📧 Email Setup

Set environment variables:

```bash
export JULI_EMAIL="your_email@gmail.com"
export JULI_EMAIL_PASS="your_app_password"
```

Use **Gmail App Password**, not your real password.

---

# 🧾 File Structure

```
project/
│
├── assistant.py
├── zap_module.py
├── hand-mouse.py
├── zap_web_ui.py
│
├── appointments.txt
├── payments.txt
├── system_errors.log
│
├── macros/
├── pentest_scans/
├── ctf_notes.txt
```

---

# ▶️ Running JULI

```bash
python3 assistant.py
```

Choose mode:

```
1 — Voice Mode
2 — Command Line Mode
```

---

# 🎤 Voice Command Format

All commands must start with:

```
juli <command>
```

Example:

```
juli date
juli system status
juli read screen
```

---

# 📚 Command Reference

## General

```
juli date
juli system status
juli list files
juli open directory
juli search <term>
juli browser search <term>
juli close
juli exit
```

---

## AI

```
juli code <prompt>
juli read screen
juli analyze errors
juli motivate <text>
juli comfort <text>
juli smile <text>
juli ask <question>
```

---

## Email

```
juli mail <topic>
```

---

## Productivity

```
juli rec appointment
juli payment
juli support
juli education
juli bus ticket
```

---

## Media

```
juli song <name>
juli mouse
juli sign
```

---

## Macro Automation

```
juli record macro <file>
juli play macro <file>
```

Stop macro playback:

```
Press F8
```

---

## Pentest Lab Commands

```
juli pentest nmap <target>
juli pentest webscan <url>
juli pentest enum linux
juli pentest exploit search <term>
juli pentest cve <id>
juli pentest msf
juli pentest checklist
juli zap start
juli zap spider <url>
juli zap active <url>
juli zap alerts
```

---

# 🧠 OCR Screen Reading

Uses:

```
GNOME portal screenshot → Tesseract → AI summary
```

First run will request screenshot permission.

---

# 🧩 Plugin System

Add plugins with:

```
def commands():
    return ["keyword"]

def handle(command):
    ...
```

They are auto-dispatched in command flow.

---

# ⏱ Scheduler

Built-in:

* Background system monitor
* Daily error analysis
* Interval jobs supported

---

# 🔒 Security Notes

* Store email credentials via environment variables only
* Never commit passwords
* Pentest tools are lab-only
* Macro playback can control your system — use carefully
* AI code generation runs code automatically — sandbox recommended

---

# 🐞 Troubleshooting

## PyAutoGUI Wayland Issues

Switch to X11 session or install:

```bash
sudo apt install xdotool
```

---

## Microphone Not Detected

```bash
arecord -l
```

Then configure ALSA / PulseAudio.

---

## Tesseract Not Found

```bash
which tesseract
```

Set path in code if needed.

---

# 🛣 Roadmap Ideas

* GUI dashboard
* Plugin marketplace
* Encrypted config store
* Remote agent mode
* Multi-assistant orchestration
* Web control panel
* Docker deployment

---

# 👨‍💻 Author

Built for automation, AI experimentation, and security learning workflows.

---

# 📜 License

Use responsibly. Lab + educational usage recommended.
Add your preferred license file (MIT / Apache / GPL).

---
