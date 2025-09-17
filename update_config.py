#!/usr/bin/env python3
"""
Script to update case_reports_config.json with all 200 patient files
"""

import json
import os
from pathlib import Path

def generate_patient_config():
    """Generate configuration for all patient files in patient_txt_200 directory"""
    
    # Base directory for patient files
    patient_dir = Path("patient_txt_200")
    
    # Check if directory exists
    if not patient_dir.exists():
        print(f"Error: Directory {patient_dir} does not exist")
        return
    
    # Get all .txt files in the directory
    patient_files = sorted(patient_dir.glob("*.txt"))
    
    if not patient_files:
        print(f"No .txt files found in {patient_dir}")
        return
    
    print(f"Found {len(patient_files)} patient files")
    
    # Create configuration dictionary
    config = {}
    
    for file_path in patient_files:
        # Extract patient ID from filename (remove .txt extension)
        patient_id = file_path.stem
        
        # Create a readable name for the patient
        patient_name = f"Patient {patient_id}"
        
        # Add to configuration with relative path
        config[patient_name] = str(file_path)
    
    # Write to case_reports_config.json
    config_file = Path("case_reports_config.json")
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Updated {config_file} with {len(config)} patient entries")
    print("Sample entries:")
    for i, (name, path) in enumerate(list(config.items())[:5]):
        print(f"  {name}: {path}")
    if len(config) > 5:
        print(f"  ... and {len(config) - 5} more entries")

if __name__ == "__main__":
    generate_patient_config()

