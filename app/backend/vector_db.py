import chromadb
import pandas as pd
from embeddings import get_embedding

client = chromadb.PersistentClient(path="./chroma_db")
jobs_collection = client.get_or_create_collection("jobs")
careers_collection = client.get_or_create_collection("careers")
resources_collection = client.get_or_create_collection("resources")


def load_jobs_data():
    df = pd.read_csv("data/india_job_market_2024_2026.csv")
    df = df.dropna(subset=['Skills_Required'])
    df = df.head(200)
    return df


def store_jobs():
    df = load_jobs_data()
    for index, row in df.iterrows():
        text = f"{row['Job_Title']} {row['Skills_Required']}"
        embedding = get_embedding(text)
        jobs_collection.add(
            ids=[str(index)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "title": str(row['Job_Title']),
                "company": str(row['Company']),
                "skills": str(row["Skills_Required"]),
                "salary": str(row["Salary_LPA"])
            }]
        )
    print(f"Jobs stored: {len(df)}")


def ensure_jobs_loaded():
    """Agar jobs collection empty hai to data load karo (Streamlit Cloud restart ke baad)"""
    if jobs_collection.count() == 0:
        print("Jobs collection empty — loading data...")
        store_jobs()


def search_jobs(query_text, n_results=5):
    query_embedding = get_embedding(query_text)
    results = jobs_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results


def search_careers(query_text, n_results=5):
    query_embedding = get_embedding(query_text)
    results = careers_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results


def search_resources(query_text, n_results=5):
    query_embedding = get_embedding(query_text)
    results = resources_collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results


if __name__ == "__main__":
    print("Storing jobs data...")
    store_jobs()
    print("Testing search...")
    results = search_jobs("Python Machine Learning")
    print("Top matches:", results['metadatas'])
