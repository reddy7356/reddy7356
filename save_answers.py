#!/usr/bin/env python3
"""
Save Medical Case Report Answers to File
Runs queries and saves all answers to a text file for easy reference
"""

import json
import os
from datetime import datetime
from multi_case_rag import query_multiple_cases

def save_answers_to_file():
    """Run queries and save answers to a file"""
    
    # Load configuration
    config_file = "case_reports_config.json"
    
    if not os.path.exists(config_file):
        print("❌ No case reports configured.")
        print("💡 Run 'python add_case_report.py' to add case reports first.")
        return
    
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
        return
    
    print(f"📋 Found {len(existing_cases)} case report(s):")
    for case_name in existing_cases.keys():
        print(f"   • {case_name}")
    
    # Define questions to ask
    questions = [
        "What are the patient ages in the case reports?",
        "What are the main diagnoses across the cases?",
        "What treatments were used in the cases?",
        "What complications occurred across the cases?",
        "What medications were used in the cases?",
        "What procedures were performed?",
        "What were the outcomes of the cases?",
        "What are the common comorbidities mentioned?",
        "What lab results or vital signs are documented?",
        "What are the key differences between the cases?"
    ]
    
    # Create output file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"medical_case_answers_{timestamp}.txt"
    
    print(f"\n🧪 Running queries and saving answers to: {output_file}")
    print("-" * 60)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write("MEDICAL CASE REPORT ANALYSIS\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Case reports analyzed: {len(existing_cases)}\n")
        f.write("\nCase Reports:\n")
        for case_name in existing_cases.keys():
            f.write(f"• {case_name}\n")
        f.write("\n" + "=" * 50 + "\n\n")
        
        # Run queries and save answers
        for i, question in enumerate(questions, 1):
            print(f"Processing question {i}/{len(questions)}: {question}")
            
            # Get answer
            answer = query_multiple_cases(question, existing_cases)
            
            # Write to file
            f.write(f"QUESTION {i}: {question}\n")
            f.write("-" * 40 + "\n")
            f.write(f"ANSWER: {answer}\n")
            f.write("\n" + "=" * 50 + "\n\n")
            
            print(f"✅ Saved answer for question {i}")
    
    print(f"\n🎉 All answers saved to: {output_file}")
    print(f"📁 File location: {os.path.abspath(output_file)}")
    
    # Also show a summary
    print(f"\n📊 Summary:")
    print(f"   • Questions processed: {len(questions)}")
    print(f"   • Case reports analyzed: {len(existing_cases)}")
    print(f"   • Output file: {output_file}")
    
    return output_file

def main():
    """Main function"""
    print("🏥 Medical Case Report Answer Saver")
    print("="*50)
    print("This script will run queries and save all answers to a file.")
    print("You can then review the answers at your convenience.\n")
    
    try:
        output_file = save_answers_to_file()
        if output_file:
            print(f"\n💡 To view your answers:")
            print(f"   • Open the file: {output_file}")
            print(f"   • Or use: open {output_file}")
            print(f"   • Or use: cat {output_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
