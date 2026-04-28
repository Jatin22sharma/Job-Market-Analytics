# 📊 India Analyst Job Market Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_RDS-MySQL-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-Storage-FF9900?style=for-the-badge&logo=amazons3&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-Data_Cleaning-150458?style=for-the-badge&logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

**A real-time end-to-end data analytics pipeline tracking AI & analyst hiring trends across India**

[🔴 Live Dashboard](https://drive.google.com/file/d/15cFnI0MOevimS_tUEEdTkDvaigGPyYCM/view?usp=sharing) · [📁 View Dataset](https://github.com/Jatin22sharma/Job-Market-Analytics/blob/main/02_data_cleaning/cleaned_data/jobs_clean.csv) · [📄 Project Report](https://github.com/Jatin22sharma/Job-Market-Analytics/blob/main/03_analysis/analysis.ipynb)

</div>

---

## 📌 Project Overview

This project answers a question every data professional in India is asking in 2026:

> *"Which skills are employers actually demanding? Where are the jobs? And why can't anyone find salary information?"*

I built a complete data pipeline — from automated job data collection via REST API, through cloud storage on AWS, to a live 6-page interactive Power BI dashboard — using 562 real job postings collected in April 2026.

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   JSearch API   │───▶│   Python     │───▶│    AWS S3       │───▶│  AWS RDS     │───▶│   Power BI      │
│  (Job postings) │    │  (Scraper +  │    │  (Raw CSV       │    │  MySQL DB    │    │  (Live 6-page   │
│  LinkedIn,      │    │   Cleaning)  │    │   Storage)      │    │  Mumbai      │    │   Dashboard)    │
│  Indeed,        │    │              │    │                 │    │  ap-south-1  │    │                 │
│  Glassdoor      │    │  562 jobs    │    │  jobs_clean.csv │    │  job_postings│    │  Public URL     │
└─────────────────┘    └──────────────┘    └─────────────────┘    └──────────────┘    └─────────────────┘
```

---

## 🔑 Key Findings

| Finding | Insight |
|---|---|
| 🥇 **Most in-demand skill** | SQL — required in 64 of 562 postings (11.4%) |
| 🏙️ **Top hiring city** | Bengaluru — 10% of all analyst postings |
| 💰 **Salary transparency** | 75% of Indian analyst jobs don't disclose salary |
| 🏠 **Remote availability** | Only 9% of postings offer remote work |
| 🎓 **Fresher opportunity** | 93% of postings don't specify experience requirement |
| 📈 **Hiring growth** | 97% more postings in April vs March 2026 |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Data Collection** | Python 3.13, JSearch API (RapidAPI) | Automated job posting collection |
| **Data Cleaning** | Pandas, NumPy, Regex | Feature engineering, text mining |
| **Cloud Storage** | AWS S3 (ap-south-1) | Raw CSV storage |
| **Cloud Database** | AWS RDS MySQL 8.4 (ap-south-1) | Structured data warehouse |
| **Data Upload** | SQLAlchemy, PyMySQL | Python → AWS pipeline |
| **Visualisation** | Power BI Desktop + Service | Interactive dashboard |
| **Version Control** | Git, GitHub | Code management |

---

## 📁 Project Structure

```
job-market-analytics/
│
├── 01_data_collection/
│   ├── scraper.py                  ← JSearch API data collection
│   └── raw_data/
│       └── jobs_raw.csv            ← 562 raw job postings
│
├── 02_data_cleaning/
│   ├── clean_data.py               ← Cleaning + feature engineering
│   └── cleaned_data/
│       └── jobs_clean.csv          ← Production-ready dataset
│
├── 03_analysis/
│   ├── analysis.ipynb              ← EDA with 8 charts
│   ├── chart_job_categories.png
│   ├── chart_skills.png
│   ├── chart_cities.png
│   ├── chart_remote.png
│   ├── chart_salary.png
│   ├── chart_experience.png
│   ├── chart_trend.png
│   └── chart_top_companies.png
│
├── 04_aws/
│   ├── upload_to_s3.py             ← S3 upload script
│   └── upload_to_rds.py            ← RDS MySQL upload script
│
├── 05_dashboard/
│   └── JobMarketDashboard.pbix     ← Power BI dashboard file
│
├── requirements.txt
└── README.md
```

---

## 📊 Dashboard Pages

| Page | Title | Key Visual |
|---|---|---|
| 1 | Executive Overview | 4 KPI cards + category breakdown |
| 2 | Skills Intelligence | Skill demand ranking + cloud skills |
| 3 | Where Are the Jobs? | Top cities + top companies |
| 4 | Salary & Transparency | Transparency donut + salary ranges |
| 5 | Experience & Hiring Profile | Experience breakdown + role comparison |
| 6 | Hiring Trends Over Time | Weekly volume area chart + tech stack |

---

## ⚙️ How to Run This Project

### Prerequisites
```bash
Python 3.10+
AWS Account (free tier)
Power BI Desktop (free)
RapidAPI account (free tier)
```

### Installation
```bash
# Clone the repository
git clone https://github.com/Jatin22sharma/job-market-analytics.git
cd job-market-analytics

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env file
```

### Run the pipeline
```bash
# Step 1: Collect data
python 01_data_collection/scraper.py

# Step 2: Clean data
python 02_data_cleaning/clean_data.py

# Step 3: Upload to AWS
python 04_aws/upload_to_rds.py

# Step 4: Open dashboard
# Open 05_dashboard/JobMarketDashboard.pbix in Power BI Desktop
```

---

## 📦 Requirements

```
pandas==2.2.0
numpy==1.26.0
requests==2.31.0
beautifulsoup4==4.12.0
python-dotenv==1.0.0
sqlalchemy==2.0.0
pymysql==1.1.0
boto3==1.34.0
cryptography==42.0.0
matplotlib==3.8.0
```

---

## 🔒 Environment Variables

Create a `.env` file in the root directory:

```env
RAPIDAPI_KEY=your_rapidapi_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## 💡 What I Learned

- Designing and deploying a **cloud data pipeline on AWS** (S3 + RDS)
- **Text mining with regex** to extract structured data from unstructured job descriptions
- **Feature engineering** — converting raw API fields into analysis-ready columns
- Building **interactive Power BI dashboards** connected to a live cloud database
- The reality of **Indian job market data** — 75% salary opacity, low remote availability, and the dominance of Bengaluru as an analytics hub

---

## 🤝 Connect

**[Jatin Sharma]**
Aspiring Data Analyst | Python · SQL · Power BI · AWS

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/jatin-sharma22)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/Jatin22sharma)

---

<div align="center">
<sub>Built with real data · Powered by AWS · April 2026</sub>
</div>
