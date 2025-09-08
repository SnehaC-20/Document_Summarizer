import os
import openai
import tiktoken

# Define the maximum tokens for the model
MAX_TOKENS = 4096

def split_text_into_chunks(text, max_tokens=1500):
    """Splits text into chunks that fit within the LLM's context window."""
    #Tokenize the Input
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    
    #Variables initialization
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    # Loop Over Tokens
    for token in tokens:
        current_chunk.append(token)
        current_token_count += 1
        
        # Check if adding the next word would exceed the max tokens
        # A rough check to ensure we're not cutting words in half
        if current_token_count >= max_tokens:
            chunks.append(encoding.decode(current_chunk))
            current_chunk = []
            current_token_count = 0
       # Handling leftover tokens     
    if current_chunk:
        chunks.append(encoding.decode(current_chunk))
        
    return chunks

def summarize_text(text):
    """Summarizes a single piece of text using the OpenAI API."""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Please provide a concise and detailed summary of the following document:\n\n{text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def generate_document_summary(file_path):
    """Generates a summary for an entire document, handling large files."""
    try:
        # Load file content based on type
        if file_path.endswith(".pdf"):
            import PyPDF2
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
        else: # Assumes text file
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        
        # Check if the document is short enough to summarize directly
        if len(text.split()) < 1000: # Simple word count check
            final_summary = summarize_text(text)
        else:
            print("Document is large. Using map-reduce summarization...")
            # Split the document into chunks
            chunks = split_text_into_chunks(text, max_tokens=1500)
            
            # Summarize each chunk
            summaries = [summarize_text(chunk) for chunk in chunks]
            
            # Combine the summaries and summarize them again
            combined_summaries = " ".join(summaries)
            final_summary = summarize_text(combined_summaries)
            
        return final_summary
        
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"