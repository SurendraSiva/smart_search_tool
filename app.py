import streamlit as st
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import Chroma

# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# Initialize the wrapper

# Initialize Chroma DB with the persistent directory
persistent_directory = 'vectordb'  # Directory where the vector data is stored
vector_db = Chroma(persist_directory=persistent_directory)

st.title("Smart Search Tool")

# Function to handle the search
def search_courses(query):
    # Display a loading spinner while processing
    with st.spinner('Processing your search...'):
        # Generate embedding for the query
        query_embedding = embedding_model.encode(query).tolist()

        # Perform similarity search
        results = vector_db.similarity_search_by_vector(query_embedding, k=5)
    
    # Display results after the search is complete
    st.subheader("Results")

    if results:
        # Sort the results by rating (in decreasing order)
        # Display the top 5 results
        for res in results:
            st.write(f"**Course Heading:** {res.metadata['course_heading']}")
            st.write(f"**Rating:** {res.metadata['rating']}")
            st.write(f"**Number of Lessons:** {res.metadata['number_of_lessons']}")
            st.write(f"[Course Link]({res.metadata['url']})")
            st.write("---")
    else:
        st.write("No relevant results found.")

# Initialize session_state.query if it does not exist
if "query" not in st.session_state:
    st.session_state.query = ""

# Text input to take user query and trigger the search on Enter key press
query = st.text_input("Search for a course:", key="query")

# Trigger search when the user presses Enter
if query:
    search_courses(query)
