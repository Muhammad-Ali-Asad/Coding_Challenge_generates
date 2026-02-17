import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from src.ai_generator import generate_challenge_with_ai
    print("Attempting to generate challenge...")
    challenge = generate_challenge_with_ai("easy")
    print("Generated Challenge Title:", challenge.get("title"))
except Exception as e:
    print("Error:", e)
