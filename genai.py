import os
import google.generativeai as genai
import time

# Configure Gemini API (Replace with your actual API key)
GEMINI_API_KEY = (
    "AIzaSyCETgHJRn3KzKuZjtuAKj2s4hRBUH-QHQY"  # Get it from: https://ai.google.dev/
)
genai.configure(api_key=GEMINI_API_KEY)


def generate_code(prompt, model_name='gemini-1.5-flash'):
    """Generate Python code using AI."""
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(
            f"Generate a Python code snippet for: {prompt}. "
            "Provide only the code (no explanations)."
        )
        time.sleep(1)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Removed CLI main() entrypoint for Django integration
