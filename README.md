# The CSV Chronicles 📊

A graphic novel-style learning experience that teaches CSV import/export with Python, culminating in Nautobot integration.

## 🎯 About This Project

Follow **Alex Chen**, a network engineer who inherits a chaotic network with zero documentation—only scattered CSV files. Through this interactive story, you'll learn:

- **Python CSV Basics** - Reading and writing CSV files
- **Data Validation** - Cleaning and normalizing messy data
- **Data Transformation** - Building ETL pipelines
- **Nautobot Integration** - Using CSVs as a bridge to a network source of truth

## 🚀 Quick Start

### View the Story

Visit the GitHub Pages site to read the story and learn:

1. Go to the repository's **Settings** → **Pages**
2. Enable GitHub Pages from the `main` branch
3. Access your site at `https://[username].github.io/[repo-name]`

### Practice in Codespace

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new)

1. Click the badge above or go to **Code** → **Codespaces** → **Create codespace**
2. Wait for the environment to build (Python 3.12 with dependencies)
3. Navigate to `exercises/` and run the Python files

```bash
# Run exercises
cd exercises
python exercise-1.py  # Reading CSVs
python exercise-2.py  # Validation
python exercise-3.py  # Writing CSVs
```

## 📚 Story Chapters

| Chapter | Title | Topics |
|---------|-------|--------|
| 1 | The Spreadsheet Nightmare | CSV structure, `csv.reader`, `csv.DictReader` |
| 2 | Making Sense of Chaos | Data validation, cleaning, error handling |
| 3 | Building Order from Disorder | Writing CSVs, `csv.DictWriter`, transformations |
| 4 | The Source of Truth | Introduction to Nautobot, data modeling |
| 5 | Automation Victory | Nautobot Jobs, `FileVar`, CSV imports |

## 📁 Project Structure

```
├── index.html              # Landing page
├── chapters/               # Story chapters (HTML)
│   ├── chapter-1.html
│   ├── chapter-2.html
│   ├── chapter-3.html
│   ├── chapter-4.html
│   └── chapter-5.html
├── exercises/              # Hands-on Python exercises
│   ├── exercise-1.py       # Reading CSVs
│   ├── exercise-2.py       # Validation
│   ├── exercise-3.py       # Writing CSVs
│   └── sample-data/        # CSV files for practice
├── assets/
│   └── css/
│       └── styles.css      # Comic-style CSS
└── .devcontainer/          # Codespace configuration
```

## 🛠️ Local Development

To run the site locally:

```bash
# Simple Python server
python -m http.server 8000

# Then open http://localhost:8000
```

To run exercises locally:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

# Install dependencies (optional, for pandas)
pip install pandas

# Run exercises
cd exercises
python exercise-1.py
```

## 🎨 Design

The site uses a comic book / graphic novel aesthetic with:

- **Dark theme** inspired by IDE/terminal aesthetics
- **Comic panels** with speech bubbles and narrative boxes
- **Tailwind CSS** for responsive layouts
- **Prism.js** for syntax highlighting
- **Custom fonts**: Bangers (titles), Comic Neue (dialogue), JetBrains Mono (code)

## 🔗 Inspired By

This project is inspired by [100 Days of Nautobot](https://github.com/nautobot/100-days-of-nautobot), specifically [Day 22: Process CSV Files](https://github.com/nautobot/100-days-of-nautobot/tree/main/Day022_Process_CSV_Files).

## 📝 License

MIT License - Feel free to use this for learning and teaching!
