from pathlib import Path

# Cohere LLM model to use
# Updated to the latest model as of March 2025
# This model is optimized for generating structured JSON outputs, which is ideal for our email generation task
MODEL = "command-a-03-2025"

# Path to the prompt file
PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "generator_prompt.txt"

# Path to a sample EML file for testing
SAMPLE_EML_PATH = Path(__file__).parent.parent / "emails" / "sample_eml"

# Dictionary of vendors and their circuit IDs
VENDORS = {
    "Airtel": ["345678912", "345678915", "345678918"],
    "Reliance": ["REL98765345", "REL98765354", "REL98765397"],
    "Lumen": ["431098345-2", "401034345-1", "101098393-2"],
    "Zayo": ["ABCD/234567//ZY", "EFGH/894567//ZY", "IJKL/267567//ZY"],
    "PCCW": ["SR 2345/ABC - EFG/RT1234", "SR 6754/QRT - FGH/RT9876", "SR 0432/XYZ - QWE/RT8765"],
    "AT&T": ["ATT1234", "ATT4567", "ATT5423"],
    "TATA": ["091ABC234567890", "091EDF234561234", "04FCR234567765"]
}

LOREM_WORDS = [
    "lorem", "ipsum", "dolor", "amet", "consectetur", "adipiscing",
    "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore"
]

# Randomly generated keywords and modifiers for email subjects
KEYWORDS = ["outage", "notification", "maintenance", "notice", "important", "alert"]
MODIFIERS = ["cancelled", "postponed", "rescheduled"]
