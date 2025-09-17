#!/usr/bin/env python3
"""
MIMIC IV Patient Query System - Examples
Demonstrates various ways to query the MIMIC IV patient database
"""

from mimic_patient_query_system import MIMICQueryInterface
import json

def main():
    """Run example queries"""
    print("🏥 MIMIC IV Patient Query System - Examples")
    print("=" * 60)
    
    # Initialize the interface
    print("Loading patient data...")
    interface = MIMICQueryInterface()
    print(f"✅ Loaded {len(interface.indexer.patients)} patients")
    print()
    
    # Example 1: Basic search
    print("📋 Example 1: Basic Search")
    print("-" * 30)
    query = "coronary artery disease"
    results = interface.search(query, max_results=3)
    
    print(f"Query: '{query}'")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        print(f"     Service: {result.metadata.get('service', 'Unknown')}")
        print(f"     Chief Complaint: {result.metadata.get('chief_complaint', 'Unknown')}")
    print()
    
    # Example 2: Search specific patients
    print("📋 Example 2: Search Specific Patients")
    print("-" * 30)
    query = "diabetes"
    patient_ids = ["10019957", "10023771", "10026161"]
    results = interface.search(query, patient_ids=patient_ids, max_results=5)
    
    print(f"Query: '{query}' in patients {patient_ids}")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        if result.matched_keywords:
            print(f"     Keywords: {', '.join(result.matched_keywords[:3])}")
    print()
    
    # Example 3: Search by medical category
    print("📋 Example 3: Search by Medical Category")
    print("-" * 30)
    query = "chest pain"
    categories = ["symptoms", "diagnoses"]
    results = interface.search(query, categories=categories, max_results=3)
    
    print(f"Query: '{query}' in categories {categories}")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        print(f"     Context: {result.context[:100]}..." if result.context else "     No context available")
    print()
    
    # Example 4: Get detailed patient information
    print("📋 Example 4: Detailed Patient Information")
    print("-" * 30)
    patient_id = "10019957"
    info = interface.get_patient_info(patient_id)
    
    if info:
        print(f"Patient {patient_id} Information:")
        print(f"  Sex: {info['metadata'].get('sex', 'Unknown')}")
        print(f"  Service: {info['metadata'].get('service', 'Unknown')}")
        print(f"  Chief Complaint: {info['metadata'].get('chief_complaint', 'Unknown')}")
        
        if info['medical_conditions']:
            print(f"  Medical Conditions: {', '.join(info['medical_conditions'][:5])}")
        
        if info['procedures']:
            print(f"  Procedures: {', '.join(info['procedures'][:5])}")
        
        if info['medications']:
            print(f"  Medications: {', '.join(info['medications'][:5])}")
    else:
        print(f"Patient {patient_id} not found")
    print()
    
    # Example 5: Database statistics
    print("📋 Example 5: Database Statistics")
    print("-" * 30)
    stats = interface.get_database_stats()
    print(f"Total Patients: {stats['total_patients']}")
    print(f"Total Keywords: {stats['total_keywords']}")
    print(f"Total Medical Terms: {stats['total_medical_terms']}")
    
    print("\nTop Services:")
    for service, count in stats['services'].most_common(3):
        print(f"  {service}: {count}")
    
    print("\nTop Diagnoses:")
    for diagnosis, count in stats['common_diagnoses'].most_common(3):
        print(f"  {diagnosis}: {count}")
    
    print("\nTop Medications:")
    for medication, count in stats['common_medications'].most_common(3):
        print(f"  {medication}: {count}")
    print()
    
    # Example 6: Complex medical query
    print("📋 Example 6: Complex Medical Query")
    print("-" * 30)
    query = "aortic valve replacement CABG"
    results = interface.search(query, max_results=3)
    
    print(f"Query: '{query}'")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        print(f"     Service: {result.metadata.get('service', 'Unknown')}")
        if result.matched_sections:
            print(f"     Matched Section: {result.matched_sections[0][:150]}...")
    print()
    
    # Example 7: Medication search
    print("📋 Example 7: Medication Search")
    print("-" * 30)
    query = "aspirin warfarin"
    results = interface.search(query, max_results=3)
    
    print(f"Query: '{query}'")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        if result.matched_keywords:
            med_keywords = [kw for kw in result.matched_keywords if any(med in kw.lower() for med in ['aspirin', 'warfarin', 'asa', 'coumadin'])]
            if med_keywords:
                print(f"     Medication Keywords: {', '.join(med_keywords)}")
    print()
    
    # Example 8: Lab values search
    print("📋 Example 8: Lab Values Search")
    print("-" * 30)
    query = "hemoglobin creatinine"
    results = interface.search(query, max_results=3)
    
    print(f"Query: '{query}'")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        if result.context:
            # Look for lab values in context
            import re
            lab_values = re.findall(r'\b\d+\.?\d*\s*(mg|mcg|ml|cc|units?|g/dl|mg/dl)\b', result.context)
            if lab_values:
                print(f"     Lab Values Found: {', '.join(lab_values[:3])}")
    print()
    
    print("✅ Examples completed!")
    print("\nTo run interactive mode, use:")
    print("  python mimic_query_cli.py --interactive")
    print("\nTo start web interface, use:")
    print("  python mimic_web_interface.py")

if __name__ == "__main__":
    main()
