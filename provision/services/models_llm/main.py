import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from sentence_transformers import SentenceTransformer

from model_llm_service import DocumentStorage, DocumentRetrieval, ModelLLMService_Local, ModelLLMService_API, Generation, Orchestration




# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    # 1. Init storage and embedder
    storage = DocumentStorage()
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    storage.add_documents(
        [
            "The capital of France is Paris.",
            "The Eiffel Tower is located in Paris.",
            "Berlin is the capital of Germany."
        ],
        embedder
    )

    # 2. Init retriever
    retriever = DocumentRetrieval(storage)

    # 3. Choose LLM service (Local or API)
    llm_service = ModelLLMService_Local("gpt2")  # small model for demo
    # llm_service = ModelLLMService_API(model_name="gpt-3.5-turbo", api_key="YOUR_KEY", api_url="API_URL")

    generator = Generation(llm_service)

    # 4. Orchestrate
    orchestrator = Orchestration(retriever, generator)

    # 5. Ask question
    response = orchestrator.ask("Where is the Eiffel Tower?", embedder)
    print("Bot:", response)
