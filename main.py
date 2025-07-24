import sys
from dotenv import load_dotenv
from src.services.llm_service import LLMService

load_dotenv()

def main():
    try:
        # If processing email piped from procmail/stdiin, read from sys.stdin
        email_content = sys.stdin.read()
        # Initialize LLMService, probably passing email string as argument
        extractor = LLMService()
        result = extractor.extract_structured(email_content=email_content)
        print("LLM extraction result:", result)
        print("Extraction process completed.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)     # Signal failure upstream

if __name__ == "__main__":
    main()
