import os
import pypdf
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from .services.scoring import compute_score
from .services.latex_service import generate_latex, compile_latex


def parse_resume_tool(file_path: str) -> str:
    """
    Parses a resume file (PDF, DOCX, or TXT) and returns the extracted text.
    
    Args:
        file_path: The absolute path to the resume file.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        elif ext == ".docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return f"Error: Unsupported file format {ext}"
    except Exception as e:
        return f"Error parsing file: {str(e)}"
    
    return text.strip()

def semantic_similarity_tool(resume_text: str, jd_text: str) -> float:
    """
    Computes the semantic similarity between resume text and job description using TF-IDF and cosine similarity.
    
    Args:
        resume_text: The text content of the resume.
        jd_text: The text content of the job description.
    """
    if not resume_text or not jd_text:
        return 0.0
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return float(similarity[0][0])

def keyword_match_tool(resume_text: str, jd_text: str) -> dict:
    """
    Identifies matching keywords and missing skills between the resume and JD.
    
    Args:
        resume_text: The text content of the resume.
        jd_text: The text content of the job description.
    """
    # Simple keyword extraction (can be improved with LLM or better NLP)
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    
    # Filter common stop words (simplified)
    stop_words = {"and", "the", "with", "for", "from", "that", "this", "our", "your"}
    jd_keywords = {w for w in jd_words if len(w) > 3 and w not in stop_words}
    
    matches = jd_keywords.intersection(resume_words)
    missing = jd_keywords.difference(resume_words)
    
    match_percentage = len(matches) / len(jd_keywords) if jd_keywords else 1.0
    
    return {
        "match_percentage": match_percentage,
        "matched_keywords": list(matches)[:10],
        "missing_keywords": list(missing)[:10]
    }

def ats_checker_tool(resume_text: str) -> dict:
    """
    Checks the resume for ATS compliance (formatting, layout, etc.).
    
    Args:
        resume_text: The text content of the resume.
    """
    issues = []
    score = 1.0
    
    # Simple heuristic checks
    if len(resume_text) < 500:
        issues.append("Resume text is very short.")
        score -= 0.2
        
    # Check for sections
    sections = ["experience", "education", "skills", "projects"]
    for section in sections:
        if section not in resume_text.lower():
            issues.append(f"Missing '{section}' section.")
            score -= 0.1
            
    return {
        "compliance_score": max(0, score),
        "issues": issues
    }

def scoring_tool(semantic_score: float, keyword_score: float, skills_alignment: float, ats_compliance: float) -> str:
    """
    Computes the final weighted ATS score and returns a structured breakdown.
    
    Args:
        semantic_score: Score from semantic comparison (0-1).
        keyword_score: Score from keyword matching (0-1).
        skills_alignment: Score for skill alignment (0-1).
        ats_compliance: Score for ATS compliance (0-1).
    """
    total_score = compute_score(
        semantic_score,
        keyword_score,
        skills_alignment,
        ats_compliance
    )
    
    result = {
        "overall_score": round(total_score * 100, 2),
        "breakdown": {
            "semantic_similarity": round(semantic_score * 100, 2),
            "keyword_match": round(keyword_score * 100, 2),
            "skills_alignment": round(skills_alignment * 100, 2),
            "ats_compliance": round(ats_compliance * 100, 2)
        }
    }
    return json.dumps(result)

def latex_builder_tool(optimized_resume_data: str) -> str:
    """
    Generates an optimized LaTeX resume based on provided data, attempts to compile it to PDF, 
    and returns the result (PDF link or raw LaTeX).
    
    Args:
        optimized_resume_data: JSON string containing the resume data.
    """
    try:
        # Load data
        if isinstance(optimized_resume_data, str):
            data = json.loads(optimized_resume_data)
        else:
            data = optimized_resume_data

        latex_content = generate_latex(data)
        
        # Try to compile
        pdf_path = compile_latex(latex_content)
        
        if pdf_path and os.path.exists(pdf_path):
            filename = os.path.basename(pdf_path)
            # Assuming media is served at /media/
            return f"Success! Optimized resume generated and compiled.\n\nPDF Download: /media/{filename}\n\nLaTeX Source:\n```latex\n{latex_content}\n```"
        else:
            return f"Resume generated, but PDF compilation failed (pdflatex might be missing or had an error). You can use the LaTeX code below in an online editor like Overleaf:\n\n```latex\n{latex_content}\n```"

    except Exception as e:
        return f"Error in LaTeX builder tool: {str(e)}"

