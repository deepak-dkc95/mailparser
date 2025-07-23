import os
import json
import cohere
from src.services.utils import logger, load_file
from src.config import MODEL, PROMPT_PATH, EMAIL_PATH

class LLMService:
    def __init__(self, model=MODEL, prompt_path=PROMPT_PATH, email_path=EMAIL_PATH):
        self.model = model
        self.prompt_path = prompt_path
        self.email_path = email_path

    def fill_prompt(self, prompt_template, email_text):
        return prompt_template.replace("{maint_email}", email_text)

    def extract_structured(self, email_path=None, prompt_path=None):
        email_path = email_path or self.email_path
        prompt_path = prompt_path or self.prompt_path

        email_text = load_file(email_path)
        prompt_template = load_file(prompt_path)
        prompt = self.fill_prompt(prompt_template, email_text)

        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            logger.error("No COHERE_API_KEY found in environment.")
            raise ValueError("COHERE_API_KEY not set in environment")

        try:
            co = cohere.ClientV2(api_key=api_key)
            response = co.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=950,
                response_format={"type": "json_object"},
            )
            json_str = ""
            for piece in response.message.content:
                if piece.type == "text":
                    json_str += piece.text
            llm_json = json.loads(json_str.strip())
        except Exception as e:
            logger.error(f"LLM extraction or parsing failed: {e}")
            raise

        output_str = json.dumps(llm_json, ensure_ascii=False)
        logger.info(f"Structured LLM JSON output: {output_str}")

        return llm_json
