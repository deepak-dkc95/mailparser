from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOG_FILE = PROJECT_ROOT / "logs" / "parser.log"

PROMPT_PATH = PROJECT_ROOT / "prompts" / "llm_prompt.txt"

MODEL = "command-a-03-2025"

IMPORTANT_KEYWORDS = ["outage", "notification", "maintenance", "notice", "important", "alert"]
CANCELLATION_KEYWORDS = ["cancelled", "postponed", "cancellation"]