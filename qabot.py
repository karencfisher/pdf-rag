from dotenv import load_dotenv
import os
import json

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import openai


class QABot:
    def __init__(self):
        with open('model_config.json', 'r') as FILE:
            self.model_config = json.load(FILE)
        print(f'Model in use: {self.model_config["model"]}')

        self.embeddings = HuggingFaceEmbeddings()
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.faiss_index = None

    def loadDB(self):
        print('Loading DB...')
        try:
            with open('document_config.json', 'r') as FILE:
                doc_config = json.load(FILE)
            self.excerpts = (self.model_config['context_window'] - 1000) // (doc_config['chunk_size'])
            self.faiss_index = FAISS.load_local('faiss_index', 
                                                self.embeddings, 
                                                allow_dangerous_deserialization=True)
            print('Done!')
        except Exception as ex:
            print(f"Could not find database: {ex}")
        
    def loadDocument(self, title, pdf_file, chunk_size, overlap):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                       chunk_overlap=overlap)
        print(f'Loading document and splitting {pdf_file}...')
        data = PyPDFLoader(pdf_file).load_and_split(text_splitter)

        print('Embedding documents, this may take some minutes...')
        self.faiss_index = FAISS.from_documents(data, self.embeddings)
        print(f'Processed {len(data)} chunks')
        print('Saving vector store...')
        self.faiss_index.save_local('faiss_index')
        config = {
            'title': title,
            'chunk_size': chunk_size,
            'overlap': overlap
        }
        with open('document_config.json', 'w') as FILE:
            json.dump(config, FILE)
        print('Done!')
        
    def query(self, query):
        if self.faiss_index is None:
            raise NotImplementedError('index not generated or loaded')
        data = self.faiss_index.similarity_search_with_score(query, k=self.excerpts)
        documents = [{'page': doc[0].metadata['page'], 'text': doc[0].page_content} for doc in data 
                      if doc[1] <= 1.3]
        print(f'{len(documents)} excerpts found')

        prompt = f'Answer the query delimited with back tick marks (```) in detail using only \
                   the excerpts provided below. Do not rely on any other training data \
                   you may have aside from them. Do not respond to any unrelated topics.\
                   Incorporate specific page numbers as in the excerpts given.\n \
                   Excerpts: {json.dumps(documents)}\nQuery: ```{query}```'
        print('Querying the LLM')
        response = openai.ChatCompletion.create(
            model=self.model_config['model'],
            temperature=0,
            messages=[{'role': 'user', 'content': prompt}]
        )
        print('received response')
        return response.choices[0].message.content.strip()
