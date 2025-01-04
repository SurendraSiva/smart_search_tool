from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma
import pandas as pd

# Load the dataset
data = pd.read_excel('all_courses_analyticsvidhya.xlsx')

# Initialize the SentenceTransformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Create a wrapper for SentenceTransformer to implement the 'embed_documents' method
class SentenceTransformerEmbedding:
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return [self.model.encode(text).tolist() for text in texts]  # Ensure embeddings are in list format

# Initialize the wrapper
embedding_function = SentenceTransformerEmbedding(embedding_model)

# Prepare data for indexing
documents = [
    {
        "course_heading": row['Course Heading'],
        "number_of_lessons": str(row['Number of Lessons']),
        "rating": str(row['Rating']),
        "url": row['Course URL']
    }
    for _, row in data.iterrows()
]

# Set the directory for persistence
persistent_directory = 'vectordb'

# Initialize Chroma DB with the custom embedding function
vector_db = Chroma(persist_directory=persistent_directory, embedding_function=embedding_function)

# Index data using Sentence Transformers
for doc in documents:
    content = f"{doc['course_heading']} with {doc['number_of_lessons']} lessons, rating: {doc['rating']}"
    vector_db.add_texts([content], metadatas=[doc])
