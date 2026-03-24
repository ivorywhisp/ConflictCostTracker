# Conflict Cost Tracker

**CS50x Final Project**

A web application that tracks and visualizes the estimated financial cost of active armed conflicts in real time.

---

## Video Demo

https://youtu.be/IUmyeR4LIyI

---

## Description

Conflict Cost Tracker is a Flask-based web application that presents running cost estimates for major ongoing armed conflicts. Each conflict displays a live ticking counter that increments every second based on estimated daily expenditure rates, sourced from international institutions such as the Kiel Institute, UN OCHA, the World Bank, and the IMF.

The project was inspired by national debt clocks — the idea that turning abstract billions into a live, ticking number makes the scale of these conflicts tangible in a way that static figures do not.

### Pages

- **Home (`/`)** — Lists all tracked conflicts as editorial rows with live cost counters, casualty figures, and displacement statistics.
- **Detail (`/conflict/<id>`)** — A deep-dive page per conflict showing the full cost breakdown (doughnut chart), per-taxpayer cost, key funders, and data sources.
- **Methodology (`/about`)** — Explains how cost figures are calculated, what is and isn't included, and links to all primary sources.

---

## Design Decisions

### Why Flask and no database?

Conflict cost data doesn't change in real time — it's updated every few months when new institutional reports are published. Storing data in a Python dictionary in `app.py` rather than a SQL database keeps the project simple and makes it easy to update figures when new estimates come out. If the project were to scale (more conflicts, user submissions, admin panel), migrating to SQLite would be the natural next step.

### Why a ticking counter?

The counter doesn't reflect real-time spending — no one can measure that. It uses a daily rate divided by 86,400 seconds to produce a continuous increment. The intent is emotional and editorial: to make the pace of expenditure visceral. This is disclosed clearly on the methodology page.

### Why an editorial aesthetic?

Most data visualization sites lean toward dark dashboards with glowing charts. The editorial design (cream backgrounds, serif typography, thin ruled lines) was a deliberate choice to signal that this is information worth reading carefully — not a live trading terminal. Inspired by publications like Sapir Journal and the Financial Times.

### Why these three conflicts?

Ukraine, Gaza, and Sudan were chosen because they are the three largest active conflicts by displacement and media coverage as of 2024, and because relatively reliable cost estimates exist for all three from institutional sources. The site is designed to accommodate additional conflicts by adding entries to the `CONFLICTS` dictionary in `app.py`.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, Bootstrap 4 |
| Charts | Chart.js |
| Fonts | Playfair Display, DM Sans, DM Mono (Google Fonts) |
| Data | Hardcoded from public institutional sources |

---

## Project Structure

```
project/
├── app.py                  # Flask app, routes, and all conflict data
├── requirements.txt
├── static/
│   └── styles.css          # All custom styles
└── templates/
    ├── layout.html          # Base template with nav and footer
    ├── index.html           # Homepage — conflict list with live counters
    ├── detail.html          # Per-conflict detail page
    └── about.html           # Methodology page
```

---

## How to Run

```bash
# Install dependencies
pip install flask

# Run the development server
flask run
```

Then open the URL shown in your terminal.

---

## Data Sources

- [Kiel Institute for the World Economy — Ukraine Support Tracker](https://www.ifw-kiel.de/topics/war-against-ukraine/ukraine-support-tracker/)
- [UN Office for the Coordination of Humanitarian Affairs (OCHA)](https://www.unocha.org)
- [World Bank — Damage and Needs Assessments](https://www.worldbank.org)
- [International Monetary Fund (IMF)](https://www.imf.org)
- [Armed Conflict Location & Event Data Project (ACLED)](https://acleddata.com)
- [Congressional Budget Office (CBO)](https://www.cbo.gov)
- Reuters and Financial Times investigative reporting

All figures are estimates. This site presents data for educational purposes and does not take political positions.

---

## Author

Created by Daniel Gallinas as the final project for Harvard's CS50x.
