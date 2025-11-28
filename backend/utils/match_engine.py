import re

def match_resume_with_keywords(cleaned_resume_text: str, job_description: str):
    # Normalize keywords: lowercase, split by comma, strip spaces
    jd_keywords = {word.strip().lower() for word in job_description.split(",") if word.strip()}

    # Clean resume text again just in case
    resume_text = cleaned_resume_text.lower()
    resume_text = re.sub(r'[^\w\s]', ' ', resume_text)
    resume_text = re.sub(r'\s+', ' ', resume_text)

    matched_keywords = {kw for kw in jd_keywords if re.search(r'\b' + re.escape(kw) + r'\b', resume_text)}
    missing_keywords = jd_keywords - matched_keywords
    match_score = (len(matched_keywords) / len(jd_keywords)) * 100 if jd_keywords else 0

    return {
        "match_score": round(match_score, 2),
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
    }
