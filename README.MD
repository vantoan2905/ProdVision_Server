

# 🧠 ProdVision – Personal Multimodal AI Assistant

ProdVision is a **personal AI assistant project** designed to support **text-based and image-based interactions**.
The system allows users to upload images, extracts text using **OCR**, and passes the extracted content to a **Large Language Model (LLM)** for reasoning and response generation.

This project is built **for personal learning and productivity**, focusing on **AI model integration, system design, and real-time interaction**, rather than large-scale production.

---
## 🔗 Related Repositories

- Backend (this repo): https://github.com/vantoan2905/ProdVision_Server
- Frontend (UI): https://github.com/vantoan2905/ProdVision_UI

---

## ✨ Key Features

* 📷 **Image Upload & OCR**
  Extracts text from user-uploaded images using pretrained OCR models.

* 🧠 **LLM Integration (Tool Calling)**
  OCR results are provided as structured input to the LLM for downstream reasoning.

* ⚡ **Real-time Chat via Server-Sent Events (SSE)**
  Streams incremental LLM responses to the client in real time.

* 🔐 **User & Conversation Management**
  Supports multiple users, conversations, and message history.

* 🐳 **Dockerized Deployment**
  Easy local setup and consistent runtime environment.

---

## 🏗️ System Architecture

```text
Client
  ├── Upload image / send message
  ↓
Backend (Django)
  ├── OCR inference (image → text)
  ├── Tool calling → LLM
  ├── Conversation & context management
  └── SSE streaming response
  ↓
Client (real-time updates)
```

---

## 🛠️ Tech Stack

* **Backend:** Django, Django REST Framework
* **AI / Data Processing:** OCR (pretrained models), OpenCV, NumPy
* **LLM Integration:** Tool-calling workflow
* **Database:** PostgreSQL / SQLite (for local use)
* **Realtime Communication:** Server-Sent Events (SSE)
* **Deployment:** Docker

---

## 📂 Project Structure

```text
ProdVision_Server/
│   ├── users/           # User management
│   ├── config/          # main application
│   ├── chat/            # Conversations & messages
│   ├── files/            # OCR inference pipeline
│   ├── llm/             # LLM integration & tool calls
│   └── core/            # Shared utilities
├── media/               # Uploaded images
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/vantoan2905/ProdVision_Server.git
cd ProdVision_Server
```


---

## 🔐 Environment Configuration

Create a `.env` file in the project root and configure the following environment variables:

### 🗄️ Database (PostgreSQL)

```env
POSTGRES_DB=sv_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/sv_db
```

> For local development, PostgreSQL is recommended.
> You may replace it with SQLite if needed.

---

### ⚙️ Django Settings

```env
SECRET_KEY=your_django_secret_key
DJANGO_SETTINGS_MODULE=app_django.settings
DEBUG=True
```

---

### 📧 Email Configuration (Optional)

Used for features such as notifications or password reset.

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password

DEFAULT_FROM_EMAIL=your_email@gmail.com
ADMIN_EMAIL=your_email@gmail.com
```

> ⚠️ Use **Gmail App Password**, not your real Gmail password.

---

### 🍃 MongoDB (Optional)

Used for storing chat logs or auxiliary data.

```env
MONGO_URI=mongodb://localhost:27017/vantoan
MONGO_DB_NAME=vantoan
```

---

### 🧠 LLM Providers

#### Ollama

```env
OLLAMA_HOST=https://ollama.com
OLLAMA_KEY=your_ollama_api_key
OLLAMA_MODEL=gpt-oss:120b
```

#### OpenAI (Optional)

```env
OPENAI_API_KEY=your_openai_api_key
```

#### Other Models (Optional)

```env
BIGMODEL_KEY=your_bigmodel_api_key
DEEPSEEK_KEY=your_deepseek_api_key
```

---

## ✅ Minimal Required Variables (Quick Start)

If you only want to run the project locally with basic features:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/sv_db
```


---

### Create virtual environment & install dependencies

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

### Apply database migrations

```bash
python manage.py migrate
```

---

### Run the development server

```bash
python manage.py runserver
```

Server will be available at:

```
http://127.0.0.1:8000
```
Swagger documentation:
```
http://127.0.0.1:8000/docs
```
---

## 🐳 Run with Docker (Recommended)

```bash
docker-compose up --build
```

This will start:

* Django backend
* Database service (if configured)

---

## 🔄 Application Workflow

1. User uploads an image or sends a message from the client.
2. Backend processes the image through the **OCR pipeline**.
3. Extracted text is passed to the **LLM as a tool input**.
4. LLM generates a response based on text + conversation context.
5. Response is streamed back to the client using **SSE**.

---

## ⚠️ Project Scope

* This is a **personal project** built for learning and experimentation.
* OCR and LLM models are **pretrained and integrated**, not trained from scratch.
* The system is designed for **personal usage**, not large-scale production.

---

## 📌 Future Improvements

* Improve OCR accuracy for complex layouts and curved text
* Add file type support (PDF, scanned documents)
* Enhance conversation memory and summarization
* Add frontend UI for better user interaction

---

## 📄 License

This project is for **personal and educational purposes**.

---

## 🙋 Author

**Nguyen Van Toan**
AI Engineer – Fresher
GitHub: [https://github.com/vantoan2905](https://github.com/vantoan2905)

---

