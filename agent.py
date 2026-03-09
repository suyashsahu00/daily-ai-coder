import os
from datetime import datetime
import google.generativeai as genai

# Configure the API key using environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it in GitHub Secrets.")

genai.configure(api_key=api_key)

def generate_code():
    """Asks the AI to generate a piece of code."""
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    Write a single, useful Python snippet. It could be an algorithm, data structure, or a utility function.
    Include comments explaining how it works.
    Return ONLY the raw python code. Do not wrap it in markdown block quotes like ```python.
    """
    
    response = model.generate_content(prompt)
    
    # Clean up possible markdown wrappers if the AI still returns them
    text = response.text.strip()
    if text.startswith("```python"):
        text = text[len("```python"):].strip()
    if text.startswith("```"):
        text = text[len("```"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
        
    return text

def main():
    print("Generating code...")
    new_code = generate_code()
    
    date_str = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    filename = f"generated_code/script_{date_str}.py"
    
    os.makedirs("generated_code", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_code)
        
    print(f"Saved generated code to {filename}")

if __name__ == "__main__":
    main()
