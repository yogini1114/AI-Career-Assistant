from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
def get_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()
if __name__ == '__main__':
    test = get_embedding('Python developer')
    print(f'Embedding size: {len(test)}')
    print('Embeddings working!')
