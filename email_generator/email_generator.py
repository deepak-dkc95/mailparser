from email.message import EmailMessage
from email.utils import formatdate, make_msgid
import pathlib, base64, random, string, glob, os

# NATO phonetic alphabet
NATO_PHONETIC = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey",
    "xray", "yankee", "zulu"
]

# Subject keywords
MAINTENANCE_KEYWORDS = ["maintenance", "outage", "notification", "bill", "interrupt"]
MODIFIER_KEYWORDS = ["", "cancelled", "postponed", "rescheduled"]

# Random sentence templates for body content
BODY_TEMPLATES = [
    "We are writing to inform you about {subject_content}.",
    "Please be advised that {subject_content} is scheduled.",
    "This is a notification regarding {subject_content}.",
    "Important update: {subject_content} requires your attention.",
    "We would like to notify you that {subject_content} will take place.",
    "Please note that {subject_content} has been arranged.",
    "This message is to inform you about {subject_content}.",
    "We want to keep you informed about {subject_content}.",
]

def count_existing_eml_files(directory):
    """Count existing .eml files in the directory"""
    eml_files = glob.glob(str(directory / "mail_*.eml"))
    return len(eml_files)

def generate_alphanumeric_sequence():
    """Generate 6-10 character random alphanumeric sequence (uppercase + digits)"""
    length = random.randint(6, 10)
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_subject():
    """Generate subject with required keywords"""
    # Choose main keyword
    main_keyword = random.choice(MAINTENANCE_KEYWORDS)
    
    # Optionally add modifier (only for maintenance)
    if main_keyword == "maintenance":
        modifier = random.choice(MODIFIER_KEYWORDS)
        if modifier:
            main_keyword = f"{modifier} {main_keyword}"
    
    # Generate alphanumeric sequence
    sequence = generate_alphanumeric_sequence()
    
    # Create filler words (6-12 total words, minus our 2-3 keywords)
    filler_words = [
        "system", "server", "network", "update", "scheduled", "urgent", "immediate",
        "required", "attention", "notice", "alert", "service", "downtime", "window",
        "please", "review", "action", "needed", "critical", "important", "reminder"
    ]
    
    # Calculate how many filler words we need
    keyword_count = len(main_keyword.split()) + 1  # +1 for sequence
    total_words = random.randint(6, 12)
    filler_count = max(0, total_words - keyword_count)
    
    selected_fillers = random.sample(filler_words, min(filler_count, len(filler_words)))
    
    # Combine all words and shuffle
    all_words = main_keyword.split() + [sequence] + selected_fillers
    random.shuffle(all_words)
    
    return ' '.join(all_words).title()

def generate_body(subject, company_keyword):
    """Generate body content based on subject"""
    # Extract key content from subject for body reference
    subject_lower = subject.lower()
    
    # Generate 2-4 sentences restating the subject
    num_sentences = random.randint(2, 4)
    sentences = []
    
    for _ in range(num_sentences):
        template = random.choice(BODY_TEMPLATES)
        sentence = template.format(subject_content=subject.lower())
        sentences.append(sentence)
    
    # Add some additional context sentences
    additional_context = [
        "We appreciate your understanding and cooperation.",
        "If you have any questions, please don't hesitate to contact us.",
        "Thank you for your patience during this time.",
        "We will keep you updated on any developments.",
        "Please ensure all necessary preparations are completed.",
        "We apologize for any inconvenience this may cause.",
    ]
    
    sentences.append(random.choice(additional_context))
    
    body = '\n\n'.join(sentences)
    
    # Add signature
    signature = f"\n\nBest regards,\nBrian Lara\n{company_keyword.title()} Enterprises"
    
    return body + signature

def generate_eml_files(count=10):
    """Generate specified number of .eml files"""
    # Create output directory structure: emails/sample_eml/
    emails_dir = pathlib.Path("emails")
    out_dir = emails_dir / "sample_eml"
    
    # Create directories if they don't exist
    emails_dir.mkdir(exist_ok=True)
    out_dir.mkdir(exist_ok=True)
    
    # Count existing files to determine starting number
    existing_count = count_existing_eml_files(out_dir)
    start_index = existing_count
    
    print(f"Output directory: {out_dir}")
    print(f"Found {existing_count} existing .eml files")
    print(f"Generating {count} new files starting from index {start_index}")
    
    for i in range(start_index, start_index + count):
        # Select random NATO phonetic word for sender
        keyword = random.choice(NATO_PHONETIC)
        
        msg = EmailMessage()
        msg["From"] = f"nobody@{keyword}.com"
        msg["To"] = "somebody@example.com"
        
        # Generate subject with required keywords
        subject = generate_subject()
        msg["Subject"] = subject
        
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()

        # Generate body content
        body = generate_body(subject, keyword)
        msg.set_content(body)

        # Add a tiny dummy attachment (optional)
        if random.choice([True, False]):  # 50% chance of attachment
            pdf_bytes = b"%PDF-1.4\n%..." + bytes(random.randint(32, 126) for _ in range(128))
            msg.add_attachment(pdf_bytes,
                              maintype="application", 
                              subtype="pdf",
                              filename=f"document_{generate_alphanumeric_sequence()}.pdf")

        # Write to file with proper numbering
        filename = f"mail_{i:02d}.eml"
        filepath = out_dir / filename
        with open(filepath, "wb") as f:
            f.write(msg.as_bytes())
        
        print(f"Generated: {filepath}")
    
    total_files = existing_count + count
    print(f"\nCompleted! Total .eml files in {out_dir}: {total_files}")

if __name__ == "__main__":
    # Generate 10 new .eml files
    generate_eml_files(10)
