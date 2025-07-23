import os
import random
import json
import datetime
from dotenv import load_dotenv
import cohere
from generator_config import VENDORS, MODEL, PROMPT_PATH

load_dotenv()

class VendorEmailGenerator:
    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable not found.")
        self.co = cohere.ClientV2(api_key=self.cohere_api_key)

        self.model = MODEL
        self.vendors = VENDORS
        self.prompt_path = PROMPT_PATH
        self.prompt_template = self.load_prompt()
        self.today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    def load_prompt(self):
        with open(self.prompt_path, "r") as f:
            return f.read()

    def random_vendor_and_circuit(self):
        vendor = random.choice(list(self.vendors.keys()))
        circuits = random.sample(self.vendors[vendor], k=random.choice([1, 2]))
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
        if vendor is None or circuits is None:
            vendor, circuits = self.random_vendor_and_circuit()
        if vendor_ticket is None:
            vendor_ticket = self.random_vendor_ticket()
        prompt = self.fill_prompt(vendor, circuits, vendor_ticket)
        response = self.co.chat(
            model=self.model,
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
