# AI Career Assistant

An intelligent career guidance system that analyzes resumes and provides personalized job recommendations using AI and vector search technology.

## Overview

AI Career Assistant is a web-based application that helps students and job seekers find the most suitable career opportunities based on their skills and experience. The system uses natural language processing and vector similarity search to match candidates with relevant job opportunities.

## Features

- Resume Parsing: Automatically extracts skills and experience from PDF resumes
- Smart Job Matching: Uses ChromaDB vector search to find semantically similar jobs
- Skill Gap Analysis: Identifies missing skills required for recommended positions
- AI Career Guidance: Generates personalized career roadmaps using Google Gemini API

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Embeddings Model | sentence-transformers (all-MiniLM-L6-v2) |
| Language Model | Google Gemini API |
| Resume Parser | PyMuPDF (fitz) |
| Data Processing | Pandas |

## Project Structure

ai-career-assistant/

├── app/

│   ├── main.py

│   └── backend/

│       ├── resume_parser.py

│       ├── embeddings.py

│       ├── vector_db.py

│       ├── recommender.py

│       └── llm_layer.py

├── data/

│   ├── india_job_market_2024_2026.csv

│   ├── career_dataset_large.csv

│   └── courses_en.csv

├── .env.example

├── .gitignore

└── README.md

## System Architecture

The system follows a 9-step pipeline:

1. User uploads resume or enters skills manually
2. Resume parser extracts raw text from PDF
3. Skills and experience are identified from text
4. Text is converted to vector embeddings using sentence-transformers
5. ChromaDB performs similarity search against job listings
6. Recommender engine calculates skill match percentage
7. Skill gap analysis identifies missing required skills
8. Gemini AI generates explanation and learning roadmap
9. Results are displayed on Streamlit dashboard

## Dataset Sources

| Dataset | Source | Records |
|---|---|---|
| India Job Market 2024-2026 | Kaggle | 5000 jobs |
| Career Recommendation Dataset | Kaggle | 5000 careers |
| Coursera Courses Dataset | Kaggle | 5411 courses |

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key (free tier available at aistudio.google.com)

### Installation

1. Clone the repository

```bash
git clone https://github.com/yogini1114/ai-career-assistant.git
cd ai-career-assistant
```

2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install required dependencies

```bash
pip install streamlit chromadb sentence-transformers pymupdf python-dotenv google-generativeai pdfplumber pandas
```

4. Configure environment variables

Create a `.env` file in the root directory:
GEMINI_API_KEY=api_key_here

5. Load dataset into ChromaDB

```bash
python app/backend/vector_db.py
```

6. Launch the application

```bash
streamlit run app/main.py
```

## Confidence Score Formula

The skill match percentage is calculated as follows:
Match Score = (Common Skills / Total Required Skills) x 100

Where:
- Common Skills = number of skills present in both student profile and job requirements
- Total Required Skills = total number of skills required for the job

## Security Considerations

- All API keys are stored in a `.env` file
- The `.env` file is excluded from version control via `.gitignore`
- Uploaded resumes are processed temporarily and not stored permanently
- No user data is retained after the session ends



