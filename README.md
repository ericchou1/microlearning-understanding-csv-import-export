# The CSV Chronicles: The Merger 🔄

<a href="https://ericchou1.github.io/microlearning-understanding-csv-import-export/" target="_blank">
  <img src="assets/images/enter-button.svg" alt="Enter The Protocol">
</a>

An intermediate-level graphic novel tutorial for Nautobot CSV import and export operations.

## 📖 About

Follow **Alex Chen**, a senior network automation engineer at DataFlow Corp, as they tackle a company acquisition. TechNova Inc.'s entire network inventory must be imported into Nautobot, and compliance auditors need reports—all within a week!

This is an **intermediate tutorial** that assumes familiarity with:
- Python basics
- CSV operations (csv module)
- Nautobot fundamentals (UI, data models)

## 🎯 What You'll Learn

### Import Skills
- `FileVar` for file uploads in Jobs
- CSV parsing with `StringIO`
- Creating objects with Django ORM
- `get_or_create` / `update_or_create` for idempotency
- Error handling and validation

### Export Skills
- QuerySet filtering and optimization
- `select_related` / `prefetch_related`
- `ObjectVar` for filter dropdowns
- CSV generation and downloads
- Multi-model reports

### Nautobot Models Covered
- Device, DeviceType, Manufacturer
- Interface
- IPAddress, Prefix, Namespace
- Location, Role, Status

## 📚 Chapters

| Chapter | Title | Topics |
|---------|-------|--------|
| 1 | The Merger Begins | Codespace setup, Nautobot environment, Job basics |
| 2 | Importing the Fleet | FileVar, CSV parsing, Device creation |
| 3 | When Things Go Wrong | Error handling, get_or_create, idempotency |
| 4 | Exporting for the Auditors | QuerySets, CSV export, ObjectVar filters |
| 5 | The Complete Pipeline | Multi-model imports/exports, relationships |

## 🚀 Getting Started

### View the Tutorial

Enable GitHub Pages in your repository settings to view the site:
1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `version_1` → `/ (root)`
4. Your site will be at: `https://[username].github.io/[repo-name]/`

### Practice Environment

This tutorial uses the [100-days-of-nautobot](https://github.com/nautobot/100-days-of-nautobot) Codespace:

1. Go to the 100-days-of-nautobot repository
2. Click **Code** → **Codespaces** → **Create codespace**
3. Follow the setup in Chapter 1

## 📁 Project Structure

```
├── index.html              # Landing page
├── chapters/
│   ├── chapter-1.html      # The Merger Begins
│   ├── chapter-2.html      # Importing the Fleet
│   ├── chapter-3.html      # When Things Go Wrong
│   ├── chapter-4.html      # Exporting for the Auditors
│   └── chapter-5.html      # The Complete Pipeline
├── assets/
│   └── css/
│       └── styles.css      # Comic-style styling
└── exercises/              # Sample data and scripts
```

## 🔗 Resources

- [Nautobot Documentation](https://docs.nautobot.com/)
- [Nautobot Jobs Guide](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/jobs/)
- [100 Days of Nautobot](https://github.com/nautobot/100-days-of-nautobot)
- [Day 22: Process CSV Files](https://github.com/nautobot/100-days-of-nautobot/tree/main/Day022_Process_CSV_Files)

## 📝 License

MIT License - Use freely for learning and teaching!
