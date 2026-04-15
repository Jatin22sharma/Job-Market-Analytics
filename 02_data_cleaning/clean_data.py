import pandas as pd
import os
import re

df = pd.read_csv("01_data_collection/raw_data/jobs_raw.csv")
print(f"Loaded: {len(df)} rows")

# ── 1. Basic nulls ──────────────────────────────────────────
df["skills_required"] = df["skills_required"].fillna("")
df["description"]     = df["description"].fillna("")
df["location"]        = df["location"].fillna("India")
df["is_remote"]       = df["is_remote"].fillna(False)
df["salary_min"]      = pd.to_numeric(df["salary_min"], errors="coerce").fillna(0)
df["salary_max"]      = pd.to_numeric(df["salary_max"], errors="coerce").fillna(0)

# ── 2. Salary disclosed flag (more useful than the number) ──
df["salary_disclosed"] = df["salary_min"].apply(lambda x: "Yes" if x > 0 else "No")

# ── 3. Salary bucket (only for rows that have it) ──────────
def salary_bucket(val):
    if val <= 0:        return "Not disclosed"
    elif val < 50000:   return "Below 50K USD"
    elif val < 100000:  return "50K-100K USD"
    elif val < 150000:  return "100K-150K USD"
    else:               return "150K+ USD"

df["salary_range"] = df["salary_min"].apply(salary_bucket)

# ── 4. Skills from description + skills_required ───────────
TOP_SKILLS = [
    "python", "sql", "excel", "power bi", "tableau",
    "azure", "aws", "machine learning", "spark",
    "pandas", "postgresql", "mysql", "powerpoint"
]

def check_skill(row, skill):
    text = (str(row["skills_required"]) + " " + str(row["description"])).lower()
    return 1 if skill in text else 0

for skill in TOP_SKILLS:
    df["skill_" + skill.replace(" ", "_")] = df.apply(lambda r, s=skill: check_skill(r, s), axis=1)

# ── 5. Experience from description ─────────────────────────
def extract_exp(text):
    text = str(text).lower()[:600]
    m = re.search(r'(\d+)\s*[-to]+\s*(\d+)\s*years?\s*(?:of\s*)?(?:exp|experience)?', text)
    if m:
        v = (int(m.group(1)) + int(m.group(2))) / 2
        return v if v <= 20 else None
    m = re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:exp|experience)', text)
    if m:
        v = int(m.group(1))
        return v if v <= 20 else None
    m = re.search(r'(?:exp|experience)[^\d]{0,10}(\d+)\+?\s*years?', text)
    if m:
        v = int(m.group(1))
        return v if v <= 20 else None
    if any(w in text for w in ["fresher", "entry level", "0 year", "no experience"]):
        return 0
    return None

df["experience_years"] = df["description"].apply(extract_exp)

def exp_label(v):
    if pd.isna(v): return "Not specified"
    elif v == 0:   return "Fresher"
    elif v <= 2:   return "0-2 years"
    elif v <= 5:   return "2-5 years"
    else:          return "5+ years"

df["experience_range"] = df["experience_years"].apply(exp_label)

# ── 6. Job category ────────────────────────────────────────
def categorise(title):
    t = str(title).lower()
    if "business" in t:                              return "Business Analyst"
    if any(w in t for w in ["ai", "machine learning", "ml"]): return "AI/ML Analyst"
    if any(w in t for w in ["power bi", "tableau", "bi "]):   return "BI Analyst"
    if "engineer" in t:                              return "Data Engineer"
    if "data" in t:                                  return "Data Analyst"
    if "analyst" in t:                               return "Other Analyst"
    return "Other"

df["job_category"] = df["job_title"].apply(categorise)

# ── 7. Clean location ──────────────────────────────────────
def clean_location(loc):
    loc = str(loc).strip()
    if loc in ["IN", "India", "india"]: return "India (unspecified)"
    return loc

df["location"] = df["location"].apply(clean_location)

# ── 8. Fix dates ───────────────────────────────────────────
df["date_posted"]  = pd.to_datetime(df["date_posted"], errors="coerce").dt.date
df["month_posted"] = pd.to_datetime(df["date_posted"], errors="coerce").dt.strftime("%b %Y")

# ── 9. Drop unused columns ─────────────────────────────────
df.drop(columns=["experience"], inplace=True, errors="ignore")

# ── 10. Save ───────────────────────────────────────────────
os.makedirs("02_data_cleaning/cleaned_data", exist_ok=True)
df.to_csv("02_data_cleaning/cleaned_data/jobs_clean.csv", index=False)

print(f"\nDone! {len(df)} rows, {df.shape[1]} columns")
print("\nJob categories:")
print(df["job_category"].value_counts())
print("\nExperience ranges:")
print(df["experience_range"].value_counts())
print("\nSalary disclosed:")
print(df["salary_disclosed"].value_counts())
skill_cols = [c for c in df.columns if c.startswith("skill_")]
print("\nSkill counts:")
print(df[skill_cols].sum().sort_values(ascending=False))