#!/usr/bin/env python3
"""
Multi-Case Medical Query Interface
Query multiple medical case reports at once
"""

import sys
import json
import os
from multi_case_rag import query_multiple_cases

def main():
    """Main function to run the multi-case query interface"""
    if len(sys.argv) < 2:
        print("Usage: python query_multiple_cases.py \"Your question here\"")
        print("\nExample questions:")
        print("• What types of complications are mentioned across the cases?")
        print("• What treatments were used in the cases?")
        print("• What are the common patient demographics?")
        print("• What procedures were performed?")
        print("• What were the outcomes of the cases?")
        print("\n💡 Make sure you have added case reports using: python add_case_report.py")
        sys.exit(1)
    
    # Get question from command line arguments
    question = " ".join(sys.argv[1:])
    
    print(f"🏥 Multi-Case Medical Query")
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
    
    print(f"📋 Querying {len(existing_cases)} case report(s):")
    for case_name in existing_cases.keys():
        print(f"   • {case_name}")
    
    # Get answer
    answer = query_multiple_cases(question, existing_cases)
    print(f"\n💡 Answer: {answer}")

if __name__ == "__main__":
    main()
