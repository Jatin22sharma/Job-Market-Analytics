import pandas as pd
from sqlalchemy import create_engine, text

# --- Your RDS details ---
RDS_ENDPOINT = "jobmarket-db.c1gcm4wiwm3j.ap-south-1.rds.amazonaws.com"
RDS_PORT     = 3306
RDS_USER     = "admin"
RDS_PASSWORD = "JobMarket2026"

# --- Step 1: Connect WITHOUT database name first ---
engine_root = create_engine(
    f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/",
    connect_args={"connect_timeout": 30}
)

# --- Step 2: Create the database if it doesn't exist ---
with engine_root.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS jobmarketdb"))
    print("Database 'jobmarketdb' created (or already exists)")

# --- Step 3: Now connect WITH the database name ---
engine = create_engine(
    f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/jobmarketdb",
    connect_args={"connect_timeout": 30}
)

# --- Step 4: Test connection ---
with engine.connect() as conn:
    conn.execute(text("SELECT 1"))
    print("Connection to jobmarketdb successful!")

# --- Step 5: Load cleaned CSV ---
df = pd.read_csv("02_data_cleaning/cleaned_data/jobs_clean.csv")
print(f"Loaded {len(df)} rows from jobs_clean.csv")

# --- Step 6: Upload to RDS ---
print("Uploading... this takes 1-2 minutes...")
df.to_sql(
    name="job_postings",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=100
)

# --- Step 7: Verify ---
result = pd.read_sql("SELECT COUNT(*) as total FROM job_postings", engine)
print(f"\nDone! Rows in AWS RDS: {result['total'][0]}")