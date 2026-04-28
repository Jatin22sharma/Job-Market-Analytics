import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# --- Get AWS credentials ---
# Go to AWS Console → top-right your name → Security Credentials
# → Access keys → Create access key → copy both values to .env

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME    = "job-market-data-jatin-sharma"  # your actual bucket name

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="ap-south-1"
)

s3.upload_file(
    "02_data_cleaning/cleaned_data/jobs_clean.csv",  # local file
    BUCKET_NAME,                                      # S3 bucket
    "cleaned/jobs_clean.csv"                          # path inside bucket
)

print(f"Uploaded jobs_clean.csv to s3://{BUCKET_NAME}/cleaned/jobs_clean.csv")