import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report

# Add parent directory to sys.path for importing utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.nlp_pipeline import preprocess_text
from dataset.generate_data import main as generate_dataset

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "resumes_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
TRAINED_DIR = os.path.join(BASE_DIR, "trained_model")

def load_data():
    if not os.path.exists(DATASET_PATH):
        print("Dataset not found. Generating synthetic dataset...")
        generate_dataset()
    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded dataset with {len(df)} resumes across {df['category'].nunique()} categories.")
    return df

def train_and_evaluate():
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(TRAINED_DIR, exist_ok=True)
    
    df = load_data()
    
    print("Preprocessing text for ML training...")
    df["processed_text"] = df["resume_text"].apply(preprocess_text)
    
    X = df["processed_text"]
    y = df["category"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Extracting TF-IDF Features...")
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=3500, sublinear_tf=True)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42),
        "Support Vector Machine": CalibratedClassifierCV(LinearSVC(random_state=42, dual="auto")),
        "Naive Bayes": MultinomialNB(alpha=0.1)
    }
    
    metrics_summary = {}
    trained_models = {}
    best_model_name = None
    best_f1 = -1.0
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)
        
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
        
        metrics_summary[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4)
        }
        trained_models[name] = model
        print(f"{name} -> Accuracy: {acc:.4f}, F1-Score: {f1:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name

    print(f"\nBest Model: {best_model_name} with weighted F1-Score of {best_f1:.4f}")
    
    # Save best model and vectorizer
    best_model = trained_models[best_model_name]
    best_model_path = os.path.join(TRAINED_DIR, "best_model.pkl")
    vectorizer_path = os.path.join(TRAINED_DIR, "tfidf_vectorizer.pkl")
    metrics_path = os.path.join(TRAINED_DIR, "model_metrics.json")
    
    joblib.dump(best_model, best_model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    output_metrics = {
        "best_model": best_model_name,
        "categories_count": int(df['category'].nunique()),
        "total_samples": int(len(df)),
        "models": metrics_summary
    }
    
    with open(metrics_path, "w") as f:
        json.dump(output_metrics, f, indent=4)
        
    # Generate visualization chart
    plot_path = os.path.join(MODELS_DIR, "model_comparison.png")
    generate_plots(metrics_summary, plot_path)
    
    print("Training complete. Artifacts saved successfully.")
    return output_metrics

def generate_plots(metrics_summary, save_path):
    names = list(metrics_summary.keys())
    accuracies = [metrics_summary[n]["accuracy"] * 100 for n in names]
    f1_scores = [metrics_summary[n]["f1_score"] * 100 for n in names]
    
    x = np.arange(len(names))
    width = 0.35
    
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    fig, ax = plt.subplots(figsize=(10, 5.5))
    rects1 = ax.bar(x - width/2, accuracies, width, label='Accuracy (%)', color='#4f46e5')
    rects2 = ax.bar(x + width/2, f1_scores, width, label='F1-Score (%)', color='#06b6d4')
    
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_title('Machine Learning Models Comparison', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=11)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 105)
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()
    print(f"Model comparison chart saved to {save_path}")

if __name__ == "__main__":
    train_and_evaluate()
