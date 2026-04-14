# ============================================
# Step 3: Data Cleaning
# Input:  01_data_collection/raw_data/jobs_raw.csv
# Output: 02_data_cleaning/cleaned_data/jobs_clean.csv
# ============================================

import pandas as pd
import os
import re

# --- Load raw data ---
df = pd.read_csv("01_data_collection/raw_data/jobs_raw.csv")
print(f"Raw data: {len(df)} rows, {df.shape[1]} columns")
print("\nMissing values per column:")
print(df.isnull().sum())  # shows how many blanks each column has


# Raw date looks like: "2025-04-01T13:45:00.000Z"
# We only need: "2025-04-01"

df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
df["date_posted"] = df["date_posted"].dt.date  # keep only the date part

# Also extract month for trend analysis
df["month_posted"] = pd.to_datetime(df["date_posted"]).dt.strftime("%b %Y")

# errors="coerce" means: if a date is unreadable, set it to NaT
# instead of crashing the entire script

# --- Extract skills FROM DESCRIPTION ---
TOP_SKILLS = [
    "python", "sql", "excel", "power bi", "tableau",
    "azure", "aws", "machine learning", "spark",
    "pandas", "numpy", "powerpoint", "mysql", "postgresql"
]

# Note: removed "r" and "numpy" standalone — too error prone
# We handle R language separately with word boundary check

def has_skill(row, skill):
    text = ""
    if pd.notna(row.get("skills_required")):
        text += str(row["skills_required"]).lower()
    if pd.notna(row.get("description")):
        text += str(row["description"]).lower()
    if skill == "r":
        # match " r " or "r," or "(r)" — not inside words
        return 1 if re.search(r'\br\b', text) else 0
    return 1 if skill.lower() in text else 0

for skill in TOP_SKILLS:
    col_name = "skill_" + skill.replace(" ", "_")
    df[col_name] = df.apply(lambda row, s=skill: has_skill(row, s), axis=1)

# Add R language separately with word boundary
df["skill_r"] = df.apply(lambda row: has_skill(row, "r"), axis=1)

# --- Extract experience FROM DESCRIPTION (smarter version) ---
def extract_experience(text):
    if pd.isna(text):
        return None
    text = str(text).lower()

    # Only look in the first 500 characters — company history appears later
    text = text[:500]

    # Must be a small number (1-20) to be valid job experience
    match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)\s*years?\s*(?:of\s*)?(?:experience|exp)', text)
    if match:
        val = (int(match.group(1)) + int(match.group(2))) / 2
        return val if val <= 20 else None

    match = re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)', text)
    if match:
        val = int(match.group(1))
        return val if val <= 20 else None

    match = re.search(r'(?:experience|exp)[^\d]*(\d+)\+?\s*years?', text)
    if match:
        val = int(match.group(1))
        return val if val <= 20 else None

    if "fresher" in text or "entry level" in text or "0 year" in text:
        return 0

    return None

df["experience_years"] = df["description"].apply(extract_experience)

def experience_label(val):
    if pd.isna(val) or val == 0:
        return "Fresher / Not specified"
    elif val <= 1:
        return "0-1 year"
    elif val <= 2:
        return "1-2 years"
    elif val <= 4:
        return "2-4 years"
    else:
        return "4+ years"

df["experience_range"] = df["experience_years"].apply(experience_label)

# Raw titles are messy: "Sr. Data Anlyst", "DATA ANALYST", "data analyst - 2025"
# We group them into clean categories

def categorise_title(title):
    if pd.isna(title):
        return "Other"
    title = title.lower()
    if "business" in title:
        return "Business Analyst"
    elif "ai" in title or "artificial" in title or "machine learning" in title:
        return "AI/ML Analyst"
    elif "power bi" in title or "tableau" in title or "bi " in title:
        return "BI Analyst"
    elif "data" in title and "engineer" in title:
        return "Data Engineer"
    elif "data" in title:
        return "Data Analyst"
    elif "analyst" in title:
        return "Other Analyst"
    else:
        return "Other"

df["job_category"] = df["job_title"].apply(categorise_title)

# --- Drop columns we no longer need ---
df.drop(columns=["experience"], inplace=True)  # replaced by experience_years

# --- Remove any rows with no job title at all ---
df.dropna(subset=["job_title"], inplace=True)

# --- Clean up whitespace in text columns ---
df["job_title"]    = df["job_title"].str.strip()
df["company_name"] = df["company_name"].str.strip()
df["location"]     = df["location"].str.strip()

# --- Save the cleaned file ---
os.makedirs("02_data_cleaning/cleaned_data", exist_ok=True)
df.to_csv("02_data_cleaning/cleaned_data/jobs_clean.csv", index=False)

print(f"\nCleaning complete!")
print(f"Cleaned rows : {len(df)}")
print(f"Total columns: {df.shape[1]}")
print(f"Saved to: 02_data_cleaning/cleaned_data/jobs_clean.csv")
print(f"\nJob categories found:")
print(df["job_category"].value_counts())