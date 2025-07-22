import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeneratorLLM:
    def __init__(self, model: str = "gpt-4o") -> None:
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not found")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_email_content(self, additional_context: str = "") -> Optional[Dict]:
        """
        Generate email content using OpenAI API.
        """
        try:
            # Build correct path to the prompt file
            script_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(script_dir, "..", "prompts", "generator_prompt.txt")

            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt = f.read().strip()

            if additional_context:
                prompt += f"\n\nAdditional context: {additional_context}"
            
            logger.info(f"Generating email content using {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates realistic network vendor emails in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                if "```json" in content and "```" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    json_content = content[json_start:json_end].strip()
                    return json.loads(json_content)
                else:
                    logger.error("Response is not valid JSON format")
                    return None

        except Exception as e:
            logger.error(f"Error generating email content: {e}")
            return None
    
    def generate_multiple_emails(self, count: int = 5, contexts: list = None) -> list:
        emails = []
        contexts = contexts or [""] * count
        
        for i in range(count):
            context = contexts[i] if i < len(contexts) else ""
            logger.info(f"Generating email {i+1}/{count}")
            email_data = self.generate_email_content(context)
            if email_data:
                emails.append(email_data)
            else:
                logger.warning(f"Failed to generate email {i+1}")
        
        return emails

def test_generator():
    try:
        generator = GeneratorLLM()
        email_data = generator.generate_email_content()
        
        if email_data:
            print("Generated email data:")
            print(json.dumps(email_data, indent=2))
        else:
            print("Failed to generate email data")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_generator()
