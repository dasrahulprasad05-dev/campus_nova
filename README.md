# PlacePulse AI 🎓
### B.Tech Campus Placement Predictive Intelligence & Data Science Platform
**Approved Production Blueprint — v1.0.0 (November 2026)**  
*Domain:* B.Tech Engineering Disciplines (CSE, IT, ECE, Mech, Civil, EE)  
*Tech Stack:* Python 3.14 / 3.12, Scikit-Learn, XGBoost, FastAPI, Streamlit, SQLite, Joblib, Pytest

---

## 1. Executive Summary & Platform Identity
**PlacePulse AI** is an applied Machine Learning and Data Science microservice and visual dashboard engineered specifically for B.Tech engineering college students, Training & Placement Officers (TPOs), and technical recruiters.

While traditional campus recruitment depends on static CGPA cutoffs and subjective evaluations, **PlacePulse AI treats placement readiness as a multi-dimensional predictive intelligence problem**:
- Ingests **3,181+ verified Kaggle recruitment records** and **962+ technical resumes** across 25+ tech categories.
- Benchmarks multiple competitive estimators (**Random Forest, XGBoost, Regularized Logistic Regression, Ridge Regression, LinearSVC, Naive Bayes**) with 5-fold cross-validation.
- Delivers real-time placement probability scoring (**94.6% F1-score**), expected CTC salary estimation (**±0.20 LPA MAE**), resume domain screening, and explainable bottleneck diagnosis (**Explainable AI / XAI**).

---

## 2. Platform Architecture & Directory Structure
Housed in an isolated directory (`placepulse_ds_lab/`) to prevent conflict with other campus web portals:

```text
placepulse_ds_lab/
├── data/
│   ├── raw/                          # Kaggle collegePlace.csv, Placement_Data.csv, UpdatedResumeDataSet.csv
│   ├── processed/                    # Cleaned, encoded, and train/test split CSVs
│   └── placepulse.db                 # Relational SQLite database
├── notebooks/                        # Publication & Viva-ready Jupyter Notebooks
│   ├── 01_placement_eda_and_cleaning.ipynb
│   ├── 02_placement_models_comparison.ipynb
│   ├── 03_resume_nlp_classification.ipynb
│   └── build_notebooks.py
├── src/                              # Production Data Science Pipeline Scripts
│   ├── data_loader.py                # Dataset download, validation & ingestion
│   ├── feature_engineering.py        # Scalers, categorical encoders, TF-IDF vectorizer
│   ├── train_classifier.py           # Multi-model placement classification & comparison
│   ├── train_regressor.py            # CTC salary regression pipeline
│   ├── train_nlp.py                  # Resume text classification model
│   └── explainability.py             # Feature importance and at-risk diagnostics
├── models/                           # Exported Production Binaries (.joblib & .json)
│   ├── placement_classifier.joblib
│   ├── placement_pipeline.joblib
│   ├── salary_regressor.joblib
│   ├── salary_pipeline.joblib
│   ├── resume_classifier.joblib
│   ├── resume_tfidf.joblib
│   ├── resume_label_encoder.joblib
│   ├── classifier_benchmarks.json
│   ├── regressor_benchmarks.json
│   └── nlp_benchmarks.json
├── api/                              # Asynchronous FastAPI Microservice
│   ├── main.py                       # REST API routes and eager lifespan loader
│   ├── schemas.py                    # Pydantic v2 data models
│   └── database.py                   # SQLite ORM connection & table creation
├── app/                              # Streamlit Interactive Presentation UI
│   ├── app.py                        # Streamlit main entrypoint
│   └── components/                   # UI helpers, PDF parsers, and matplotlib renderers
├── tests/                            # Automated Pytest Suite & Regression Tests
│   ├── test_api_and_models.py
│   └── verify_endpoints.py
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation & viva defense guide
```

---

## 3. The 7-Step Data Science Lifecycle
1. **Dataset Acquisition:** Kaggle Engineering College Placement (2,966 records), Ben Roshan Campus Recruitment (215 records), Gaurav Dutta Resumes (962 records), and Technical Interview Q&A.
2. **Data Preprocessing & EDA:** Missing salary value imputation for unplaced records, outlier checks, categorical encoding of engineering disciplines, and correlation matrices.
3. **Feature Engineering:** Continuous standardization with `StandardScaler`, interaction term formulation ($Interaction = CGPA \times (Internships + 1)$), and sublinear TF-IDF vectorization (1,500 features, n-gram=(1,2)).
4. **Multi-Model Benchmark Training:** Stratified 80/20 train-test splits evaluated using 5-fold cross-validation.
5. **Rigorous Model Evaluation:** Selected winning algorithms based on F1-score, ROC-AUC, and MAE.
6. **Model Serialization:** Exported production `.joblib` binaries with schema versioning.
7. **Production Inference & UI:** FastAPI asynchronous REST microservice + Streamlit interactive dashboard with live What-If scenario simulations.

---

## 4. Benchmark Performance Leaderboard

### Placement Probability Classifier (Binary Classification)
| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (L2 Baseline)** | **92.59%** | **94.40%** | **94.87%** | **94.63%** | **0.9838** | 🏆 **Production Active** |
| **Gradient Boosting** | 91.92% | 94.13% | 94.13% | 94.13% | 0.9789 | Candidate |
| **XGBoost Classifier** | 91.58% | 93.25% | 94.62% | 93.93% | 0.9814 | Candidate |
| **Random Forest (100 trees)** | 91.41% | 93.24% | 94.38% | 93.80% | 0.9794 | Candidate |
| **Decision Tree (max_depth=6)** | 90.91% | 93.83% | 92.91% | 93.37% | 0.9631 | Baseline |

### CTC Expected Salary Regressor (in LPA)
| Model | Test MAE | Test RMSE | R² Score | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Ridge Regression ($\alpha=1.0$)** | **0.2044 LPA** | **0.2415 LPA** | **0.7933** | 🏆 **Production Active** |
| **Linear Regression (OLS)** | 0.2062 LPA | 0.2441 LPA | 0.7890 | Candidate |
| **Random Forest Regressor** | 0.2337 LPA | 0.2889 LPA | 0.7043 | Candidate |
| **Gradient Boosting Regressor** | 0.2580 LPA | 0.2982 LPA | 0.6851 | Candidate |

### Technical Resume Domain Classifier (25+ Roles)
| Model | Accuracy | Macro F1 | Weighted F1 | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Support Vector Classifier (LinearSVC)** | **100.0%** | **1.0000** | **1.0000** | 🏆 **Production Active** |
| **Multinomial Naive Bayes** | 100.0% | 1.0000 | 1.0000 | Candidate |
| **Multinomial Logistic Regression** | 100.0% | 1.0000 | 1.0000 | Candidate |

---

## 5. REST API Specifications (FastAPI)

Interactive Swagger / OpenAPI UI: `http://localhost:8000/docs`

| Method | Endpoint Route | Request Body | Response Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/health` | None | Service status, active production model names, version |
| `POST` | `/api/v1/predict/placement` | `{ stream, cgpa, internships, backlogs, student_name? }` | Placed verdict, probability score, confidence rating, DB reference ID |
| `POST` | `/api/v1/predict/salary` | `{ cgpa, aptitude_score, internships, stream? }` | Expected CTC (LPA), 95% confidence interval `[min, max]` |
| `POST` | `/api/v1/nlp/resume-screen` | `{ resume_text, candidate_name?, target_role? }` | Predicted tech role, confidence, matched skills, missing prerequisites |
| `POST` | `/api/v1/explain/at-risk` | `{ stream, cgpa, internships, backlogs }` | Risk score, attribution penalties, prescriptive remediation checklist |
| `GET` | `/api/v1/analytics/eda-metrics`| None | Branch-wise placement rates, salary quartiles, feature correlations |
| `POST` | `/api/v1/interview/questions` | `{ role, stream }` | Curated DSA, systems, and branch interview questions & answers |
| `GET` | `/api/v1/predictions/history` | `limit: int = 50` | Recent logged placement predictions from SQLite |
| `GET` | `/api/v1/benchmarks` | None | Registered multi-model benchmark leaderboard |

---

## 6. Relational Database Schema (`data/placepulse.db`)

PlacePulse AI automatically manages 3 relational SQLite tables:
1. `placement_predictions`: Tracks candidate name, stream, CGPA, internships, backlogs, aptitude, placement verdict, probability, predicted CTC, model version, and timestamp.
2. `resume_evaluations`: Stores raw snippet, predicted domain, confidence, detected skills (JSON array), missing skills (JSON array), and candidate details.
3. `model_benchmark_registry`: Stores model name, task type (`classification`, `regression`, `nlp`), accuracy, F1-score, ROC-AUC, MAE, active flag, and training timestamp.

---

## 7. Quickstart Guide: Running the Microservice & UI

### Step 1: Install Dependencies
```bash
pip install -r placepulse_ds_lab/requirements.txt
```

### Step 2: Ingest Data & Train Pipelines (Optional if joblib exists)
```bash
python placepulse_ds_lab/src/data_loader.py
python placepulse_ds_lab/src/train_classifier.py
python placepulse_ds_lab/src/train_regressor.py
python placepulse_ds_lab/src/train_nlp.py
```

### Step 3: Launch Asynchronous FastAPI Microservice
```bash
uvicorn api.main:app --app-dir placepulse_ds_lab --host 127.0.0.1 --port 8000 --reload
```
Navigate to: `http://127.0.0.1:8000/docs` to test live endpoints via Swagger.

### Step 4: Launch Interactive Streamlit Visual Dashboard
```bash
streamlit run placepulse_ds_lab/app/app.py
```
Open your browser at: `http://localhost:8501`.

### Step 5: Execute Automated Pytest Test Suite
```bash
python -m pytest placepulse_ds_lab/tests/test_api_and_models.py -v
```

---

## 8. Academic Viva Presentation & Defense Pitch
*Quick reference notes for academic defense, viva voce, and technical reviewer queries:*

1. **Why treat placement readiness as a regression/classification problem?**  
   Standard placement cutoffs look strictly at CGPA. PlacePulse AI proves through correlation analysis ($r = 0.58$) and non-linear interactions ($CGPA \times Internships$) that practical industry experience can compensate for moderate academic marks and dramatically alter the shortlisting boundary.
2. **Why evaluate multiple algorithms instead of picking one?**  
   Following strict Data Science lifecycle methodology, we benchmark linear vs non-linear vs tree ensemble algorithms. L2-regularized logistic regression and Ridge regression achieved the lowest generalization error and highest F1-scores without overfitting the benchmark splits.
3. **How does the Explainable AI (XAI) engine work?**  
   Rather than presenting a black-box decision, our explainer isolates marginal contributions ($p_{base} - p_{perturbed}$) to compute exact penalty percentages for active backlogs and zero-internship profiles, providing students with transparent, prescriptive guidance.
4. **How are skills extracted from resumes?**  
   The NLP pipeline combines sublinear TF-IDF vectorization (1,500 features across unigrams and bigrams) for domain classification with deterministic regex boundary matching against a curated 25+ domain industry taxonomy to detect competencies and identify missing prerequisites.

