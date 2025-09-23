import requests
import numpy as np
from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer


# -----------------------------
# LLM Services
# -----------------------------
class ModelLLMService_API:
    def __init__(self, model_name, api_key, api_url, api_version=None, api_type=None,
                 max_tokens=512, temperature=0.7, top_p=1.0, n=1, stream=False, stop=None):
        self.model_name = model_name
        self.api_key = api_key
        self.api_url = api_url
        self.api_version = api_version
        self.api_type = api_type
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop

    def generate_response(self, prompt: str):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "stop": self.stop
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()


class ModelLLMService_Local:
    def __init__(self, model_name, model_version=None,
                 max_tokens=128, temperature=0.7, top_p=1.0, n=1, stream=False, stop=None):
        self.model_name = model_name
        self.model_version = model_version
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, prompt: str):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            num_return_sequences=self.n
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


# -----------------------------
# RAG Components
# -----------------------------
class DocumentStorage:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_documents(self, docs: List[str], embedder):
        for doc in docs:
            emb = embedder.encode(doc)
            self.documents.append(doc)
            self.embeddings.append(emb)

    def get_all(self):
        return self.documents, self.embeddings


class DocumentRetrieval:
    def __init__(self, storage: DocumentStorage):
        self.storage = storage

    def retrieve(self, query: str, embedder, top_k=3):
        docs, embs = self.storage.get_all()
        q_emb = embedder.encode(query)
        scores = [np.dot(q_emb, e) / (np.linalg.norm(q_emb) * np.linalg.norm(e)) for e in embs]
        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked[:top_k]]


class Generation:
    def __init__(self, llm_service):
        self.llm_service = llm_service

    def generate(self, prompt: str):
        return self.llm_service.generate_response(prompt)


class Orchestration:
    def __init__(self, retriever: DocumentRetrieval, generator: Generation):
        self.retriever = retriever
        self.generator = generator

    def ask(self, query: str, embedder):
        context_docs = self.retriever.retrieve(query, embedder)
        context = "\n".join(context_docs)
        final_prompt = f"Answer the question based on the context:\n{context}\n\nQuestion: {query}\nAnswer:"
        return self.generator.generate(final_prompt)

