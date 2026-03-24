from flask import Flask, render_template, abort
from datetime import datetime

app = Flask(__name__)

# ── Data ──────────────────────────────────────────────────────────────────────
# Cost figures are based on publicly reported estimates from sources such as
# the Kiel Institute, Congressional Budget Office, UN OCHA, and Reuters.
# Daily costs are conservative mid-range estimates.

CONFLICTS = {
    "ukraine": {
        "id": "ukraine",
        "name": "Russia–Ukraine War",
        "flag_a": "🇺🇦",
        "flag_b": "🇷🇺",
        "started": "2022-02-24",
        "daily_cost_usd": 1_000_000_000,   # ~$1B/day combined (both sides + aid)
        "total_cost_usd": 1_400_000_000_000, # ~$1.4T estimated total as of early 2025
        "cost_basis_date": "2025-01-01",
        "description": "The largest conventional war in Europe since World War II, triggered by Russia's full-scale invasion of Ukraine on February 24, 2022.",
        "casualties": "500,000+",
        "displaced": "14,000,000+",
        "top_funders": [
            {"country": "United States", "flag": "🇺🇸", "amount": "$175B+", "type": "Military & Economic Aid"},
            {"country": "European Union", "flag": "🇪🇺", "amount": "$100B+", "type": "Financial & Military Aid"},
            {"country": "Germany",        "flag": "🇩🇪", "amount": "$22B+",  "type": "Military & Humanitarian"},
            {"country": "United Kingdom", "flag": "🇬🇧", "amount": "$15B+",  "type": "Military Aid"},
            {"country": "Russia",         "flag": "🇷🇺", "amount": "$300B+", "type": "Military Expenditure"},
        ],
        "per_taxpayer": [
            {"country": "United States", "flag": "🇺🇸", "amount": "$530"},
            {"country": "Germany",       "flag": "🇩🇪", "amount": "$620"},
            {"country": "United Kingdom","flag": "🇬🇧", "amount": "$540"},
        ],
        "breakdown": [
            {"label": "Military Equipment & Weapons", "pct": 38},
            {"label": "Russian Military Expenditure",  "pct": 28},
            {"label": "Economic & Budget Aid",         "pct": 18},
            {"label": "Humanitarian Aid",              "pct": 10},
            {"label": "Reconstruction Costs",          "pct": 6},
        ],
        "sources": [
            {"name": "Kiel Institute for the World Economy", "url": "https://www.ifw-kiel.de/topics/war-against-ukraine/ukraine-support-tracker/"},
            {"name": "Congressional Budget Office (CBO)",    "url": "https://www.cbo.gov"},
            {"name": "Reuters — War Cost Estimates",         "url": "https://www.reuters.com"},
        ],
        "color": "#4a90d9",
        "color_dark": "#2c5f8a",
    },
    "gaza": {
        "id": "gaza",
        "name": "Gaza War",
        "flag_a": "🇵🇸",
        "flag_b": "🇮🇱",
        "started": "2023-10-07",
        "daily_cost_usd": 260_000_000,    # ~$260M/day combined
        "total_cost_usd": 165_000_000_000, # ~$165B estimated total as of early 2025
        "cost_basis_date": "2025-01-01",
        "description": "A war between Israel and Hamas beginning October 7, 2023, following a Hamas attack on southern Israel. The conflict has caused a severe humanitarian crisis in Gaza.",
        "casualties": "45,000+",
        "displaced": "1,900,000+",
        "top_funders": [
            {"country": "United States", "flag": "🇺🇸", "amount": "$18B+",  "type": "Military Aid to Israel"},
            {"country": "Israel",        "flag": "🇮🇱", "amount": "$60B+",  "type": "Military Expenditure"},
            {"country": "Qatar",         "flag": "🇶🇦", "amount": "$1.5B+", "type": "Humanitarian Aid to Gaza"},
            {"country": "UN Agencies",   "flag": "🇺🇳", "amount": "$2B+",   "type": "Humanitarian Relief"},
        ],
        "per_taxpayer": [
            {"country": "United States", "flag": "🇺🇸", "amount": "$54"},
            {"country": "Israel",        "flag": "🇮🇱", "amount": "$6,200"},
        ],
        "breakdown": [
            {"label": "Israeli Military Operations",  "pct": 42},
            {"label": "US Military Aid to Israel",    "pct": 20},
            {"label": "Infrastructure Destruction",   "pct": 22},
            {"label": "Humanitarian Aid",             "pct": 10},
            {"label": "Economic Losses",              "pct": 6},
        ],
        "sources": [
            {"name": "UN OCHA — Humanitarian Situation", "url": "https://www.ochaopt.org"},
            {"name": "World Bank — Gaza Economic Monitor","url": "https://www.worldbank.org"},
            {"name": "Reuters — Gaza War Costs",         "url": "https://www.reuters.com"},
        ],
        "color": "#c0392b",
        "color_dark": "#7b241c",
    },
    "sudan": {
        "id": "sudan",
        "name": "Sudan Civil War",
        "flag_a": "🇸🇩",
        "flag_b": "⚔️",
        "started": "2023-04-15",
        "daily_cost_usd": 56_000_000,    # ~$56M/day
        "total_cost_usd": 40_000_000_000, # ~$40B estimated total as of early 2025
        "cost_basis_date": "2025-01-01",
        "description": "A civil war between the Sudanese Armed Forces and the Rapid Support Forces (RSF) that began April 15, 2023. It has caused one of the world's worst humanitarian crises.",
        "casualties": "20,000+",
        "displaced": "10,000,000+",
        "top_funders": [
            {"country": "UAE",            "flag": "🇦🇪", "amount": "Undisclosed", "type": "Alleged RSF Support"},
            {"country": "Egypt",          "flag": "🇪🇬", "amount": "Undisclosed", "type": "SAF Support"},
            {"country": "UN & NGOs",      "flag": "🇺🇳", "amount": "$2.5B+",     "type": "Humanitarian Aid"},
            {"country": "United States",  "flag": "🇺🇸", "amount": "$1B+",       "type": "Humanitarian Aid"},
        ],
        "per_taxpayer": [
            {"country": "United States", "flag": "🇺🇸", "amount": "$3"},
            {"country": "Sudan",         "flag": "🇸🇩", "amount": "$850"},
        ],
        "breakdown": [
            {"label": "Military Operations (SAF + RSF)", "pct": 45},
            {"label": "Economic Collapse & GDP Loss",    "pct": 30},
            {"label": "Humanitarian Aid",                "pct": 15},
            {"label": "Infrastructure Damage",           "pct": 10},
        ],
        "sources": [
            {"name": "UN OCHA — Sudan Crisis",           "url": "https://www.unocha.org/sudan"},
            {"name": "Acled — Armed Conflict Data",      "url": "https://acleddata.com"},
            {"name": "IMF — Sudan Economic Outlook",     "url": "https://www.imf.org"},
        ],
        "color": "#e67e22",
        "color_dark": "#935116",
    },
}


def days_since(date_str):
    start = datetime.strptime(date_str, "%Y-%m-%d")
    return (datetime.utcnow() - start).days


def cost_since_basis(conflict):
    """Calculate total cost = stored total + days since basis date * daily rate."""
    basis = datetime.strptime(conflict["cost_basis_date"], "%Y-%m-%d")
    extra_days = (datetime.utcnow() - basis).days
    return conflict["total_cost_usd"] + extra_days * conflict["daily_cost_usd"]


@app.route("/")
def index():
    cards = []
    for c in CONFLICTS.values():
        cards.append({
            **c,
            "days": days_since(c["started"]),
            "current_total": cost_since_basis(c),
        })
    return render_template("index.html", conflicts=cards)


@app.route("/conflict/<conflict_id>")
def detail(conflict_id):
    conflict = CONFLICTS.get(conflict_id)
    if not conflict:
        abort(404)
    conflict["days"] = days_since(conflict["started"])
    conflict["current_total"] = cost_since_basis(conflict)
    return render_template("detail.html", c=conflict)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
