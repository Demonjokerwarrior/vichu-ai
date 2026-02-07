Nice project — this is a **full-blown desktop AI assistant**, not a toy 😄
Here’s a clean, professional **`README.md`** you can drop straight into your GitHub repo.

---

# 🤖 Juli – Intelligent Desktop Voice Assistant

**Juli** is an advanced Python-based desktop assistant that combines voice control, automation, AI-powered text generation, system monitoring, macros, and emotional interaction into a single unified tool.
It is designed for Linux systems (GNOME recommended) and integrates deeply with the OS.

---

## ✨ Features

### 🎙️ Voice & Command-Line Control

* Wake-word based command execution (`"juli"`)
* Google Speech Recognition
* Text-to-Speech responses (gTTS)

### 📧 Smart Email Assistant

* AI-drafted email bodies using **DeepSeek (via Ollama)**
* Automatic subject generation
* Gmail SMTP integration

### 🧠 AI Capabilities

* Code generation & execution
* Screen text reading + AI summarization
* Emotional, motivational, and comforting responses
* Education & career guidance
* Health-related Q&A

### 🖥️ System & File Operations

* List and open directories
* Monitor CPU & memory usage
* Run terminal commands in new windows
* Scheduled jobs (interval & cron-like)

### 🧩 Automation & Macros

* Record mouse & keyboard macros
* Replay macros with precise timing
* Emergency stop during playback (F8)

### 📅 Productivity Tools

* Appointment recording
* Payment requests
* Bus ticket requests
* Support / grievance logging

### 🎵 Media & Browser

* Play YouTube songs via `mpv`
* Google search via browser
* Dedicated browser agent

### 🔐 Advanced / Security Tools

* TCP listener (educational use)
* CamPhish launcher (educational / testing only)

---

## 🛠️ Requirements

### System

* **Linux (GNOME recommended)**
* Python **3.8+**

### Python Libraries

```bash
pip install speechrecognition pyautogui psutil pytesseract gtts playsound pillow pynput
```

### System Dependencies

```bash
sudo apt install mpv tesseract-ocr xdotool gnome-terminal
```

### Optional (AI Features)

* **Ollama**
* DeepSeek model:

```bash
ollama pull deepseek-r1:7b
```

---

## 🔐 Environment Variables

Set your email credentials securely:

```bash
export JULI_EMAIL="your_email@gmail.com"
export JULI_EMAIL_PASS="your_app_password"
```

> ⚠️ Use **Gmail App Passwords**, not your main password.

---

## 🚀 How to Run

```bash
python3 juli.py
```

Choose:

```
1 → Voice Mode
2 → Command Line Mode
```

---

## 🗣️ Example Commands

```
juli send mail about project update
juli system status
juli play song interstellar theme
juli read screen
juli record macro
juli play macro
juli motivate me
juli education guidance
juli list files
juli search python automation
```

---

## 📂 Project Files

| File                   | Purpose            |
| ---------------------- | ------------------ |
| `juli.py`              | Main assistant     |
| `appointments.txt`     | Saved appointments |
| `payments.txt`         | Payment records    |
| `support_requests.txt` | Support tickets    |
| `system_errors.log`    | Error logs         |
| `macro.json`           | Recorded macros    |

---

## ⚠️ Disclaimer

This project is intended for **personal productivity, automation, learning, and ethical security testing only**.
Any misuse for unauthorized access or malicious activity is **strictly discouraged** and is the user’s responsibility.

---

## ❤️ Credits

* Python Open Source Community
* Ollama + DeepSeek
* Google Speech Recognition
* GNOME & Linux ecosystem

---

## 🌟 Future Improvements

* Plugin marketplace
* GUI dashboard
* Cross-platform support
* Offline speech recognition
* Encrypted data storage

---


