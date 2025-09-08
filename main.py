import os
from dotenv import load_dotenv
import openai
from summarizer import generate_document_summary

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")

def main():
    """Main function to run the summarizer tool."""
    print("Welcome to the Document Summarization Tool!")
    file_path = input("Enter the path to the document (e.g., document.txt or document.pdf): ")
    
    if not os.path.exists(file_path):
        print(f"Error: The file at {file_path} does not exist.")
        return
        
    print("\nGenerating summary...")
    summary = generate_document_summary(file_path)
    
    print("\n--- Summary ---")
    print(summary)
    print("---------------")

    print("---------------")

if __name__== "__main__":
    main()