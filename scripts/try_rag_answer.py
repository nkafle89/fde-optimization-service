
from dotenv import load_dotenv

from app.rag.retriever import DocumentRetriever
from app.rag.rag_service import RAGService

load_dotenv()

retriever = DocumentRetriever()

retriever.index_document(
    "data/knowledge/transportation_policy.md"
)

rag = RAGService(retriever=retriever)

questions = [
    "What should happen when DC capacity is insufficient?",
    "Can we use an external fulfillment provider?",
    "What is the objective of transportation optimization?",
    "What is the company's maximum driver working time?",
]

for question in questions:
    print(f"\nQUESTION: {question}")
    print(f"ANSWER: {rag.answer(question)}")
