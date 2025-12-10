# backend/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import ast

app = FastAPI(title="AI Tutor Backend")

# --------- LOAD DATA ONCE AT STARTUP ---------
# Expecting file: data/clean_student_dataset.csv
df = pd.read_csv("../data/clean_student_dataset.csv")

# convert concept_tags from string to list
def _parse_tags(x):
    if isinstance(x, list):
        return x
    try:
        return ast.literal_eval(x)
    except Exception:
        return [str(x)]

df["concept_tags"] = df["concept_tags"].apply(_parse_tags)

ALL_CONCEPTS = sorted({c for tags in df["concept_tags"] for c in tags})

# --------- UTILS ---------
def get_student_df(student_id: int) -> pd.DataFrame:
    s_df = df[df["student_id"] == student_id]
    return s_df

def compute_per_concept_stats(s_df: pd.DataFrame):
    stats = []
    for c in ALL_CONCEPTS:
        mask = s_df["concept_tags"].apply(lambda tags: c in tags)
        c_df = s_df[mask]
        if len(c_df) == 0:
            continue
        acc = float(c_df["correct"].mean())
        attempts = int(len(c_df))
        stats.append({
            "concept": c,
            "accuracy": acc,
            "attempts": attempts,
            "is_weak": bool(acc < 0.6 and attempts >= 3)
        })
    return stats

# --------- MODELS ---------
class LoginRequest(BaseModel):
    student_id: int
    password: str

class LoginResponse(BaseModel):
    success: bool
    student_id: int | None = None
    message: str

# --------- ENDPOINTS ---------

@app.get("/students")
def list_students() -> Dict[str, List[int]]:
    """Return all available student_ids."""
    students = sorted(df["student_id"].unique().tolist())
    return {"students": students}

@app.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    """
    Very simple demo login:
    - student_id must exist in data
    - password must be '1234'
    """
    if req.student_id not in df["student_id"].unique():
        return LoginResponse(success=False, message="Student ID not found", student_id=None)
    if req.password != "1234":
        return LoginResponse(success=False, message="Incorrect demo password (use 1234)", student_id=None)
    return LoginResponse(success=True, message="Login successful", student_id=req.student_id)

@app.get("/student_summary/{student_id}")
def student_summary(student_id: int) -> Dict[str, Any]:
    """Basic stats for a student."""
    s_df = get_student_df(student_id)
    if len(s_df) == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    attempts = int(len(s_df))
    accuracy = float(s_df["correct"].mean()) if attempts > 0 else None
    avg_time = float(s_df["response_time"].mean()) if attempts > 0 else None

    per_concept = compute_per_concept_stats(s_df)

    return {
        "student_id": student_id,
        "attempts": attempts,
        "overall_accuracy": accuracy,
        "avg_response_time": avg_time,
        "per_concept": per_concept,
    }

@app.get("/weak_topics/{student_id}")
def weak_topics(student_id: int) -> Dict[str, Any]:
    """Return only weak concepts for a student."""
    s_df = get_student_df(student_id)
    if len(s_df) == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    per_concept = compute_per_concept_stats(s_df)
    weak = [c for c in per_concept if c["is_weak"]]

    return {
        "student_id": student_id,
        "weak_topics": weak,
        "all_concepts": per_concept,
    }

# backward-compatible alias
@app.get("/predict_weak_topics")
def predict_weak_topics(student_id: int):
    """Alias for /weak_topics for old code."""
    return weak_topics(student_id)
