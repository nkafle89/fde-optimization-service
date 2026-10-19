
from dotenv import load_dotenv

from app.rag.retriever import DocumentRetriever

load_dotenv()

retriever = DocumentRetriever()

retriever.index_document(
    "data/knowledge/transportation_policy.md"
)

questions = [
    "What happens when distribution center capacity is insufficient?",
    "Can we use an external fulfillment provider?",
    "What is the objective of transportation optimization?",
]

for question in questions:
    print(f"\nQUESTION: {question}")

    results = retriever.retrieve(question, top_k=2)

    for result in results:
        print(f"\nScore: {result['score']:.4f}")
        print(result["text"])
