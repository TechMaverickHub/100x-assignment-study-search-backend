# prd.md

## 📝 Abstract
A lightweight, local-only RAG MVP for undergraduate students to quickly search and understand long lecture PDFs. The system ingests PDFs, chunks and embeds content, retrieves relevant passages, generates answers with citations, evaluates performance via RAGAS, applies minimal personalization, and exposes everything through a simple Streamlit UI. The rationale: enable fast, accurate study support before exams.

## 🎯 Business Objectives
- Improve students’ study efficiency by enabling instant answers from lecture materials.
- Demonstrate end-to-end GenAI competency across ingestion, embedding, retrieval, generation, evaluation, and personalization.
- Deliver a deployable MVP for academic submission within the given deadline.

## 📊 KPI
| GOAL             | METRIC                 | QUESTION                                             |
|------------------|-------------------------|------------------------------------------------------|
| Answer Accuracy   | RAGAS Accuracy %        | Are answers factually correct relative to the PDFs?  |
| Speed             | Avg. Retrieval Time     | How fast is each query served locally?               |
| User Delight      | Satisfaction Score (1–5)| Do students feel this tool helps them revise faster? |

## 🏆 Success Criteria
- MVP runs end-to-end locally with no cloud dependencies.
- Answers include citations and hit minimum RAGAS accuracy >60%.
- Query response time < 2 seconds on CPU.
- User feedback from peers is positive (≥4/5 satisfaction).

## 🚶‍♀️ User Journeys
1. Student uploads a lecture PDF.
2. System auto-chunks, embeds, and stores vectors.
3. Student asks a question in UI.
4. System retrieves top relevant chunks and synthesizes an answer with citation.
5. Student sees result and optionally re-asks follow-up questions.
6. Student can run a quick evaluation on sample Q&A to check quality.

## 📖 Scenarios
- Student uploading one PDF just before an exam.
- Asking concept-explanation queries.
- Asking location queries.
- Running evaluation for quality assurance.

## 🕹️ User Flow
- Upload PDF → Parse → Chunk → Embed → Store vectors
- Ask question → Retrieve top-k chunks → LLM → Answer + citations
- Evaluation → Load Q/A → RAGAS → Metrics
- Personalization → Save name + tone → Apply in responses
- Deploy → Streamlit UI

## 🧰 Functional Requirements
| SECTION     | SUB-SECTION | USER STORY & EXPECTED BEHAVIORS                          | SCREENS          |
|-------------|-------------|------------------------------------------------------------|------------------|
| Upload      | Single PDF  | Upload PDF; system validates & ingests                    | Streamlit page   |
| Embeddings  | FAISS Store | Chunk PDF, embed using open-source model                  | Backend only     |
| Query       | RAG         | User enters question; system retrieves + answers          | Streamlit chat   |
| Citations   |             | Show top chunk sources with metadata                      | Inline           |
| Evaluation  | RAGAS       | Run RAGAS on sample Q&A set, show metrics                 | Metrics page     |
| Personalization | Tone/Name | Store name; steer answers using tone                     | Settings         |
| Deployment  | Local-only  | App runs via `streamlit run app.py`                       | Local            |

## 📐 Model Requirements
| SPECIFICATION          | REQUIREMENT                        | RATIONALE |
|------------------------|------------------------------------|-----------|
| Open vs Proprietary    | Open-source only                   | Local-only |
| Context Window         | ~4k–8k tokens                      | Enough for chunks |
| Modalities             | Text                               | PDFs + questions |
| Fine Tuning Capability | Not required                       | RAG handles facts |
| Latency                | P50 < 2s                           | Smooth use |
| Parameters             | Small model (e.g., 7B)             | CPU-friendly |

## 🧮 Data Requirements
- No fine-tuning.
- Chunk size 300–500 tokens.
- One PDF required.
- Synthetic Q&A for RAGAS (5–10).
- FAISS local storage.

## 💬 Prompt Requirements
- Personalization variables.
- Structured outputs: answer + citations.
- Guardrails: refuse hallucinations.
- Concise academic tone.

## 🧪 Testing & Measurement
### Offline
- RAGAS metrics: relevancy, recall, faithfulness.
- Threshold: ≥60%.

### Online
- Manual QA.
- Error checks: missing citations, empty retrieval.

### Rollback
- If no relevant content → “No relevant content found.”

## ⚠️ Risks & Mitigations
| RISK                               | MITIGATION                       |
|------------------------------------|----------------------------------|
| Ingestion breaks on messy PDFs     | Fallback to alternate parsing    |
| Poor accuracy from chunking        | Tune chunk size + overlap        |

## 💰 Costs
- Local compute only.
- Open-source models.
- Minimal storage.

## 🔗 Assumptions & Dependencies
- One PDF at a time.
- FAISS vector store.
- Streamlit UI.
- Local CPU/GPU.

## 🔒 Compliance/Privacy/Legal
- Fully local.
- No cloud storage.
- No PII retention.

## 📣 GTM/Rollout Plan
- Day 1: Ingestion + embeddings  
- Day 2: RAG pipeline  
- Day 3: RAGAS + personalization  
- Day 4: UI polish + testing  
- Final Day: Submit MVP

