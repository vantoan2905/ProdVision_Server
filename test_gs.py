import requests
import json

def stream_ollama(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True  # bật chế độ stream
    }
    
    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    print(data["response"], end="", flush=True)  # in real-time
                if data.get("done", False):
                    print()  # xuống dòng khi kết thúc
                    break


# Demo chatbot real-time
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("Bot:", end=" ", flush=True)
    stream_ollama(user_input)
