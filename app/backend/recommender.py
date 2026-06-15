from vector_db import search_jobs, search_careers, search_resources

def calculate_skill_match(student_skills, required_skills):
    student_set= set(student_skills.lower().split(','))
    required_set=set(required_skills.lower().split(','))
    common=student_set.intersection(required_set)
    if len(required_set)==0:
        return 0
    score = len(common)/len(required_set)*100
    return round(score,2)

def get_recommendations(student_skills, top_n=5):
    """Student skills se best jobs recommend karo"""
    
    # Step 1: ChromaDB se jobs dhundo
    job_results = search_jobs(student_skills, n_results=top_n)
    
    recommendations = []
    
    # Step 2: Har job ka score calculate karo
    for i, metadata in enumerate(job_results['metadatas'][0]):
        
        # Debug — dekho kya aa raha hai
        print("DEBUG metadata:", metadata)
        
        # Skills nikalo metadata se
        job_skills = metadata.get('skills', '')
        
        # Score calculate karo
        score = calculate_skill_match(
            student_skills,
            job_skills
        )
        
        recommendations.append({
            'title': metadata.get('title', 'Unknown'),
            'company': metadata.get('company', 'Unknown'),
            'skills_required': job_skills,
            'salary': metadata.get('salary', 'N/A'),
            'match_score': score
        })
    
    # Step 3: Score se sort karo — best pehle
    recommendations.sort(
        key=lambda x: x['match_score'],
        reverse=True
    )
    
    return recommendations

def get_skill_gaps(student_skills, required_skills):
    # List hai toh string banao
    if isinstance(student_skills, list):
        student_skills = ', '.join(student_skills)
    if isinstance(required_skills, list):
        required_skills = ', '.join(required_skills)
    
    # String check karo
    if not isinstance(student_skills, str):
        student_skills = str(student_skills)
    if not isinstance(required_skills, str):
        required_skills = str(required_skills)
    
    student_set = set(s.strip() for s in student_skills.lower().split(','))
    required_set = set(s.strip() for s in required_skills.lower().split(','))
    
    gaps = required_set - student_set
    return list(gaps)

if __name__ == "__main__":
    test_skills = "Python, TensorFlow, Machine Learning, Scikit-learn, Docker"
    print("Testing recommendations...")
    results = get_recommendations(test_skills)
    for job in results:
        print(f"\nJob: {job['title']} at {job['company']}")
        print(f"Match: {job['match_score']}%")
        print(f"Salary: {job['salary']} LPA")
        gaps = get_skill_gaps(test_skills, job['skills_required'])
        print(f"Skills to learn: {gaps}")