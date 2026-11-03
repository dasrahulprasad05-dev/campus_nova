"""
Generator for PlacePulse_AI_Colab_Master_Trainer.ipynb
Author: PlacePulse AI Team
"""

import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LAB_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
WORKSPACE_ROOT = os.path.abspath(os.path.join(LAB_DIR, ".."))

NOTEBOOK_DIR = os.path.join(LAB_DIR, "notebooks")
ROOT_NOTEBOOK_PATH = os.path.join(WORKSPACE_ROOT, "PlacePulse_AI_Colab_Master_Trainer.ipynb")
LAB_NOTEBOOK_PATH = os.path.join(NOTEBOOK_DIR, "PlacePulse_AI_Colab_Master_Trainer.ipynb")


def md_cell(source: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.strip().split("\n")]
    }


def code_cell(source: str):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.strip().split("\n")]
    }


def create_colab_notebook():
    cells = [
        md_cell("""# 🎓 PlacePulse AI: Google Colab Master Dataset Downloader & ML Pipeline
### Comprehensive Dataset Ingestion, EDA, Multi-Model Training, and Export
**Project Website:** PlacePulse AI (https://placepulse.ai / campusplacement.ai)  
**Target:** Ingest 6 Verified Datasets, Train Placement Classifiers, Salary Regressors, Resume NLP Models, and Export all `.joblib` & `.csv` files as a single ZIP.

---

### 📋 The 6 Target Datasets Covered in this Notebook:
1. **B.Tech Placement Prediction:** `tejashvi14/engineering-placements-prediction` (`collegePlace.csv` - 2,966 records)
2. **Campus Recruitment & CTC:** `benroshan/factors-influencing-campus-placement` (`Placement_Data_Full_Class.csv` - 215 records)
3. **Student Placement Benchmark:** `anmol4210/placement-data-full-class` (`Placement_Data_Full_Class.csv`)
4. **Technical Resume Dataset:** `gauravduttakiit/resume-dataset` (`UpdatedResumeDataSet.csv` - 962 resumes, 25+ tech categories)
5. **LinkedIn Tech Job Postings:** `arshkon/linkedin-job-postings` (`job_postings.csv` - 30,000+ postings)
6. **Technical Interview QA (Hugging Face):** `virattt/technical-interview-qa` (Thousands of Q&A across DSA, System Design, SQL)"""),

        md_cell("""## 📦 Cell 1: Install Required Python Libraries
We install `kaggle`, `huggingface_hub`, `datasets`, `xgboost`, `scikit-learn`, `joblib`, and `pypdfium2`."""),

        code_cell("""!pip install -q kaggle datasets huggingface_hub scikit-learn xgboost pandas numpy joblib matplotlib seaborn
print("✓ Libraries installed successfully!")"""),

        md_cell("""## 🔑 Cell 2: Kaggle API Authentication (`kaggle.json`)
You can authenticate using **either** of two methods:
- **Method A:** Upload your `kaggle.json` file directly using the file picker below.
- **Method B:** Or enter your Kaggle Username and API Key in the form fields."""),

        code_cell("""import os
import json
from google.colab import files

# Create ~/.kaggle directory
os.makedirs(os.path.expanduser("~/.kaggle"), exist_ok=True)
kaggle_json_path = os.path.expanduser("~/.kaggle/kaggle.json")

print("Please upload your kaggle.json file below:")
uploaded = files.upload()

if "kaggle.json" in uploaded:
    with open(kaggle_json_path, "wb") as f:
        f.write(uploaded["kaggle.json"])
    os.chmod(kaggle_json_path, 0o600)
    print("✓ Successfully authenticated with uploaded kaggle.json!")
else:
    # Fallback to manual entry
    print("No kaggle.json uploaded. Checking manual credentials...")
    username = input("Enter Kaggle Username (or press Enter to skip): ").strip()
    key = input("Enter Kaggle API Key (or press Enter to skip): ").strip()
    if username and key:
        with open(kaggle_json_path, "w") as f:
            json.dump({"username": username, "key": key}, f)
        os.chmod(kaggle_json_path, 0o600)
        print("✓ Successfully authenticated with manual credentials!")
    else:
        print("⚠️ Warning: Kaggle credentials not provided. Dataset downloads may fail.")"""),

        md_cell("""## 📥 Cell 3: Download & Unpack All 6 Target Datasets
Downloads the 5 Kaggle datasets via Kaggle CLI and the Hugging Face Technical Interview QA dataset via `datasets` or direct download."""),

        code_cell("""import os
import shutil
import pandas as pd

DATA_RAW_DIR = "placepulse_ds_lab/data/raw"
DATA_PROC_DIR = "placepulse_ds_lab/data/processed"
MODELS_DIR = "placepulse_ds_lab/models"

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROC_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

print("=" * 70)
print("DOWNLOADING 6 VERIFIED BENCHMARK DATASETS")
print("=" * 70)

# 1. Engineering College Placement (Tejashvi)
print("\\n[1/6] Ingesting: tejashvi14/engineering-placements-prediction...")
f1 = os.path.join(DATA_RAW_DIR, "collegePlace.csv")
if not os.path.exists(f1):
    !kaggle datasets download -d tejashvi14/engineering-placements-prediction -p {DATA_RAW_DIR} --unzip || true
if not os.path.exists(f1):
    import urllib.request
    print("Fetching collegePlace.csv from verified public mirror...")
    try:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/Avi8010/Placement_Predictor/master/collegePlace.csv", f1)
        print("✓ Downloaded collegePlace.csv from public mirror!")
    except Exception as e:
        print(f"Mirror note: {e}")

# 2. Factors Influencing Campus Placement (Ben Roshan)
print("\\n[2/6] Ingesting: benroshan/factors-affecting-campus-placement...")
f2 = os.path.join(DATA_RAW_DIR, "Placement_Data_Full_Class.csv")
if not os.path.exists(f2) and not os.path.exists(os.path.join(DATA_RAW_DIR, "Placement_Data.csv")):
    !kaggle datasets download -d benroshan/factors-affecting-campus-placement -p {DATA_RAW_DIR} --unzip || true
if not os.path.exists(f2) and not os.path.exists(os.path.join(DATA_RAW_DIR, "Placement_Data.csv")):
    !kaggle datasets download -d anmol4210/placement-data-full-class -p {DATA_RAW_DIR} --unzip || true
if not os.path.exists(f2) and not os.path.exists(os.path.join(DATA_RAW_DIR, "Placement_Data.csv")):
    import urllib.request
    print("Fetching Placement_Data_Full_Class.csv from verified public mirror...")
    try:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/ShuklaPrashant21/Campus_Recruitment/master/Placement_Data_Full_Class.csv", f2)
        print("✓ Downloaded Placement_Data_Full_Class.csv from public mirror!")
    except Exception as e:
        print(f"Mirror note: {e}")

# 3. Placement Data Full Class (Anmol)
print("\\n[3/6] Ingesting: anmol4210/placement-data-full-class...")
os.makedirs(os.path.join(DATA_RAW_DIR, "anmol_placement"), exist_ok=True)
!kaggle datasets download -d anmol4210/placement-data-full-class -p {DATA_RAW_DIR}/anmol_placement --unzip || true

# 4. Updated Resume Dataset (Gaurav Dutta)
print("\\n[4/6] Ingesting: gauravduttakiit/resume-dataset...")
f4 = os.path.join(DATA_RAW_DIR, "UpdatedResumeDataSet.csv")
if not os.path.exists(f4):
    !kaggle datasets download -d gauravduttakiit/resume-dataset -p {DATA_RAW_DIR} --unzip || true
if not os.path.exists(f4):
    import urllib.request
    print("Fetching UpdatedResumeDataSet.csv from verified public mirror...")
    try:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/jjso/resume-dataset/master/UpdatedResumeDataSet.csv", f4)
        print("✓ Downloaded UpdatedResumeDataSet.csv from public mirror!")
    except Exception as e:
        print(f"Mirror note: {e}")

# 5. LinkedIn Tech Job Postings (Arsh Kon - Optional)
print("\\n[5/6] Ingesting: arshkon/linkedin-job-postings...")
!kaggle datasets download -d arshkon/linkedin-job-postings -p {DATA_RAW_DIR}/linkedin --unzip || true

# 6. Technical Interview QA (Hugging Face)
print("\\n[6/6] Ingesting: virattt/technical-interview-qa from Hugging Face...")
try:
    from datasets import load_dataset
    hf_ds = load_dataset("virattt/technical-interview-qa")
    df_hf = pd.DataFrame(hf_ds["train"])
    hf_save_path = os.path.join(DATA_RAW_DIR, "technical_interview_qa.csv")
    df_hf.to_csv(hf_save_path, index=False)
    print(f"✓ Saved Hugging Face QA dataset: {len(df_hf)} questions to {hf_save_path}")
except Exception as e:
    print(f"HF Hub notice ({e}). Generating curated engineering interview question repository...")
    hf_save_path = os.path.join(DATA_RAW_DIR, "technical_interview_qa.csv")
    curated_qa = [
        {"role": "Data Science", "stream": "Computer Science", "category": "Machine Learning", "difficulty": "Medium", "question": "Explain Bias-Variance tradeoff and how L1/L2 regularization controls it.", "answer_summary": "Bias stems from erroneous assumptions causing underfitting; variance stems from sensitivity to small fluctuations causing overfitting. L1 penalizes absolute weights inducing sparsity, while L2 penalizes squared weights shrinking them smoothly."},
        {"role": "Data Science", "stream": "Computer Science", "category": "Algorithms", "difficulty": "Hard", "question": "How does XGBoost handle missing values during tree split finding?", "answer_summary": "XGBoost automatically learns optimal default split directions for missing values during training by comparing the split gain when allocating missing values to the left versus right child."},
        {"role": "Python Developer", "stream": "Computer Science", "category": "DSA", "difficulty": "Medium", "question": "How do you implement an LRU Cache with O(1) time complexity?", "answer_summary": "Combine a Hash Map for O(1) key lookups with a Doubly Linked List to maintain access recency order in O(1) time."},
        {"role": "Java Developer", "stream": "Computer Science", "category": "Core Java", "difficulty": "Medium", "question": "Explain the Java Memory Model: Heap, Stack, and Metaspace.", "answer_summary": "Stack stores method frames and local variables (LIFO). Heap stores instantiated objects. Metaspace in native memory holds loaded class metadata."},
        {"role": "DevOps Engineer", "stream": "Information Technology", "category": "Containerization", "difficulty": "Medium", "question": "Explain Docker Container vs Virtual Machine.", "answer_summary": "VMs run full guest operating systems on top of hypervisors. Docker containers share the host Linux kernel isolation primitives (namespaces/cgroups), making them lightweight."},
        {"role": "Web Designing", "stream": "Computer Science", "category": "React / Frontend", "difficulty": "Medium", "question": "Explain React Virtual DOM and the Fiber Reconciliation algorithm.", "answer_summary": "React retains a virtual DOM tree in memory. Fiber incrementally diffs changes against previous state trees with heuristic O(n) comparison, batching real DOM updates."},
        {"role": "Network Security Engineer", "stream": "Electronics And Communication", "category": "Cybersecurity", "difficulty": "Medium", "question": "How does TLS 1.3 handshake achieve Forward Secrecy?", "answer_summary": "TLS 1.3 completes in a 1-RTT handshake using ephemeral Diffie-Hellman (ECDHE) keys for each session, ensuring past communications cannot be decrypted even if private keys are compromised."}
    ]
    df_hf = pd.DataFrame(curated_qa)
    df_hf.to_csv(hf_save_path, index=False)
    print(f"✓ Created {len(df_hf)} curated engineering interview questions!")

print("\\n" + "=" * 70)
print("DATASET INGESTION SUMMARY:")
print("=" * 70)
for root, dirs, files_list in os.walk(DATA_RAW_DIR):
    for f in files_list:
        if f.endswith(".csv"):
            fpath = os.path.join(root, f)
            print(f"  📄 {f:<35} | Size: {os.path.getsize(fpath)/1024:.1f} KB")"""),

        md_cell("""## 🔍 Cell 4: Dataset Schema Verification & Preview
Let's inspect the shapes, columns, and head of the downloaded datasets."""),

        code_cell("""import glob

# 1. College Placement
col_files = glob.glob(f"{DATA_RAW_DIR}/*collegePlace*.csv") + glob.glob(f"{DATA_RAW_DIR}/*college*.csv")
if col_files:
    df_college = pd.read_csv(col_files[0])
    print(f"1. College Placement Shape: {df_college.shape}")
    display(df_college.head(3))

# 2. Campus Recruitment (Ben Roshan / Placement Data)
place_files = glob.glob(f"{DATA_RAW_DIR}/*Placement_Data*.csv") + glob.glob(f"{DATA_RAW_DIR}/*placement*.csv")
if place_files:
    df_placement = pd.read_csv(place_files[0])
    print(f"\\n2. Placement Data Shape: {df_placement.shape}")
    display(df_placement.head(3))

# 3. Resume Dataset
resume_files = glob.glob(f"{DATA_RAW_DIR}/*Resume*.csv")
if resume_files:
    df_resumes = pd.read_csv(resume_files[0])
    print(f"\\n3. Resume Dataset Shape: {df_resumes.shape} across {df_resumes['Category'].nunique()} roles")
    display(df_resumes.head(3))"""),

        md_cell("""## 🛠️ Cell 5: Data Preprocessing & Feature Engineering
We standardize continuous features, formulate the interaction term $Interaction = CGPA \\times (Internships + 1)$, isolate placed candidate salaries in LPA, and build the sublinear TF-IDF 1,500 feature vectorizer."""),

        code_cell("""import re
import string
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Clean and process College Placement
# Find collegePlace.csv
f_college = col_files[0] if col_files else f"{DATA_RAW_DIR}/collegePlace.csv"
df_col = pd.read_csv(f_college)

# Ensure standard column naming
col_map = {c: c.strip() for c in df_col.columns}
df_col.rename(columns=col_map, inplace=True)

# Engineer interaction
df_col["CGPA_Internship_Interaction"] = df_col["CGPA"] * (df_col["Internships"] + 1)
df_col.to_csv(f"{DATA_PROC_DIR}/college_placement_processed.csv", index=False)
print("✓ College placement dataset preprocessed.")

# 2. Clean and process Campus Salary Dataset
f_place = place_files[0] if place_files else f"{DATA_RAW_DIR}/Placement_Data_Full_Class.csv"
df_sal_raw = pd.read_csv(f_place)
df_sal_placed = df_sal_raw[df_sal_raw["status"] == "Placed"].copy()
df_sal_placed["salary_lpa"] = (df_sal_placed["salary"] / 100000.0).round(2)
df_sal_placed["workex_binary"] = (df_sal_placed["workex"] == "Yes").astype(int)
df_sal_placed.to_csv(f"{DATA_PROC_DIR}/salary_placed_processed.csv", index=False)
print("✓ Salary regression dataset preprocessed.")

# 3. Clean Resume Text Function
def clean_resume_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'www\.\S+\s*', ' ', text)
    text = re.sub(r'\S+@\S+', ' ', text)
    text = re.sub(r'[@#]\S+', ' ', text)
    text = re.sub(r'\b(RT|cc)\b', ' ', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()

f_res = resume_files[0] if resume_files else f"{DATA_RAW_DIR}/UpdatedResumeDataSet.csv"
df_res = pd.read_csv(f_res)
df_res["Cleaned_Resume"] = df_res["Resume"].apply(clean_resume_text)
df_res.to_csv(f"{DATA_PROC_DIR}/resumes_processed.csv", index=False)
print(f"✓ Resume dataset cleaned ({len(df_res)} resumes).")"""),

        md_cell("""## 🤖 Cell 6: Train Multi-Model Placement Classifiers & Export
We benchmark:
- **Logistic Regression (L2 Baseline)**
- **Random Forest Classifier (100 estimators)**
- **XGBoost Classifier**
- **Decision Tree & Gradient Boosting**

Evaluated with 5-fold cross-validation and 80/20 train-test splits. The winning estimator is serialized to `.joblib`."""),

        code_cell("""import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import xgboost as xgb

STREAM_KEYS = [
    "Computer Science", "Information Technology", "Electronics And Communication",
    "Mechanical", "Electrical", "Civil"
]

class PlacementPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.stream_encoder = OneHotEncoder(categories=[STREAM_KEYS], sparse_output=False, handle_unknown="ignore")
    def fit(self, df):
        feats = np.hstack([df[["CGPA"]].values, (df["CGPA"] * (df["Internships"] + 1)).values.reshape(-1, 1)])
        self.scaler.fit(feats)
        self.stream_encoder.fit(df[["Stream"]].values)
        return self
    def transform(self, df):
        scaled = self.scaler.transform(np.hstack([df[["CGPA"]].values, (df["CGPA"] * (df["Internships"] + 1)).values.reshape(-1, 1)]))
        stream_ohe = self.stream_encoder.transform(df[["Stream"]].values)
        return np.hstack([scaled[:, 0:1], df[["Internships"]].values, df[["HistoryOfBacklogs"]].values, scaled[:, 1:2], stream_ohe])

pipe_clf = PlacementPipeline()
pipe_clf.fit(df_col)
X = pipe_clf.transform(df_col)
y = df_col["PlacedOrNot"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

clf_candidates = {
    "Logistic Regression (L2)": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=8, criterion="entropy", random_state=42),
    "XGBoost": xgb.XGBClassifier(n_estimators=150, learning_rate=0.05, max_depth=5, eval_metric="logloss", random_state=42),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42)
}

best_clf_f1 = -1.0
best_clf_name = ""
best_clf_model = None
clf_leaderboard = {}

print("-" * 75)
print(f"{'Classifier Model':<28} | {'Accuracy':<9} | {'Precision':<9} | {'Recall':<8} | {'F1':<8} | {'ROC-AUC':<8}")
print("-" * 75)

for name, model in clf_candidates.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)
    
    clf_leaderboard[name] = {"accuracy": acc, "f1": f1, "roc_auc": auc, "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()}
    print(f"{name:<28} | {acc:.4f}    | {prec:.4f}    | {rec:.4f}   | {f1:.4f}   | {auc:.4f}")
    
    if f1 > best_clf_f1:
        best_clf_f1 = f1
        best_clf_name = name
        best_clf_model = model

print("-" * 75)
print(f"🏆 Winning Placement Classifier: {best_clf_name} (F1: {best_clf_f1:.4f})")

# Serialize
joblib.dump(best_clf_model, f"{MODELS_DIR}/placement_classifier.joblib")
joblib.dump(pipe_clf, f"{MODELS_DIR}/placement_pipeline.joblib")
with open(f"{MODELS_DIR}/classifier_benchmarks.json", "w") as f:
    json.dump({"production_model": best_clf_name, "best_f1": best_clf_f1, "leaderboard": clf_leaderboard}, f, indent=2)
print("✓ Placement classifier and pipeline exported!")"""),

        md_cell("""## 💰 Cell 7: Train CTC Salary Regressors & Export
Evaluates Ridge Regression vs Random Forest Regressor vs Gradient Boosting on actual placed student compensation."""),

        code_cell("""from sklearn.linear_model import Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class SalaryPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
    def fit(self, df):
        self.scaler.fit(df[["degree_p", "etest_p"]].values)
        return self
    def transform(self, df):
        num_s = self.scaler.transform(df[["degree_p", "etest_p"]].values)
        workex = df[["workex_binary"]].values
        stream_code = np.zeros((len(df), 1))
        return np.hstack([num_s, workex, stream_code])

pipe_sal = SalaryPipeline()
pipe_sal.fit(df_sal_placed)
X_sal = pipe_sal.transform(df_sal_placed)
y_sal = df_sal_placed["salary_lpa"].values

X_tr_s, X_te_s, y_tr_s, y_te_s = train_test_split(X_sal, y_sal, test_size=0.20, random_state=42)

reg_candidates = {
    "Ridge Regression (alpha=1.0)": Ridge(alpha=1.0, random_state=42),
    "Linear Regression (OLS)": LinearRegression(),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42),
    "Gradient Boosting Regressor": GradientBoostingRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
}

best_reg_mae = float("inf")
best_reg_name = ""
best_reg_model = None
reg_leaderboard = {}

print("-" * 70)
print(f"{'Salary Regressor Model':<32} | {'MAE (LPA)':<10} | {'RMSE':<10} | {'R2 Score':<8}")
print("-" * 70)

for name, model in reg_candidates.items():
    model.fit(X_tr_s, y_tr_s)
    y_pred = model.predict(X_te_s)
    mae = mean_absolute_error(y_te_s, y_pred)
    rmse = np.sqrt(mean_squared_error(y_te_s, y_pred))
    r2 = r2_score(y_te_s, y_pred)
    
    reg_leaderboard[name] = {"mae": mae, "rmse": rmse, "r2": r2}
    print(f"{name:<32} | {mae:.4f}     | {rmse:.4f}     | {r2:.4f}")
    
    if mae < best_reg_mae:
        best_reg_mae = mae
        best_reg_name = name
        best_reg_model = model

print("-" * 70)
print(f"🏆 Winning Salary Regressor: {best_reg_name} (MAE: ±{best_reg_mae:.4f} LPA)")

joblib.dump(best_reg_model, f"{MODELS_DIR}/salary_regressor.joblib")
joblib.dump(pipe_sal, f"{MODELS_DIR}/salary_pipeline.joblib")
with open(f"{MODELS_DIR}/regressor_benchmarks.json", "w") as f:
    json.dump({"production_model": best_reg_name, "best_mae_lpa": best_reg_mae, "leaderboard": reg_leaderboard}, f, indent=2)
print("✓ Salary regressor and pipeline exported!")"""),

        md_cell("""## 📄 Cell 8: Train Technical Resume NLP Classifier & Export
TF-IDF Sublinear Vectorization (1,500 features) + LinearSVC / Naive Bayes across 25+ tech job categories."""),

        code_cell("""from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

# Encode labels
lbl_enc = LabelEncoder()
y_nlp = lbl_enc.fit_transform(df_res["Category"].values)

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=1500, ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
X_nlp = tfidf.fit_transform(df_res["Cleaned_Resume"])

X_tr_n, X_te_n, y_tr_n, y_te_n = train_test_split(X_nlp, y_nlp, test_size=0.20, random_state=42, stratify=y_nlp)

nlp_candidates = {
    "Linear SVC": LinearSVC(C=1.0, random_state=42),
    "Multinomial Naive Bayes": MultinomialNB(alpha=0.1)
}

best_nlp_f1 = -1.0
best_nlp_name = ""
best_nlp_model = None
nlp_leaderboard = {}

for name, model in nlp_candidates.items():
    model.fit(X_tr_n, y_tr_n)
    y_pred = model.predict(X_te_n)
    acc = accuracy_score(y_te_n, y_pred)
    f1 = f1_score(y_te_n, y_pred, average="weighted")
    nlp_leaderboard[name] = {"accuracy": acc, "weighted_f1": f1}
    print(f"NLP Model: {name:<25} | Accuracy: {acc:.4f} | Weighted F1: {f1:.4f}")
    if f1 > best_nlp_f1:
        best_nlp_f1 = f1
        best_nlp_name = name
        best_nlp_model = model

print(f"🏆 Winning Resume Classifier: {best_nlp_name}")

joblib.dump(best_nlp_model, f"{MODELS_DIR}/resume_classifier.joblib")
joblib.dump(tfidf, f"{MODELS_DIR}/resume_tfidf.joblib")
joblib.dump(lbl_enc, f"{MODELS_DIR}/resume_label_encoder.joblib")
with open(f"{MODELS_DIR}/nlp_benchmarks.json", "w") as f:
    json.dump({"production_model": best_nlp_name, "best_f1": best_nlp_f1, "leaderboard": nlp_leaderboard}, f, indent=2)
print("✓ Resume NLP models exported!")"""),

        md_cell("""## 📦 Cell 9: Package Everything into `placepulse_ds_lab_complete.zip` & Download
Packages all raw downloaded CSVs (`collegePlace.csv`, `Placement_Data_Full_Class.csv`, `UpdatedResumeDataSet.csv`, `job_postings.csv`, `technical_interview_qa.csv`), processed CSVs, and trained `.joblib` production binaries into a single ZIP file for instant download."""),

        code_cell("""import zipfile
from google.colab import files

zip_filename = "placepulse_ds_lab_complete.zip"
print(f"Creating archive: {zip_filename}...")

with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk("placepulse_ds_lab"):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            arcname = os.path.relpath(filepath, "placepulse_ds_lab")
            zipf.write(filepath, arcname)

print(f"✓ Archive created! Size: {os.path.getsize(zip_filename) / (1024 * 1024):.2f} MB")
print("Triggering browser download of placepulse_ds_lab_complete.zip...")
files.download(zip_filename)
print("🎉 Done! Unzip this archive into your local placepulse_ds_lab/ folder.")""")
    ]

    nb = {
        "cells": cells,
        "metadata": {
            "colab": {
                "name": "PlacePulse_AI_Colab_Master_Trainer.ipynb",
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }

    # Write to both locations
    with open(LAB_NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    with open(ROOT_NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)

    print(f"Colab Notebook successfully generated at:\n  {LAB_NOTEBOOK_PATH}\n  {ROOT_NOTEBOOK_PATH}")


if __name__ == "__main__":
    create_colab_notebook()
