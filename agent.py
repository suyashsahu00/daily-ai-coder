import os
from datetime import datetime


def generate_code():
    """Returns a simple Python snippet."""
    
    text = """
# Simple Python snippet
def add_numbers(a, b):
    # Returns the sum of a and b
    return a + b

def subtract_numbers(a, b):
    # Returns the difference of a and b
    return a - b

print(f"10 + 5 = {add_numbers(10, 5)}")
print(f"10 - 5 = {subtract_numbers(10, 5)}")
"""
    return text.strip()

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
