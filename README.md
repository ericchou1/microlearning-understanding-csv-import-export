# NETRUNNER: The Nautobot Protocol

<a href="https://ericchou1.github.io/microlearning-understanding-csv-import-export/" target="_blank">
  <img src="https://img.shields.io/badge/View%20Live%20Site-00FFFF?style=for-the-badge&logo=github" alt="View Live Site">
</a>

**A LitRPG learning experience for mastering Nautobot CSV import/export.**

## 🎮 The Story

*Neo-Tokyo, 2087.*

You are a **netrunner**—a ghost in the machine, hired by the megacorp DataFlow Industries to infiltrate a network infrastructure database called **Nautobot**. Your mission: learn everything about CSV data manipulation.

But nothing is as it seems. A mysterious entity called **Ghost** watches from within the system, offering cryptic warnings. What happened to the runners who came before you? And what is DataFlow really planning?

## 📖 Features

- **Immersive narrative** with plot twists and character reveals
- **Interactive elements** — character creation, skill tracking, quest log
- **NPCs** — Maya the fixer, Ghost the enigma
- **RPG mechanics** — XP, skills, level progression
- **Real technical content** — Nautobot Jobs, CSV operations, Django ORM

## 🗺️ Quest Log

| Quest | Title | Story | Skills |
|-------|-------|-------|--------|
| 01 | INITIALIZATION | Jack into the system | SYSTEM_ACCESS, TERMINAL_CTRL |
| 02 | DATA EXTRACTION | First data stream arrives | FILE_UPLOAD, CSV_PARSE |
| 03 | ERROR RECOVERY | Ghost's warning saves you | IDEMPOTENCY, ERROR_HANDLE |
| 04 | DATA EXFILTRATION | Extract the payload | QUERY_BUILD, EXPORT_STREAM |
| 05 | SYSTEM INTEGRATION | The truth revealed | MULTI_MODEL, DATA_ARCHITECT |

## 🚀 Getting Started

1. Open `index.html` in your browser
2. Create your character
3. Follow the story through all 5 quests

**Or deploy to GitHub Pages:**
- Set your repository's Pages source to the `version_2` branch

## 📁 Structure

```
├── index.html              # Prologue and mission hub
├── chapters/
│   ├── quest-01.html      # INITIALIZATION
│   ├── quest-02.html      # DATA EXTRACTION
│   ├── quest-03.html      # ERROR RECOVERY
│   ├── quest-04.html      # DATA EXFILTRATION
│   └── quest-05.html      # SYSTEM INTEGRATION
├── assets/
│   ├── css/cyberpunk.css  # Cyberpunk visual theme
│   └── js/litrpg.js       # Interactive RPG mechanics
└── data/                   # Sample CSV files
```

## 🛠️ Technical Content Covered

- Nautobot Jobs with `FileVar` for file uploads
- CSV parsing with `csv.DictReader` and `StringIO`
- Django ORM: `get_or_create`, `update_or_create`
- QuerySets: `filter`, `select_related`, `prefetch_related`
- Multi-model operations: Devices, Interfaces, IP Addresses

## 📚 Resources

- [Nautobot Documentation](https://docs.nautobot.com/)
- [100 Days of Nautobot](https://github.com/nautobot/100-days-of-nautobot)

## License

MIT License
