def compute_score(semantic_similarity: float, keyword_match: float, skills_alignment: float, ats_compliance: float) -> float:
    """
    Computes a hybrid weighted ATS score.
    
    Weights:
    - 0.4 * Semantic Similarity
    - 0.3 * Keyword Match
    - 0.2 * Skills Alignment
    - 0.1 * ATS Compliance
    """
    overall_score = (
        0.4 * semantic_similarity +
        0.3 * keyword_match +
        0.2 * skills_alignment +
        0.1 * ats_compliance
    )
    return overall_score
