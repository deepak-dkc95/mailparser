import os
import random
import json
import datetime
from pathlib import Path
from dotenv import load_dotenv
import cohere

load_dotenv()

class VendorEmailGenerator:
    MODEL = "command-a-03-2025"
    PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "generator_prompt.txt"
    VENDORS = {
        "Airtel": ["345678912", "345678915", "345678918"],
        "Reliance": ["REL98765345", "REL98765354", "REL98765397"],
        "Lumen": ["431098345-2", "401034345-1", "101098393-2"],
        "Zayo": ["ABCD/234567//ZY", "EFGH/894567//ZY", "IJKL/267567//ZY"],
        "PCCW": ["SR 2345/ABC - EFG/RT1234", "SR 6754/QRT - FGH/RT9876", "SR 0432/XYZ - QWE/RT8765"],
        "AT&T": ["ATT1234", "ATT4567", "ATT5423"],
        "TATA": ["091ABC234567890", "091EDF234561234", "04FCR234567765"]
    }

    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable not found.")
        self.co = cohere.ClientV2(api_key=self.cohere_api_key)
        self.prompt_template = self.load_prompt()
        self.today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def load_prompt(cls):
        with open(cls.PROMPT_PATH, "r") as f:
            return f.read()

    @classmethod
    def random_vendor_and_circuit(cls):
        vendor = random.choice(list(cls.VENDORS.keys()))
        circuits = random.sample(cls.VENDORS[vendor], k=random.choice([1, 2]))
        return vendor, circuits

    @staticmethod
    def random_vendor_ticket():
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(6, 10)))

    def fill_prompt(self, vendor, circuits, vendor_ticket):
        prompt = self.prompt_template
        return (
            prompt
            .replace("{vendor}", vendor)
            .replace("{circuit_ids}", ", ".join(circuits))
            .replace("{vendor_ticket}", vendor_ticket)
            .replace("{date}", self.today_str)
        )

    def generate_email(self, vendor=None, circuits=None, vendor_ticket=None):
        # Allow overriding vendor/circuits/ticket for testing
        if vendor is None or circuits is None:
            vendor, circuits = self.random_vendor_and_circuit()
        if vendor_ticket is None:
            vendor_ticket = self.random_vendor_ticket()
        prompt = self.fill_prompt(vendor, circuits, vendor_ticket)
        response = self.co.chat(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=850,
            response_format={"type": "json_object"},
        )
        json_str = ""
        for piece in response.message.content:
            if piece.type == "text":
                json_str += piece.text
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"Parsing error:\n{json_str}\nError: {e}")
            return None

    def generate_batch(self, n=5):
        return [self.generate_email() for _ in range(n)]


# === DEMO / MAIN USAGE ===
if __name__ == "__main__":
    generator = VendorEmailGenerator()
    print(generator.random_vendor_and_circuit())
    print(generator.random_vendor_ticket())
    # Single
    email = generator.generate_email()
    print(json.dumps(email, indent=2, ensure_ascii=False))
    # Batch
    # print("\n--- Batch Generation ---")
    # batch = generator.generate_batch(5)
    # for item in batch:
    #     print(json.dumps(item, indent=2, ensure_ascii=False), end='\n\n')
