import os
import json
import re
from typing import Dict, Any
import random
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator. 
Your task is to generate a coding question with multiple choice answers.
The question should be appropriate for the specified difficulty level.

For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

Return the challenge strictly as a JSON object in the following format:
{
    "title": "The question title",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer_id": 0,
    "explanation": "Detailed explanation of why the correct answer is right"
}

Only return the JSON. Do not include anything else.
"""

    try:
        # Call Groq API
        # Add a random seed to the prompt to avoid caching/repetition
        random_seed = f"{difficulty}-{time.time()}-{random.randint(1, 1000)}"
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge and return only the JSON object. Random seed: {random_seed}"}
            ],
            temperature=0.7
        )

        # Extract content from response
        content = response.choices[0].message.content.strip()
        print("🔍 Raw response content:\n", content)

        # Use regex to extract JSON object from the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON found in the response.")

        json_str = json_match.group(0)

        # Parse JSON
        try:
            challenge_data = json.loads(json_str)
        except json.JSONDecodeError as decode_err:
            print("❌ JSON decode error:", decode_err)
            raise ValueError("The response was not valid JSON. Model may not have followed instructions.")

        # Validate required fields
        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data

    except Exception as e:
        print("⚠️ Error occurred:", e)
        # Optional fallback example
        return {
            "title": "Basic Python List Operation",
            "options": [
                "my_list.append(5)",
                "my_list.add(5)",
                "my_list.push(5)",
                "my_list.insert(5)",
            ],
            "correct_answer_id": 0,
            "explanation": "In Python, append() is the correct method to add an element to the end of a list."
        }


# ✅ Example usage
if __name__ == "__main__":
    challenge = generate_challenge_with_ai("easy")
    print("\n✅ Final Challenge JSON:")
    print(json.dumps(challenge, indent=4))
