# RateFlow

**RateFlow** is a lightweight, end-to-end data pipeline built with Python.  
It automatically fetches live currency exchange rates from free APIs, stores them locally, and visualizes historical trends in an interactive Streamlit dashboard.

## 🚀 Features
- **Automated ETL:** Extracts, transforms, and loads daily exchange rate data.
- **Open APIs:** Uses [Frankfurter API](https://frankfurter.dev/).
- **Local Storage:** Saves data in a SQLite database for persistence and analysis.
- **Interactive Dashboard:** Explore and visualize currency trends over time with Streamlit.

## 🏗️ Tech Stack
- **Python 3**
- **Pandas** – data processing
- **SQLAlchemy + SQLite** – local database
- **Streamlit** – dashboard and visualization
- **Requests** – API data fetching
- **Altair** – Interactive data visualization  

## 📦 Project Structure

RateFlow/
├── dashboard/
│   └── app.py
├── etl/
│   ├── extract.py
│   ├── load.py
│   └── scheduler.py
├── data/
│   └── exchange_rates.db
├── requirements.txt
├── .gitignore
└── README.md

## 🧭 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/<your-username>/rateflow.git
cd rateflow
```

**2. Set up env**
# Option A: Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
````

Option B: Create a conda environment
```bash
conda create -n rateflow python=3.11
conda activate rateflow
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run ETL pipeline**
```bash
python etl/load.py
```

**5. Launch dashboard**
```bash
streamlit run dashboard/app.py
```


