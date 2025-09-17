#!/usr/bin/env python3
"""
MIMIC IV Patient Query CLI
Simple command-line interface for querying MIMIC IV patients
"""

import sys
import argparse
from mimic_patient_query_system import MIMICQueryInterface

def main():
    parser = argparse.ArgumentParser(description='Query MIMIC IV patient data')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--patients', '-p', help='Comma-separated patient IDs to search')
    parser.add_argument('--categories', '-c', help='Comma-separated medical categories')
    parser.add_argument('--max-results', '-m', type=int, default=10, help='Maximum results to return')
    parser.add_argument('--interactive', '-i', action='store_true', help='Start interactive mode')
    parser.add_argument('--stats', '-s', action='store_true', help='Show database statistics')
    parser.add_argument('--list-patients', '-l', type=int, help='List patients (with optional limit)')
    parser.add_argument('--patient-info', help='Show detailed info for specific patient')
    
    args = parser.parse_args()
    
    try:
        interface = MIMICQueryInterface()
        
        if args.stats:
            show_stats(interface)
        elif args.list_patients is not None:
            show_patient_list(interface, args.list_patients)
        elif args.patient_info:
            show_patient_info(interface, args.patient_info)
        elif args.interactive:
            interface.interactive_search()
        elif args.query:
            perform_search(interface, args)
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def show_stats(interface):
    """Show database statistics"""
    stats = interface.get_database_stats()
    print(f"📊 MIMIC IV Database Statistics")
    print(f"=" * 40)
    print(f"Total Patients: {stats['total_patients']}")
    print(f"Total Keywords: {stats['total_keywords']}")
    print(f"Total Medical Terms: {stats['total_medical_terms']}")
    
    print(f"\n🏥 Top Services:")
    for service, count in stats['services'].most_common(5):
        print(f"  {service}: {count}")
    
    print(f"\n🩺 Top Diagnoses:")
    for diagnosis, count in stats['common_diagnoses'].most_common(5):
        print(f"  {diagnosis}: {count}")
    
    print(f"\n💊 Top Medications:")
    for medication, count in stats['common_medications'].most_common(5):
        print(f"  {medication}: {count}")

def show_patient_list(interface, limit):
    """Show list of patients"""
    patients = interface.list_patients(limit)
    print(f"👥 Patient List (showing {len(patients)} of {interface.get_database_stats()['total_patients']}):")
    for i, patient_id in enumerate(patients, 1):
        print(f"  {i:3d}. {patient_id}")

def show_patient_info(interface, patient_id):
    """Show detailed patient information"""
    info = interface.get_patient_info(patient_id)
    
    if not info:
        print(f"Patient {patient_id} not found.")
        return
    
    print(f"👤 Patient {patient_id} Information:")
    print(f"=" * 40)
    print(f"Sex: {info['metadata'].get('sex', 'Unknown')}")
    print(f"Service: {info['metadata'].get('service', 'Unknown')}")
    print(f"Chief Complaint: {info['metadata'].get('chief_complaint', 'Unknown')}")
    
    if info['medical_conditions']:
        print(f"\n🩺 Medical Conditions:")
        for condition in info['medical_conditions'][:10]:
            print(f"  • {condition}")
    
    if info['procedures']:
        print(f"\n🔧 Procedures:")
        for procedure in info['procedures'][:10]:
            print(f"  • {procedure}")
    
    if info['medications']:
        print(f"\n💊 Medications:")
        for medication in info['medications'][:10]:
            print(f"  • {medication}")
    
    if info['metadata'].get('allergies'):
        print(f"\n⚠️  Allergies:")
        for allergy in info['metadata']['allergies']:
            print(f"  • {allergy}")
    
    print(f"\n📄 Content Length: {info['content_length']} characters")

def perform_search(interface, args):
    """Perform search and display results"""
    patient_ids = None
    if args.patients:
        patient_ids = [pid.strip() for pid in args.patients.split(',')]
    
    categories = None
    if args.categories:
        categories = [cat.strip() for cat in args.categories.split(',')]
    
    results = interface.search(args.query, patient_ids, categories, args.max_results)
    
    if not results:
        print(f"No results found for query: '{args.query}'")
        return
    
    print(f"🔍 Search Results for '{args.query}' ({len(results)} results):")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
        print(f"   Service: {result.metadata.get('service', 'Unknown')}")
        print(f"   Chief Complaint: {result.metadata.get('chief_complaint', 'Unknown')}")
        
        if result.matched_keywords:
            print(f"   Keywords: {', '.join(result.matched_keywords[:5])}")
        
        if result.context:
            context = result.context[:300] + "..." if len(result.context) > 300 else result.context
            print(f"   Context: {context}")

if __name__ == "__main__":
    main()
