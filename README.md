# Document Summarization Tool
This project offers a Python-based utility for summarizing text documents, including.txt and.pdf formats.  It is designed to handle huge files by employing a map-reduce summarization technique that divides the material into smaller, more manageable parts before summarizing.
## Description
The goal is to produce a summary that retains the most important information while significantly reducing the original document's size. This is particularly useful for handling large amounts of data, such as articles, reports, or legal documents, as it allows users to quickly grasp the main points without reading the entire text.

## Features 
* **Supports Multiple File Types:** Works with both .txt and .pdf documents.

* **Handles Large Files:** Automatically detects large documents and uses a map-reduce strategy to summarize them effectively.

- **Concise and Detailed Summaries:** Utilizes the OpenAI GPT-3.5-Turbo model to generate high-quality summaries.

## Working
### Setup and Installation
**Prerequisites**
````
openai
python-dotenv
tiktoken
PyPDF2
````

**Create Virtual Environment & Install Dependencies**
```
python -m venv venv
venv\Scripts\activate       
pip install -r requirements.txt
```
**Add `.env` file**
```
OPENAI_API_KEY= "your_api_key_here"
```
**The `main.py` file serves as the command-line interface**

It loads OpenAI API key from a `.env`file.
```
# Load environment variables from .env
load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file.")
```
It prompts the user to enter the path to the document they want to summarize.
```
file_path = input("Enter the path to the document (e.g., document.txt or document.pdf): ")
```
It calls the `generate_document_summary` function and prints the final output.

**The core logic is within `summarizer.py`**

`generate_document_summary`: This is the main function that orchestrates the process.
* It first reads the content of the specified document.
- If the document is short (under 1000 words), it summarizes it directly.
- If the document is long, it splits the text into chunks, summarizes each chunk individually, and then combines those summaries into a final, comprehensive summary.
```
if file_path.endswith(".pdf"):
    import PyPDF2
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
else:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
```

`split_text_into_chunks`: This function tokenizes the input text and divides it into smaller chunks to fit within the language model's context window. This is crucial for handling documents that are too long for a single API call.
```
if len(text.split()) < 1000:
    final_summary = summarize_text(text)   # Direct summarization
else:
    print("Document is large. Using map-reduce summarization...")
    chunks = split_text_into_chunks(text, max_tokens=1500)
    summaries = [summarize_text(chunk) for chunk in chunks]
    combined = " ".join(summaries)
    final_summary = summarize_text(combined)
```

`summarize_text`: This function sends a text chunk to the OpenAI API with a prompt to generate a summary.
```
def summarize_text(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Please summarize the following:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()
```
**Final Output**
```
print("\n--- Summary ---")
    print(summary)
    print("---------------")

    print("---------------")

```
 



