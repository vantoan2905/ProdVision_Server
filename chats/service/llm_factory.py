from llama_index.llms.groq import Groq
from config import settings

_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = Groq(
            model="llama-3.1-8b-instant",
            api_key=settings.GROQ_API_KEY,
            temperature=0.0,
        )
    return _llm_instance
