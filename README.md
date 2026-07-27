<<<<<<< HEAD
# AI Resume Screening & Candidate Ranking System

An end-to-end AI-powered recruitment platform designed to parse candidate resumes (PDF, DOCX), compute multi-dimensional matching scores using NLP & Machine Learning, identify skill gaps, and rank applicants for technical and corporate job roles.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-black)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

---

## 🌟 Key Features

* **📄 Document Parsing**: Automatic extraction of text, contact info (Email, Phone), education, work history, and candidate skills from PDF, DOCX, and TXT files.
* **🧠 Multi-Criteria Candidate Scoring Engine**:
  * **TF-IDF & Cosine Similarity (40%)**: Statistical text overlap analysis between job descriptions and resume text.
  * **Weighted Skill Match (40%)**: Case-insensitive comparison of extracted skills against required job competencies.
  * **Machine Learning Categorization (20%)**: Multi-class text classifier confidence scoring trained on 600 resumes across 25 job domains.
* **📊 Machine Learning Model Comparison**: Benchmarks Logistic Regression, Random Forest, Support Vector Machine (Linear SVM), and Naive Bayes classifiers with automated performance metrics (Accuracy, Precision, Recall, F1-Score).
* **💎 Glassmorphism UI/UX**: Dark mode layout with indigo accents, micro-animations, Plotly.js charts, and responsive Bootstrap 5 design.
* **📥 Multi-Format Reports**: Automated generation of candidate ranking reports in **PDF (ReportLab)**, **Excel (OpenPyXL)**, and **CSV**.

---

## 📁 Architecture & Folder Structure

```
ai-resume-screening/
├── app.py                      # Main Flask Web Application
├── requirements.txt            # Package Dependencies
├── README.md                   # System Documentation
│
├── database/
│   ├── database.db             # SQLite Database
│   ├── schema.sql              # SQL Table Schema
│   └── db_helper.py            # SQLite CRUD & Stats Helper
│
├── dataset/
│   ├── generate_data.py        # Dataset Generator (600 resumes, 25 categories)
│   └── resumes_dataset.csv     # Synthetic Resume Dataset
│
├── models/
│   ├── train_model.py          # Machine Learning Classifier Training Script
│   └── model_comparison.png    # Benchmarks Plot
│
├── trained_model/
│   ├── best_model.pkl          # Saved Best Classifier
│   ├── tfidf_vectorizer.pkl    # Saved TF-IDF Vectorizer
│   └── model_metrics.json      # Saved Performance Metrics
│
├── utils/
│   ├── nlp_pipeline.py         # NLTK/spaCy Text Cleaning & Lemmatization
│   ├── resume_parser.py        # PDF/DOCX Parsing & Entity Extraction
│   ├── report_generator.py     # PDF, Excel, and CSV Exporters
│   └── visualizations.py       # Plotly & Matplotlib Data Preprocessors
│
├── templates/                  # Jinja2 HTML Templates
├── static/                     # CSS & JS Assets
└── tests/
    └── test_pipeline.py        # Automated Test Suite
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Setup Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Generate Dataset & Train Machine Learning Models
```bash
python dataset/generate_data.py
python models/train_model.py
```

### 4. Run Automated Test Verification
```bash
python tests/test_pipeline.py
```

### 5. Launch Application
```bash
python app.py
```
Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## 📐 Scoring Formula

$$\text{Final Candidate Score (\%)} = (0.40 \times \text{Cosine Sim}) + (0.40 \times \text{Skill Match}) + (0.20 \times \text{ML Probability}) \times 100$$

* 🟢 **Highly Recommended**: Score $\ge 80\%$
* 🟡 **Recommended**: $60\% \le \text{Score} < 80\%$
* 🔴 **Not Recommended**: Score $< 60\%$
=======
# AI-resume-screening
>>>>>>> 7b683ed15349e9359a8cc176080201cc062360dc
