# finsage-ai


```text
User
  ↓
Frontend
  ↓
FastAPI
  ↙︎             ↘︎
(uploads/query)   ↘︎
 [OCR/Embed/Chunk] ↘︎
      ↓             ↘︎
 Milvus (embeddings) Neo4j (graph)
      ↑              ↑
 [Retrieve context]  ↑
      ↓              ↑
FastAPI aggregates context (incl. user profile from Postgres)
      ↓
Gemini API (LLM) ← [Prompt with context]
      ↓
FastAPI ← [LLM answer + citations]
      ↓
Frontend (show answer)
      ↓
Postgres (log session/conversation)
```
