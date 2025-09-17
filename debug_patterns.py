#!/usr/bin/env python3
"""
Debug regex patterns for medical information extraction
"""

import re

def test_age_patterns():
    """Test age extraction patterns"""
    
    # Sample text from case reports
    test_texts = [
        "A 74-year-old woman with a history of infiltrating ductal carcinoma",
        "A 68-year-old man with a history of coronary artery disease",
        "A morbidly obese man in his 70s with a medical history",
        "A 45-year-old female patient presented with chest pain",
        "Patient is a 52-year-old male"
    ]
    
    # Age patterns
    age_patterns = [
        r'(\d+)-year-old',
        r'(\d+)\s*year[s]?\s*old',
        r'age[:\s]+(\d+)',
        r'(\d+)\s*years?\s*of\s*age',
        r'in\s*his\s*(\d+)s',
        r'in\s*her\s*(\d+)s',
        r'(\d+)-year-old\s*(male|female|man|woman)',
        r'(\d+)\s*year[s]?\s*old\s*(male|female|man|woman)'
    ]
    
    print("🧪 Testing Age Extraction Patterns")
    print("="*50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test Text {i}: {text}")
        print("-" * 40)
        
        for j, pattern in enumerate(age_patterns, 1):
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                print(f"  Pattern {j}: {pattern}")
                print(f"    Matches: {matches}")
            else:
                print(f"  Pattern {j}: {pattern} - No matches")

if __name__ == "__main__":
    test_age_patterns()
