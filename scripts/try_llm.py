from dotenv import load_dotenv

from app.services.llm_service import LLMService

load_dotenv()

service = LLMService()

result = service.parse_optimization_request(
    "I have 3 distribution centers and 5 stores. "
    "Minimize transportation cost while respecting "
    "DC capacity and satisfying store demand."
)

print(result.model_dump_json(indent=2))