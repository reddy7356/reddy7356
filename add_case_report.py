#!/usr/bin/env python3
"""
Add Case Report Helper Script
Makes it easy to add new medical case reports to the RAG system
"""

import os
import shutil
import json
from pathlib import Path

def create_case_reports_directory():
    """Create a directory to store case reports"""
    case_reports_dir = Path("case_reports")
    case_reports_dir.mkdir(exist_ok=True)
    return case_reports_dir

def copy_case_report_to_directory(source_path: str, case_name: str = None):
    """Copy a case report to the case_reports directory"""
    if not os.path.exists(source_path):
        print(f"❌ Error: Source file not found: {source_path}")
        return None
    
    case_reports_dir = create_case_reports_directory()
    
    if case_name is None:
        case_name = Path(source_path).stem
    
    # Create a safe filename
    safe_filename = case_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    destination_path = case_reports_dir / f"{safe_filename}.txt"
    
    try:
        shutil.copy2(source_path, destination_path)
        print(f"✅ Copied case report to: {destination_path}")
        return str(destination_path)
    except Exception as e:
        print(f"❌ Error copying file: {e}")
        return None

def update_config_file(case_name: str, file_path: str):
    """Update the configuration file with new case report"""
    config_file = "case_reports_config.json"
    
    # Load existing config or create new one
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Add new case report
    config[case_name] = file_path
    
    # Save updated config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Updated configuration file: {config_file}")

def list_existing_case_reports():
    """List all existing case reports in the system"""
    config_file = "case_reports_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("\n📋 Existing case reports in the system:")
        for case_name, file_path in config.items():
            if os.path.exists(file_path):
                print(f"   ✅ {case_name}: {file_path}")
            else:
                print(f"   ❌ {case_name}: {file_path} (file not found)")
    else:
        print("\n📋 No case reports configured yet.")

def main():
    """Main function to add case reports"""
    print("🏥 Add Medical Case Report to RAG System")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Add a new case report")
        print("2. List existing case reports")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n📝 Adding new case report...")
            
            # Get source file path
            source_path = input("Enter the path to your case report file: ").strip()
            
            if not source_path:
                print("❌ No file path provided.")
                continue
            
            # Get case name
            case_name = input("Enter a name for this case report (or press Enter to use filename): ").strip()
            
            if not case_name:
                case_name = Path(source_path).stem
            
            # Copy file to case_reports directory
            destination_path = copy_case_report_to_directory(source_path, case_name)
            
            if destination_path:
                # Update configuration
                update_config_file(case_name, destination_path)
                print(f"✅ Successfully added case report: {case_name}")
            else:
                print("❌ Failed to add case report.")
        
        elif choice == "2":
            list_existing_case_reports()
        
        elif choice == "3":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
