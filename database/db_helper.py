import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "database.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema file not found at {SCHEMA_PATH}")
    conn = get_db_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# User Authentication Helpers
def create_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        log_action(user_id, "User Registered", f"Account created for {username}")
        return user_id, None
    except sqlite3.IntegrityError as e:
        conn.close()
        if "username" in str(e):
            return None, "Username already exists."
        elif "email" in str(e):
            return None, "Email already registered."
        return None, "Registration failed."

def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        log_action(user["id"], "User Login", f"Successful login for {username}")
        return dict(user)
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

# Job Description Helpers
def create_job_description(user_id, title, category, description_text, required_skills):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO job_descriptions (user_id, title, category, description_text, required_skills)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, title, category, description_text, required_skills)
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    log_action(user_id, "Job Created", f"Posted job description: '{title}' ({category})")
    return job_id

def get_user_jobs(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    jobs = cursor.fetchall()
    conn.close()
    return [dict(j) for j in jobs]

def get_job_by_id(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    return dict(job) if job else None

def delete_job(job_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM job_descriptions WHERE id = ? AND user_id = ?", (job_id, user_id))
    conn.commit()
    conn.close()
    log_action(user_id, "Job Deleted", f"Deleted job ID #{job_id}")

# Resume Helpers
def save_resume(user_id, filename, filepath, raw_text, parsed_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO resumes 
           (user_id, filename, filepath, raw_text, parsed_name, parsed_email, parsed_phone, 
            parsed_skills, parsed_education, parsed_experience, parsed_projects, parsed_certifications)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            filename,
            filepath,
            raw_text,
            parsed_data.get("name", "N/A"),
            parsed_data.get("email", "N/A"),
            parsed_data.get("phone", "N/A"),
            ", ".join(parsed_data.get("skills", [])),
            parsed_data.get("education", "N/A"),
            parsed_data.get("experience", "N/A"),
            parsed_data.get("projects", "N/A"),
            parsed_data.get("certifications", "N/A")
        )
    )
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id

def get_resume_by_id(resume_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,))
    resume = cursor.fetchone()
    conn.close()
    return dict(resume) if resume else None

def get_user_resumes(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resumes WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    resumes = cursor.fetchall()
    conn.close()
    return [dict(r) for r in resumes]

# Result Helpers
def save_result(job_id, resume_id, matching_score, cosine_sim, skill_score, ml_prob, missing_skills, suitability, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO results 
           (job_id, resume_id, matching_score, cosine_similarity, skill_match_score, ml_probability, missing_skills, suitability_prediction, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (job_id, resume_id, matching_score, cosine_sim, skill_score, ml_prob, missing_skills, suitability, status)
    )
    conn.commit()
    result_id = cursor.lastrowid
    conn.close()
    return result_id

def get_job_results(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT res.id as result_id, res.matching_score, res.cosine_similarity, 
                  res.skill_match_score, res.ml_probability, res.missing_skills, 
                  res.suitability_prediction, res.status, res.created_at as evaluated_at,
                  r.id as resume_id, r.filename, r.parsed_name, r.parsed_email, r.parsed_phone, r.parsed_skills
           FROM results res
           JOIN resumes r ON res.resume_id = r.id
           WHERE res.job_id = ?
           ORDER BY res.matching_score DESC""",
        (job_id,)
    )
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]

def get_result_detail(result_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT res.*, r.filename, r.parsed_name, r.parsed_email, r.parsed_phone, 
                  r.parsed_skills, r.parsed_education, r.parsed_experience, 
                  r.parsed_projects, r.parsed_certifications, r.raw_text,
                  j.title as job_title, j.category as job_category, j.required_skills as job_required_skills, j.description_text as job_description
           FROM results res
           JOIN resumes r ON res.resume_id = r.id
           JOIN job_descriptions j ON res.job_id = j.id
           WHERE res.id = ?""",
        (result_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return dict(result) if result else None

# History & Stats
def log_action(user_id, action, details):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user_id, action, details) VALUES (?, ?, ?)", (user_id, action, details))
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=15):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, limit))
    history = cursor.fetchall()
    conn.close()
    return [dict(h) for h in history]

def get_dashboard_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total_jobs FROM job_descriptions WHERE user_id = ?", (user_id,))
    total_jobs = cursor.fetchone()["total_jobs"]
    
    cursor.execute("SELECT COUNT(*) as total_resumes FROM resumes WHERE user_id = ?", (user_id,))
    total_resumes = cursor.fetchone()["total_resumes"]
    
    cursor.execute(
        """SELECT COUNT(res.id) as total_evaluations, 
                  AVG(res.matching_score) as avg_score
           FROM results res
           JOIN job_descriptions j ON res.job_id = j.id
           WHERE j.user_id = ?""",
        (user_id,)
    )
    eval_row = cursor.fetchone()
    total_evaluations = eval_row["total_evaluations"] or 0
    avg_score = round(eval_row["avg_score"] or 0, 1)
    
    cursor.execute(
        """SELECT status, COUNT(*) as count 
           FROM results res
           JOIN job_descriptions j ON res.job_id = j.id
           WHERE j.user_id = ?
           GROUP BY status""",
        (user_id,)
    )
    status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    return {
        "total_jobs": total_jobs,
        "total_resumes": total_resumes,
        "total_evaluations": total_evaluations,
        "avg_score": avg_score,
        "status_counts": status_counts
    }
