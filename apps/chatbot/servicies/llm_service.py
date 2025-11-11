import os
import io
import requests
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import Docx2txtLoader

from apps.chatbot.models.model_mongo import ChatHistory
from apps.chatbot.models.knowled_base import KnowledgeBase


class LLMService:
    MAX_RAM_HISTORY = 10

    def __init__(
        self,
        use_api: bool = False,
        api_key: str = "",
        model_local: str = "llama3.1",
        model_api: str = "gpt-4o-mini",
        temperature: float = 0,
        retriever=None,
    ):
        self.use_api = use_api
        self.api_key = api_key
        self.model_local = model_local
        self.model_api = model_api
        self.temperature = temperature
        self.retriever = retriever
        self.llm = self._init_model()
        self.prompt = self._build_prompt()
        self.chain = self.prompt | self.llm | StrOutputParser()
        self.sessions = {}

    def _init_model(self):
        if self.use_api:
            return ChatOpenAI(
                model=self.model_api,
                temperature=self.temperature,
                api_key=self.api_key,
                streaming=True,
            )
        return ChatOllama(
            model=self.model_local,
            temperature=self.temperature,
            streaming=True,
        )

    def _build_prompt(self):
        return PromptTemplate(
            template=(
                "You are an assistant for question-answering tasks.\n"
                "Use the following documents and previous messages to answer the question.\n"
                "If you don't know the answer, say you don't know.\n"
                "Keep your answer concise and clear.\n\n"
                "Chat History:\n{chat_history}\n"
                "Question: {question}\n"
                "Documents: {documents}\n"
                "Answer:"
            ),
            input_variables=["question", "documents", "chat_history"],
        )

    def create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def get_history(self, session_id: str, user_id: str = None):
        if session_id in self.sessions and len(self.sessions[session_id]) > 0:
            return self.sessions[session_id]

        doc = ChatHistory.objects(user_id=user_id).first()
        if not doc:
            return []

        session = next((s for s in doc.sessions if s["session_id"] == session_id), None)
        if not session:
            return []

        return [f"{m['role']}: {m['message']}" for m in session["chat_history"]]


    def run_stream(self, session_id: str, question: str, user_id: str = None):
        if session_id not in self.sessions:
            raise ValueError(f"Session '{session_id}' not found.")

        docs = self.retriever.invoke(question) if self.retriever else []
        context = "\n".join([d.page_content for d in docs])
        chat_history = "\n".join(self.sessions[session_id][-self.MAX_RAM_HISTORY * 2:])

        answer = ""
        for chunk in self.chain.stream({
            "question": question,
            "documents": context,
            "chat_history": chat_history,
        }):
            answer += chunk

        self.sessions[session_id].append(f"Q: {question}")
        self.sessions[session_id].append(f"A: {answer}")

        if len(self.sessions[session_id]) > self.MAX_RAM_HISTORY * 2:
            self.sessions[session_id] = self.sessions[session_id][-self.MAX_RAM_HISTORY * 2:]

        try:
            self.save_history(session_id, question, answer, user_id)
        except Exception as e:
            print(e)

        return answer

    def save_history(self, session_id: str, question: str, answer: str, user_id: str = None):
        now = datetime.utcnow()

        user_doc = ChatHistory.objects(user_id=user_id).first()
        if not user_doc:
            user_doc = ChatHistory(user_id=user_id, sessions=[])
            user_doc.save()

        session = next((s for s in user_doc.sessions if s["session_id"] == session_id), None)
        if not session:
            session = {"session_id": session_id, "chat_history": []}
            user_doc.sessions.append(session)

        session["chat_history"].append({
            "role": "user",
            "message": question,
            "create_at": now,
            "update_at": now
        })
        session["chat_history"].append({
            "role": "assistant",
            "message": answer,
            "create_at": now,
            "update_at": now
        })

        user_doc.save()

    def clear_history(self, session_id: str):
        self.sessions[session_id] = []

    def delete_session(self, session_id: str, user_id: str):
        user_doc = ChatHistory.objects(user_id=user_id).first()
        if not user_doc:
            return False

        user_doc.sessions = [
            s for s in user_doc.sessions if s["session_id"] != session_id
        ]

        user_doc.save()
        return True



    def save_knowledge_base(self, title: str, content: str, user_id: str = None, metadata: dict = None, embeddings: list = None):
        kb = KnowledgeBase(
            user_id=user_id,
            title=title,
            content=content,
            metadata=metadata or {},
            embeddings=embeddings or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        kb.save()

    def load_knowledge_base(self, user_id: str = None, limit: int = None):
        query = KnowledgeBase.objects
        if user_id:
            query = query(user_id=user_id)
        return query.limit(limit) if limit else query

    def delete_knowledge_base(self, user_id: str = None, title: str = None):
        query = KnowledgeBase.objects
        if user_id:
            query = query(user_id=user_id)
        if title:
            query = query(title=title)
        query.delete()

    def update_knowledge_base(self, user_id: str = None, title: str = None, content: str = None):
        query = KnowledgeBase.objects
        if user_id:
            query = query(user_id=user_id)
        if title:
            query = query(title=title)
        query.update(set__content=content, set__updated_at=datetime.utcnow())

    def extract_knowledge_base(self, path: str = None, urls: list = None):
        """
        path -> file or directory
        urls -> list of urls
        at least 1 phải tồn tại
        """
        if not path and not urls:
            raise ValueError("Either path or urls must be provided.")

        docs = []

        if path:
            if os.path.isfile(path):
                docs.extend(self._extract_from_file(path))
            elif os.path.isdir(path):
                docs.extend(self._extract_from_dir(path))
            else:
                raise ValueError(f"Invalid path: {path}")

        if urls:
            docs.extend(self._extract_from_urls(urls))

        return docs


    def _extract_from_file(self, file_path: str):
        return Docx2txtLoader(file_path).load()


    def _extract_from_dir(self, dir_path: str):
        docs = []
        for filename in os.listdir(dir_path):
            if filename.endswith(".docx"):
                full_path = os.path.join(dir_path, filename)
                docs.extend(self._extract_from_file(full_path))
        return docs


    def _extract_from_urls(self, urls: list):
        docs = []
        for url in urls:
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                doc = Docx2txtLoader(io.BytesIO(resp.content)).load()
                docs.extend(doc)
            except Exception as e:
                print(f"Download error {url}: {e}")
        return docs


    def list_sessions(self, user_id: str = None, limit: int = None):
        query = ChatHistory.objects

        if user_id:
            query = query.filter(user_id=user_id)

        if limit:
            query = query[:limit]

        return query
