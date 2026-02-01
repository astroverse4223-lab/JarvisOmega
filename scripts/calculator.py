"""
Calculator - Perform quick calculations
"""
import math
import re

def safe_eval(expression):
    """Safely evaluate mathematical expressions"""
    # Remove any non-math characters
    allowed = set('0123456789+-*/().^ ')
    cleaned = ''.join(c for c in expression if c in allowed or c.isalpha())
    
    # Replace ^ with **
    cleaned = cleaned.replace('^', '**')
    
    # Define safe math functions
    safe_dict = {
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'pi': math.pi,
        'e': math.e
    }
    
    try:
        result = eval(cleaned, {"__builtins__": {}}, safe_dict)
        return result
    except Exception as e:
        return None

def main():
    """Demonstrate calculator with example calculations"""
    examples = [
        ("15 * 8", 15 * 8),
        ("100 / 4", 100 / 4),
        ("2^10", 2**10),
        ("sqrt(144)", math.sqrt(144))
    ]
    
    print("CALCULATOR EXAMPLES:\n")
    for expr, result in examples:
        print(f"{expr} = {result}")
    
    print("\nCalculator ready for voice commands")

if __name__ == "__main__":
    main()
