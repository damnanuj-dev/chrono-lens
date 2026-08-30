# 🔎 ChronoLens

A simple Python command-line tool for exploring and analyzing calendar dates.

## ✨ Features

* 📅 Get the weekday for any date
* 🔢 Find the day of the year
* 📊 Show the ISO week number
* 🗓️ Check days in a month
* 🌓 Detect leap years
* 🎂 Calculate age
* 🎉 Find the next birthday
* ⏳ Show days remaining until the next birthday
* 💻 Interactive command-line interface
* 🏷️ Version information with `--version`

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/chrono-lens.git
cd chrono-lens
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 4. Run the program

```bash
python dayfinder.py
```

Enter a date when prompted:

```text
Date > 2000-01-01
```

You can also provide a date directly:

```bash
python dayfinder.py 2000-01-01
```

## 📌 Example

```text
╔══════════════════════════════════════════════════════════════╗
║                    ✦ CHRONOLENS ✦                           ║
╠══════════════════════════════════════════════════════════════╣
║  Date            : Saturday, 01 January 2000                ║
║  Weekday         : Saturday                                  ║
║  Day of year     : 1                                         ║
║  ISO week        : 52                                        ║
║  Days in month   : 31                                        ║
║  Leap year       : Yes                                       ║
╠══════════════════════════════════════════════════════════════╣
║  Fun fact        : शनिवार                                    ║
╚══════════════════════════════════════════════════════════════╝
```

## 🛠️ Built With

* Python 3.9+
* `datetime`
* `calendar`
* `argparse`
* `dataclasses`

## 📂 Project Structure

```text
chrono-lens/
│
├── dayfinder.py
├── README.md
└── .gitignore
```

## 📜 License

This project is open source and available under the MIT License.

---

⭐ If you find this project useful, consider giving it a star!
