## Basic RAG application

This repository provides an example of a basic application to ingest a PDF file, and provide a web UI to make queries about its content. It is a basic example of a RAG -- "Retrieval Augmented Generation" -- model.

In the below example, I have ingested a large PDF document (the 900+ pages of the "Project 2025" that is much in the current news but too long for many to read in its entriety). One can then ask the model to summarize various topics from within the document.

![screenshot](/Images/Screenshot.jpg)

One can ingest any single PDF document. (None are included in this repository to avoid possible copyright issues.)
    
Keep in mind that the input to the LLM may include up to 125,000 tokens for the retrieved context for a query. I have seen good results with OpenAI's gpt-4o-mini to reduce API costs as low as possible.

### Setup

1) Download, clone, or fork/clone this repository
2) It is suggested that one create a virtual environment for this project and acitvate it. E.g., within the project root in your terminal:

```
python -m venv ragenv
ragenv\scripts\activate
```

3) Install the dependencies:

```
pip install -r requirements.txt
```

4) You will need an OpenAI API key
5) Create a .env file in the root of the project. In it include your OpenAI API key as:

```
OPENAI_API_KEY = 'sk-<rest of your aPI key>'
```

### Use

1) In order to ingest a PDF document you are interested, in the terminal use the loadBook utility:

```
python loadBook.py <title> <PDF-path> <chunk-size> <overlap>
```

Where \<title> is the title as it ahould appear in the UI, \<PDF-path> is the actual PDF file, \<chunk-size> is the desired of excerpt sizes in tokens, and \<overlap> is any overlap between excerpts in tokens.

2) Run the app:

```
python app.py
```

The web app will be available both on your localhost as well as on the IP address of the hosting machine, at port 5000.
