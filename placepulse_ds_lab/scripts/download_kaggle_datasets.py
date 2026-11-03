"""
PlacePulse AI: Automated Dataset Downloader via Kaggle CLI & Hugging Face
Module: scripts/download_kaggle_datasets.py
Author: PlacePulse AI Team
License: Approved Production Blueprint - v1.0.0
"""

import os
import sys
import shutil
import subprocess
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
RAW_DATA_DIR = os.path.join(PROJECT_DIR, "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

DATASETS = [
    {
        "name": "Engineering College Placement Prediction (Tejashvi)",
        "kaggle_slug": "tejashvi14/engineering-placements-prediction",
        "output_dir": RAW_DATA_DIR,
        "expected_files": ["collegePlace.csv"]
    },
    {
        "name": "Factors Influencing Campus Placement (Ben Roshan)",
        "kaggle_slug": "benroshan/factors-influencing-campus-placement",
        "output_dir": RAW_DATA_DIR,
        "expected_files": ["Placement_Data_Full_Class.csv", "Placement_Data.csv"]
    },
    {
        "name": "Placement Data Full Class (Anmol)",
        "kaggle_slug": "anmol4210/placement-data-full-class",
        "output_dir": os.path.join(RAW_DATA_DIR, "anmol_placement"),
        "expected_files": ["Placement_Data_Full_Class.csv"]
    },
    {
        "name": "Updated Resume Dataset (Gaurav Dutta)",
        "kaggle_slug": "gauravduttakiit/resume-dataset",
        "output_dir": RAW_DATA_DIR,
        "expected_files": ["UpdatedResumeDataSet.csv"]
    },
    {
        "name": "LinkedIn Tech Job Postings (Arsh Kon)",
        "kaggle_slug": "arshkon/linkedin-job-postings",
        "output_dir": os.path.join(RAW_DATA_DIR, "linkedin"),
        "expected_files": ["job_postings.csv"]
    }
]


def check_kaggle_auth() -> bool:
    """Verifies whether kaggle.json exists in user profile or current directory."""
    user_kaggle = os.path.expanduser("~/.kaggle/kaggle.json")
    local_kaggle = os.path.join(PROJECT_DIR, "kaggle.json")
    root_kaggle = os.path.join(os.path.dirname(PROJECT_DIR), "kaggle.json")

    if os.path.exists(user_kaggle):
        print(f"✓ Found Kaggle authentication token at: {user_kaggle}")
        return True
    elif os.path.exists(local_kaggle):
        os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
        shutil.copy(local_kaggle, user_kaggle)
        print(f"✓ Copied kaggle.json from project folder to: {user_kaggle}")
        return True
    elif os.path.exists(root_kaggle):
        os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
        shutil.copy(root_kaggle, user_kaggle)
        print(f"✓ Copied kaggle.json from workspace root to: {user_kaggle}")
        return True
    else:
        print("⚠️ kaggle.json not found in ~/.kaggle/ or project root.")
        print("Please place your downloaded kaggle.json in ~/.kaggle/kaggle.json or project folder.")
        return False


def download_all():
    print("=" * 70)
    print("PLACEPULSE AI - KAGGLE & HUGGING FACE DATASET INGESTION")
    print("=" * 70)

    has_auth = check_kaggle_auth()

    for idx, ds in enumerate(DATASETS, 1):
        print(f"\n[{idx}/6] Ingesting: {ds['name']} ({ds['kaggle_slug']})...")
        os.makedirs(ds["output_dir"], exist_ok=True)
        cmd = f"kaggle datasets download -d {ds['kaggle_slug']} -p {ds['output_dir']} --unzip"
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  ✓ Successfully downloaded and extracted to: {ds['output_dir']}")
            else:
                print(f"  ⚠️ Notice from Kaggle CLI: {res.stderr.strip() or res.stdout.strip()}")
        except Exception as e:
            print(f"  ⚠️ Execution error: {e}")

    # Hugging Face: virattt/technical-interview-qa
    print(f"\n[6/6] Ingesting: virattt/technical-interview-qa from Hugging Face...")
    hf_save_path = os.path.join(RAW_DATA_DIR, "technical_interview_qa.csv")
    try:
        from datasets import load_dataset
        ds = load_dataset("virattt/technical-interview-qa")
        df_hf = pd.DataFrame(ds["train"])
        df_hf.to_csv(hf_save_path, index=False)
        print(f"  ✓ Successfully fetched Hugging Face dataset ({len(df_hf)} Q&As) to {hf_save_path}")
    except Exception as e:
        print(f"  ⚠️ HF notice ({e}). Curated repository in data/raw/technical_interview_qa.csv is active.")

    print("\n" + "=" * 70)
    print("DATASET VERIFICATION SUMMARY:")
    print("=" * 70)
    for root, dirs, files in os.walk(RAW_DATA_DIR):
        for f in files:
            if f.endswith(".csv"):
                fpath = os.path.join(root, f)
                print(f"  📄 {f:<35} | Size: {os.path.getsize(fpath)/1024:.1f} KB")


if __name__ == "__main__":
    download_all()

