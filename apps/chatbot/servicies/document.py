import os
import uuid
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser



class DocumentService:
    def __init__(self,
                 mode: str = "file",
                 folder_path: str = "",
                 chunk_size: int = 250,
                 chunk_overlap: int = 0,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 use_api: bool = False,
                 api_key: str = "",
                 k: int = 4):

        self.mode = mode
        self.folder_path = folder_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model
        self.use_api = use_api
        self.api_key = api_key
        self.k = k
        self.vectorstore = None
        self.retriever = None

    # 1. Load documents
    def load_documents(self):
        docs = []
        if self.mode == "file":
            print(f"Loading documents from: {self.folder_path}")
            for filename in os.listdir(self.folder_path):
                if filename.endswith(".docx"):
                    path = os.path.join(self.folder_path, filename)
                    print(f"  Loading file: {filename}")
                    loader = Docx2txtLoader(path)
                    docs.extend(loader.load())
        print(f"Loaded {len(docs)} documents.")
        return docs

    # 2. Split documents
    def split_documents(self, docs):
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        chunks = splitter.split_documents(docs)
        print(f"Created {len(chunks)} text chunks.")
        return chunks

    # 3. Create vector store
    def create_vectorstore(self, docs):
        print("Creating embeddings and vector store...")
        if self.use_api:
            embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        else:
            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)

        self.vectorstore = SKLearnVectorStore.from_documents(docs, embedding=embeddings)
        actual_k = min(self.k, len(docs))
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": actual_k})
        print(f"Vector store created (k={actual_k}, total_docs={len(docs)})")
        return self.retriever