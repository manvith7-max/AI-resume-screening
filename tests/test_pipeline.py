import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from database.db_helper import (
    init_db, create_user, verify_user, create_job_description,
    save_resume, save_result, get_job_results, get_dashboard_stats
)
from utils.nlp_pipeline import clean_text, preprocess_text
from utils.resume_parser import parse_email, parse_phone, parse_skills, parse_resume
from utils.report_generator import generate_pdf_report, generate_excel_report, generate_csv_report
from dataset.generate_data import main as generate_dataset
from models.train_model import train_and_evaluate

class TestAIResumeScreeningPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_01_nlp_pipeline(self):
        sample_text = "Experienced Senior Python Developer with 5+ years building Web APIs & Machine Learning models!"
        cleaned = clean_text(sample_text)
        processed = preprocess_text(sample_text)
        self.assertIn("python", cleaned)
        self.assertIn("developer", processed)
        print("[OK] NLP preprocessing test passed.")

    def test_02_resume_parsing(self):
        sample_resume = """
Johnathan Doe
Senior Software Engineer | johnathan.doe99@gmail.com | +1 (555) 234-5678

PROFESSIONAL SUMMARY
5+ years experience in Python, Flask, SQL, React, AWS, Docker, Kubernetes, and Machine Learning.

EDUCATION
BS in Computer Science - Tech University (2018)
"""
        email = parse_email(sample_resume)
        phone = parse_phone(sample_resume)
        skills = parse_skills(sample_resume)
        
        self.assertEqual(email, "johnathan.doe99@gmail.com")
        self.assertIn("+1 (555) 234-5678", phone)
        self.assertIn("Python", skills)
        self.assertIn("Docker", skills)
        print("[OK] Resume parser test passed.")

    def test_03_database_operations(self):
        user_id, err = create_user("testuser_qa", "testuser_qa@example.com", "SecretPass123")
        if not user_id:
            user = verify_user("testuser_qa", "SecretPass123")
            user_id = user["id"]
            
        self.assertIsNotNone(user_id)
        
        job_id = create_job_description(
            user_id=user_id,
            title="Senior Python Architect",
            category="Backend Developer",
            description_text="Looking for a Python expert with SQL and Docker experience.",
            required_skills="Python, SQL, Docker, Flask"
        )
        self.assertIsNotNone(job_id)
        
        parsed_mock = {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+1 555-987-6543",
            "skills": ["Python", "SQL", "Docker"],
            "education": "MS in CS",
            "experience": "4 years",
            "projects": "Built REST APIs",
            "certifications": "AWS Certified"
        }
        
        resume_id = save_resume(
            user_id=user_id,
            filename="jane_smith_resume.pdf",
            filepath="/tmp/jane_smith_resume.pdf",
            raw_text="Jane Smith Python SQL Docker",
            parsed_data=parsed_mock
        )
        self.assertIsNotNone(resume_id)
        
        res_id = save_result(
            job_id=job_id,
            resume_id=resume_id,
            matching_score=88.5,
            cosine_sim=0.85,
            skill_score=100.0,
            ml_prob=0.92,
            missing_skills="None",
            suitability="Backend Developer",
            status="Highly Recommended"
        )
        self.assertIsNotNone(res_id)
        
        results = get_job_results(job_id)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["parsed_name"], "Jane Smith")
        
        stats = get_dashboard_stats(user_id)
        self.assertGreaterEqual(stats["total_jobs"], 1)
        print("[OK] Database CRUD operations test passed.")

    def test_04_dataset_and_ml_training(self):
        generate_dataset()
        dataset_file = os.path.join(BASE_DIR, "dataset", "resumes_dataset.csv")
        self.assertTrue(os.path.exists(dataset_file))
        
        metrics = train_and_evaluate()
        self.assertIn("best_model", metrics)
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, "trained_model", "best_model.pkl")))
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, "trained_model", "tfidf_vectorizer.pkl")))
        self.assertTrue(os.path.exists(os.path.join(BASE_DIR, "models", "model_comparison.png")))
        print("[OK] Dataset & ML model training pipeline test passed.")

    def test_05_report_generators(self):
        mock_results = [{
            "parsed_name": "Alex Mercer",
            "parsed_email": "alex@example.com",
            "parsed_phone": "+1 555-111-2222",
            "matching_score": 85.0,
            "cosine_similarity": 0.82,
            "skill_match_score": 90.0,
            "ml_probability": 0.88,
            "missing_skills": "Kubernetes",
            "status": "Highly Recommended"
        }]
        
        pdf_name, pdf_path = generate_pdf_report("Python Dev", "Backend Developer", mock_results)
        self.assertTrue(os.path.exists(pdf_path))
        
        excel_name, excel_path = generate_excel_report("Python Dev", "Backend Developer", mock_results)
        self.assertTrue(os.path.exists(excel_path))
        
        csv_name, csv_path = generate_csv_report("Python Dev", mock_results)
        self.assertTrue(os.path.exists(csv_path))
        print("[OK] PDF, Excel, and CSV report generator tests passed.")

if __name__ == "__main__":
    unittest.main()
