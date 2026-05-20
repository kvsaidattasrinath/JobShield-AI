import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


# -----------------------------
# LOAD DATASET
# -----------------------------
df = pd.read_csv("data/fake_job_postings.csv")

print("Dataset Loaded Successfully!")

# -----------------------------
# HANDLE NULL VALUES
# -----------------------------
df = df.fillna('')

# -----------------------------
# COMBINE TEXT COLUMNS
# -----------------------------
df["text"] = (
    df["title"] + " " +
    df["company_profile"] + " " +
    df["description"]
)

# -----------------------------
# FEATURES & TARGET
# -----------------------------
X = df["text"]
y = df["fraudulent"]

# -----------------------------
# TF-IDF VECTORIZATION
# -----------------------------
vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words='english',
    ngram_range=(1, 2)
)

X_vectorized = vectorizer.fit_transform(X)

print("Text Vectorization Completed!")

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# MODELS
# -----------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "Linear SVM": LinearSVC(),

    "XGBoost": XGBClassifier(
        eval_metric='logloss'
    ),

    "LightGBM": LGBMClassifier()
}

# -----------------------------
# TRAIN & EVALUATE
# -----------------------------
best_model = None
best_accuracy = 0
best_model_name = ""

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"{name} Accuracy: {accuracy:.4f}")

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

# -----------------------------
# SAVE BEST MODEL
# -----------------------------
joblib.dump(best_model, "models/fake_job_model.pkl")

joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\n==============================")
print(f"Best Model: {best_model_name}")
print(f"Best Accuracy: {best_accuracy:.4f}")
print("==============================")

print("\nBest model and vectorizer saved successfully!")