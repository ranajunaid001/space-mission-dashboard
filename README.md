# Space Missions Dashboard - Quick Guide

## Overview
Interactive dashboard exploring 4,630 space missions from 1957–2022.

**Live URL:** https://space-mission-dashboard-production.up.railway.app

---

## Features

### Filters (Sidebar)
| Filter | Description |
|--------|-------------|
| Date Range | Select start and end dates |
| Company | Filter by launch organization |
| Mission Status | Success, Failure, Partial Failure, Prelaunch Failure |
| Rocket Status | Active or Retired rockets |
| Reset | Clear all filters |

### Visualizations
1. **Missions Over Time** — Launch frequency by year
2. **Mission Outcomes** — Success/failure distribution
3. **Leading Organizations** — Top 10 companies by launches
4. **Success Rate by Company** — Reliability comparison

### Data Table
- **Search** — Find missions by name, company, or rocket
- **Sort** — Order by Date, Company, Mission, Rocket, or Status

---

## Required Functions

```python
GetMissionCountByCompany("SpaceX")        → 182
GetSuccessRate("SpaceX")                  → 94.50549
GetMissionsByDateRange("1957-10-01", "1957-12-31") → ['Sputnik-1', 'Sputnik-2', 'Vanguard TV3']
GetTopCompaniesByMissionCount(3)          → [('RVSN USSR', 1777), ('CASC', 338), ('Arianespace', 293)]
GetMissionStatusCount()                   → {'Success': 4162, 'Failure': 357, ...}
GetMissionsByYear(2020)                   → 119
GetMostUsedRocket()                       → 'Cosmos-3M (11K65M)'
GetAverageMissionsPerYear(2010, 2020)     → 72.27273
```

---

## Tech Stack
- **Python** + **Streamlit**
- **Pandas** for data processing
- **Plotly** for visualizations
- **Railway** for deployment

---

## Files
```
├── app.py              # Dashboard application
├── data_functions.py   # 8 required functions
├── space_missions.csv  # Dataset
├── requirements.txt    # Dependencies
├── Procfile            # Railway config
└── .streamlit/
    └── config.toml     # Theme configuration
```
