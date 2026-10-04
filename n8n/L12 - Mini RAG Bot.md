---
tags: [n8n, lab, tier3, ai, rag, capstone]
difficulty: 5
time: 3 hr
---
# L12 - Mini RAG Bot

**Goal:** Answer questions from your own documents, grounded in retrieved text.

**Concepts:** RAG (retrieval-augmented generation), chunking, embeddings, vector store, retrieval grounding.

## Concept First
Retrieval-augmented generation works in two phases. First you index documents: split them into chunks, convert each chunk to an embedding vector, and store it. Then at question time you embed the question, retrieve the most similar chunks, and pass them to the model as context. The model answers from that context rather than from memory alone.

## Steps
1. Write a short policy document of about 2 pages. Make up a fictional company, which keeps it safe to use.
2. **Indexing workflow:** Manual Trigger → Default Data Loader → Recursive Character Text Splitter (chunk 500, overlap 50) → Embeddings node → an in-memory or company-approved vector store.
3. **Query workflow:** Chat Trigger → Question and Answer Chain (or an AI Agent with a vector store tool) → answer.
4. Ask questions answerable from the document, then one that is not. The bot should say it doesn't know.
5. Change chunk size to 100 and then 2000. Note how answer quality changes.

> [!hint]- Hint 1
> If answers are wrong, inspect what the retriever returned before blaming the model. Retrieval is usually the problem.

> [!hint]- Hint 2
> Add "If the context does not contain the answer, say you don't know" to the prompt. Without it, models often guess.

> [!hint]- Hint 3
> Use the same embedding model for indexing and querying. Mixing models silently breaks retrieval.

## Stretch
Add a source citation to each answer by returning the chunk's metadata.

## Reflection
- Which change made the biggest difference, chunk size, overlap, the prompt, or the retrieval count? Why?
