# StudySearch

StudySearch is a simple, learning-focused Retrieval-Augmented Generation (RAG) application built using **Google Gemini File Search**. The goal of this project is to deeply understand grounded retrieval—ensuring that all answers come strictly from the uploaded documents, with zero hallucinations.

## 🚀 Features

- Upload PDFs and ingest them into Gemini File Search
- Create isolated file-search stores per user
- Query documents with full grounding
- Extract actual text chunks used by Gemini (not just titles)
- Enforce **truth-first AI**: if the answer isn’t in the document, the system responds with  
  *“I don't know. The answer is not present in the document.”*
- Django REST Framework backend with clean, scalable APIs

## 🧩 Architecture Overview

1. **Upload PDF** → stored in Django → uploaded to Gemini File Search  
2. **Gemini store creation** → store_name generated per document  
3. **Query API** → system prompt enforces grounded answers  
4. **Grounding extraction** → retrieved_context.text chunks returned to user  
5. **Frontend / Client App** → can render accurate grounded responses

## 📡 Core APIs

### `POST /api/filesearch/upload/`
Upload and ingest a PDF into Gemini File Search.

### `POST /api/filesearch/query/`
Query the ingested document.  
If the answer isn’t found, returns a safe fallback.

### `GET /api/filesearch/stores/list/`
View all your uploaded documents.

## 🛡 Hallucination Prevention

StudySearch forces Gemini to respond using only the retrieved chunks.  
If no chunk supports the answer → the system automatically replies:

```
I don't know. The answer is not present in the document.
```

This makes StudySearch ideal for learning real-world RAG behaviors.

## 🛠 Tech Stack

- **Python / Django**
- **Django REST Framework**
- **Google Gemini File Search**
- **PostgreSQL (recommended)**
- **Docker-ready structure (optional)**

## 📘 Why This Project Exists

RAG is powerful—but easy to misunderstand. StudySearch was built to explore:

- How document grounding really works
- What LLMs do when grounding is missing
- How to enforce strict source adherence
- Practical chunk extraction and retrieval flows

## 📄 License

MIT License

---

Feel free to fork, extend, or critique this project.  
Always open to learning from the community!
