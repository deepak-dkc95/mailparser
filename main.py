#!/usr/bin/env python3

import sys
from dotenv import load_dotenv
from src.config import *
from src.services.utils import logger, is_important, is_maintenance, check_cancelled
from src.services.llm_service import LLMService
from src.services.email_processor import EmailProcessor

def process_email():
    # Step 1: Parse email from stdin
    email_msg = EmailProcessor.parse_eml()  # returns email.message.EmailMessage
    
    # Step 2: Check importance
    subject = (email_msg.get('Subject', '') or '').strip()
    if not is_important(subject):
        logger.info("Email ignored: not important.")
        return

    logger.info("Email is important, subject: '%s'", subject)

    # Step 3: Check if maintenance related
    if not is_maintenance(subject):
        logger.info("Important email, but not maintenance related.")
        return

    # Step 4: Check if maintenance is cancelled
    if check_cancelled(subject):
        logger.info("Maintenance has been cancelled: subject contains cancellation keyword.")
        return

    # Step 5: Passed all checks -- run LLM extraction
    msg_string = EmailProcessor.get_msg_string(email_msg)
    logger.info("Processing maintenance email with Cohere LLM")

    llm = LLMService()
    llm_output = llm.extract_structured(email_text=msg_string)

def main():
    try:
        logger.info("Starting email processing script.")
        process_email()
        logger.info("Script completed successfully.")
    except Exception as e:
        logger.error(f"email/main.py pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    load_dotenv()
    main()
