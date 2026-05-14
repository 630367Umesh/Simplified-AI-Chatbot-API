# Simplified AI Chatbot API

A production-ready, multi-provider Chatbot API supporting Gemini, Groq, and Llama. Designed for simplicity with a single Master API Key and no database requirements.

## Features
- **Multi-LLM Router**: Switch between `gemini`, `groq`, and `llama` dynamically.
- **Single Auth**: Secure access via a single `MASTER_API_KEY` in the `x-api-key` header.
- **FastAPI Core**: High-performance asynchronous backend.
- **Zero Database**: No complex database setup or maintenance required.
- **Deployment Ready**: Native Render support without Docker.

## Setup & Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file based on `.env.example`:
   ```env
   MASTER_API_KEY=your_secret_key
   GEMINI_API_KEY=your_gemini_key
   GROQ_API_KEY=your_groq_key
   LLAMA_API_URL=http://localhost:11434/api/generate
   ```

3. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Usage

### Chat Endpoint
- **Endpoint**: `POST /v1/chat`
- **Header**: `x-api-key: your_secret_key`
- **Body**:
  ```json
  {
    "message": "Hello AI",
    "provider": "groq"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "provider": "groq",
    "output_text": "..."
  }
  ```

## Deployment (Render)
1. Push to GitHub.
2. Connect to Render as a Web Service.
3. Add Environment Variables (including `MASTER_API_KEY`).
4. Render will use `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
