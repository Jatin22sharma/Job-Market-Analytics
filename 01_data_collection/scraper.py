# --- Import libraries ---
import requests   # sends web requests (like opening a URL)
import pandas as pd  # creates and saves data tables
import os         # reads system settings
import time       # adds delays so we don't hit API too fast
from dotenv import load_dotenv  # reads our .env file

# --- Load the API key from .env ---
load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")

# --- Define what we want to search ---
SEARCH_QUERIES = [
    "data analyst",
    "business analyst",
    "AI analyst",
    "data analyst fresher",
    "data analyst Python SQL",
    "power bi analyst",
    "sql analyst",
    "analytics engineer",
    "data analyst remote",
    "junior data analyst",
]

# --- API connection settings ---
url = "https://jsearch.p.rapidapi.com/search"
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch27.p.rapidapi.com"
}

# --- Function to fetch jobs for one query ---
def fetch_jobs(query, pages=5):
    all_jobs = []
    for page in range(1, pages + 1):
        params = {
            "query": query + " India",
            "page": str(page),
            "num_pages": "1",
            "date_posted": "month"  # only last 30 days
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        for job in data.get("data", []):
            all_jobs.append({
                "job_title":       job.get("job_title"),
                "company_name":    job.get("employer_name"),
                "location":        job.get("job_city") or job.get("job_country"),
                "is_remote":       job.get("job_is_remote"),
                "salary_min":      job.get("job_min_salary"),
                "salary_max":      job.get("job_max_salary"),
                "skills_required": ", ".join(job.get("job_required_skills") or []),
                "experience":      job.get("job_required_experience", {}).get("required_experience_in_months"),
                "date_posted":     job.get("job_posted_at_datetime_utc"),
                "job_url":         job.get("job_apply_link"),
                "description":     job.get("job_description", "")[:300]
            })
        time.sleep(1)  # wait 1 second between pages — good API etiquette
    return all_jobs

# --- Run for all queries and combine ---
all_results = []
for query in SEARCH_QUERIES:
    print(f"Fetching: {query}...")
    jobs = fetch_jobs(query, pages=3)
    all_results.extend(jobs)
    print(f"  Got {len(jobs)} jobs")
    time.sleep(2)  # wait between different search terms

# --- Create the output folder if it doesn't exist ---
os.makedirs("01_data_collection/raw_data", exist_ok=True)

csv_path = "01_data_collection/raw_data/jobs_raw.csv"

# --- Combine with existing data if file already exists ---
new_df = pd.DataFrame(all_results)

if os.path.exists(csv_path):
    existing_df = pd.read_csv(csv_path)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    combined_df.drop_duplicates(subset="job_url", inplace=True)
    combined_df.to_csv(csv_path, index=False)
    print(f"\nDone! Combined total: {len(combined_df)} unique jobs saved.")
else:
    new_df.drop_duplicates(subset="job_url", inplace=True)
    new_df.to_csv(csv_path, index=False)
    print(f"\nDone! Saved {len(new_df)} unique jobs.")
