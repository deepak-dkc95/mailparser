from dotenv import load_dotenv
from src.services.llm_service import LLMService

load_dotenv()

if __name__ == "__main__":
    extractor = LLMService()
    extractor.extract_structured()