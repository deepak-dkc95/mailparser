from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "logs" / "parser.log"

PROMPT_PATH = PROJECT_ROOT / "prompts" / "llm_prompt.txt"
EMAIL_PATH = PROJECT_ROOT / "tests" / "test_email.txt"

MODEL = "command-a-03-2025"
