#!/usr/bin/env python3
"""
Ask Specific Medical Questions
Get structured, specific answers instead of long text chunks
"""

import sys
import json
import os
from intelligent_medical_extractor import query_with_intelligent_extraction

def main():
    """Main function to ask specific medical questions"""
    if len(sys.argv) < 2:
        print("Usage: python ask_specific_question.py \"Your specific question\"")
        print("\nExample questions:")
        print("• What are the patient ages?")
        print("• What is the patient sex/gender?")
        print("• What medications were used?")
        print("• What procedures were performed?")
        print("• What complications occurred?")
        print("• What are the diagnoses?")
        print("• What are the outcomes?")
        print("\n💡 This system gives specific answers, not long text chunks!")
        sys.exit(1)
    
    # Get question from command line arguments
    question = " ".join(sys.argv[1:])
    
    print(f"🧠 Intelligent Medical Question Answering")
    print(f"Question: {question}")
    print("-" * 50)
    
    # Load configuration
    config_file = "case_reports_config.json"
    
    if not os.path.exists(config_file):
        print("❌ No case reports configured.")
        print("💡 Run 'python add_case_report.py' to add case reports first.")
        sys.exit(1)
    
    with open(config_file, 'r') as f:
        case_reports_config = json.load(f)
    
    # Check which case reports exist
    existing_cases = {}
    for case_name, file_path in case_reports_config.items():
        if os.path.exists(file_path):
            existing_cases[case_name] = file_path
        else:
            print(f"⚠️  Warning: Case report not found: {file_path}")
    
    if not existing_cases:
        print("❌ No accessible case reports found.")
        print("💡 Check the file paths in case_reports_config.json")
        sys.exit(1)
    
    print(f"📋 Analyzing {len(existing_cases)} case report(s):")
    for case_name in existing_cases.keys():
        print(f"   • {case_name}")
    
    print("\n🔍 Extracting specific information...")
    
    # Get specific answer
    answer = query_with_intelligent_extraction(question, existing_cases)
    print(f"\n💡 Specific Answer:\n{answer}")

if __name__ == "__main__":
    main()
