#!/usr/bin/env python3
"""
Test Patient Data with Knowledge Graph
Analyzes the first 20 patients from patient_txt_200 directory using the medical knowledge graph
"""

import os
import json
from typing import List, Dict, Any
from medical_knowledge_graph import MedicalKnowledgeGraph
from rag_knowledge_graph_integration import RAGKnowledgeGraphPipeline, load_medical_case_report
from haystack import Document

def get_first_20_patients() -> List[str]:
    """Get the first 20 patient files from patient_txt_200 directory"""
    patient_dir = "/Users/saiofocalallc/haystack RAG/patient_txt_200"
    all_files = sorted(os.listdir(patient_dir))
    return all_files[:20]

def load_patient_documents(patient_files: List[str]) -> List[Document]:
    """Load patient documents and convert to Haystack documents"""
    patient_dir = "/Users/saiofocalallc/haystack RAG/patient_txt_200"
    documents = []
    
    for i, filename in enumerate(patient_files):
        file_path = os.path.join(patient_dir, filename)
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                    
                    # Create document
                    doc = Document(
                        content=content,
                        meta={
                            'patient_id': filename.replace('.txt', ''),
                            'source': 'patient_data',
                            'file_path': file_path
                        }
                    )
                    documents.append(doc)
                    print(f"✅ Loaded patient {i+1}/20: {filename} (encoding: {encoding})")
                    break
                    
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"❌ Error loading {filename} with {encoding}: {e}")
                    continue
            else:
                print(f"❌ Failed to load {filename} with any encoding")
                
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    return documents

def test_medical_keywords_in_patients(kg: MedicalKnowledgeGraph, documents: List[Document]) -> Dict[str, Any]:
    """Test which medical keywords appear in the patient data"""
    print("\n🔍 Testing Medical Keywords in Patient Data...")
    print("=" * 60)
    
    # Get all medical keywords from knowledge graph
    all_keywords = kg.query_keywords()
    keyword_names = [kw['name'] for kw in all_keywords]
    
    results = {
        'total_patients': len(documents),
        'total_keywords': len(keyword_names),
        'keyword_matches': {},
        'patient_keywords': {},
        'category_analysis': {}
    }
    
    # Initialize category analysis
    categories = ['cardiovascular_conditions', 'symptoms', 'acute_events', 'risk_factors', 'complications', 'devices']
    for category in categories:
        results['category_analysis'][category] = {
            'total_matches': 0,
            'patients_with_matches': 0,
            'keywords_found': []
        }
    
    # Test each keyword
    for keyword in keyword_names:
        results['keyword_matches'][keyword] = {
            'total_matches': 0,
            'patients_with_matches': [],
            'match_count': 0
        }
    
    # Analyze each patient document
    for i, doc in enumerate(documents):
        patient_id = doc.meta['patient_id']
        content_lower = doc.content.lower()
        
        results['patient_keywords'][patient_id] = {
            'keywords_found': [],
            'total_matches': 0
        }
        
        # Check for each keyword
        for keyword in keyword_names:
            keyword_lower = keyword.lower()
            if keyword_lower in content_lower:
                # Count occurrences
                match_count = content_lower.count(keyword_lower)
                
                # Update keyword results
                results['keyword_matches'][keyword]['total_matches'] += match_count
                results['keyword_matches'][keyword]['patients_with_matches'].append(patient_id)
                results['keyword_matches'][keyword]['match_count'] += match_count
                
                # Update patient results
                results['patient_keywords'][patient_id]['keywords_found'].append({
                    'keyword': keyword,
                    'count': match_count
                })
                results['patient_keywords'][patient_id]['total_matches'] += match_count
        
        # Get category information for found keywords
        for keyword_match in results['patient_keywords'][patient_id]['keywords_found']:
            keyword_name = keyword_match['keyword']
            keyword_info = kg.query_keywords(query=keyword_name)
            if keyword_info and keyword_info[0]['category']:
                category = keyword_info[0]['category']
                if category in results['category_analysis']:
                    results['category_analysis'][category]['total_matches'] += keyword_match['count']
                    if keyword_name not in results['category_analysis'][category]['keywords_found']:
                        results['category_analysis'][category]['keywords_found'].append(keyword_name)
    
    # Count patients with matches for each category
    for category in categories:
        patients_with_matches = set()
        for patient_id, patient_data in results['patient_keywords'].items():
            for keyword_match in patient_data['keywords_found']:
                keyword_name = keyword_match['keyword']
                keyword_info = kg.query_keywords(query=keyword_name)
                if keyword_info and keyword_info[0]['category'] == category:
                    patients_with_matches.add(patient_id)
        results['category_analysis'][category]['patients_with_matches'] = len(patients_with_matches)
    
    return results

def test_rag_queries_with_patients(pipeline: RAGKnowledgeGraphPipeline, documents: List[Document]) -> Dict[str, Any]:
    """Test RAG queries with patient data"""
    print("\n🤖 Testing RAG Queries with Patient Data...")
    print("=" * 60)
    
    test_queries = [
        "What heart conditions are mentioned?",
        "Are there any cardiovascular symptoms?",
        "What devices are used for heart conditions?",
        "What are the symptoms related to heart disease?",
        "Tell me about chest pain and related conditions",
        "What risk factors are present?",
        "Are there any complications mentioned?"
    ]
    
    results = {
        'queries_tested': len(test_queries),
        'query_results': {}
    }
    
    for query in test_queries:
        print(f"\n❓ Testing Query: {query}")
        try:
            result = pipeline.run(query, documents)
            
            results['query_results'][query] = {
                'answer': result['kg_generator']['answer'],
                'kg_insights': result['kg_generator']['kg_insights'],
                'success': True
            }
            
            print(f"✅ Query successful")
            print(f"💡 Answer: {result['kg_generator']['answer'][:100]}...")
            
            # Display KG insights
            kg_insights = result['kg_generator']['kg_insights']
            if kg_insights['concepts_found']:
                print(f"🔍 KG Concepts: {', '.join(kg_insights['concepts_found'])}")
            if kg_insights['categories']:
                print(f"📁 KG Categories: {', '.join(kg_insights['categories'])}")
                
        except Exception as e:
            print(f"❌ Query failed: {e}")
            results['query_results'][query] = {
                'error': str(e),
                'success': False
            }
    
    return results

def print_summary_report(keyword_results: Dict[str, Any], rag_results: Dict[str, Any]):
    """Print a comprehensive summary report"""
    print("\n" + "="*80)
    print("📊 PATIENT DATA ANALYSIS SUMMARY REPORT")
    print("="*80)
    
    # Keyword Analysis Summary
    print(f"\n🔍 KEYWORD ANALYSIS:")
    print(f"   • Total Patients Analyzed: {keyword_results['total_patients']}")
    print(f"   • Total Medical Keywords: {keyword_results['total_keywords']}")
    
    # Top keywords found
    keyword_matches = keyword_results['keyword_matches']
    top_keywords = sorted(keyword_matches.items(), key=lambda x: x[1]['total_matches'], reverse=True)[:10]
    
    print(f"\n📈 TOP 10 KEYWORDS FOUND:")
    for keyword, data in top_keywords:
        if data['total_matches'] > 0:
            print(f"   • {keyword}: {data['total_matches']} matches in {len(data['patients_with_matches'])} patients")
    
    # Category Analysis
    print(f"\n📁 CATEGORY ANALYSIS:")
    for category, data in keyword_results['category_analysis'].items():
        if data['total_matches'] > 0:
            print(f"   • {category.replace('_', ' ').title()}: {data['total_matches']} matches in {data['patients_with_matches']} patients")
            print(f"     Keywords found: {', '.join(data['keywords_found'][:3])}{'...' if len(data['keywords_found']) > 3 else ''}")
    
    # Patient Analysis
    patients_with_keywords = sum(1 for p in keyword_results['patient_keywords'].values() if p['total_matches'] > 0)
    print(f"\n👥 PATIENT ANALYSIS:")
    print(f"   • Patients with medical keywords: {patients_with_keywords}/{keyword_results['total_patients']}")
    print(f"   • Coverage: {(patients_with_keywords/keyword_results['total_patients']*100):.1f}%")
    
    # RAG Analysis
    print(f"\n🤖 RAG QUERY ANALYSIS:")
    successful_queries = sum(1 for q in rag_results['query_results'].values() if q['success'])
    print(f"   • Successful queries: {successful_queries}/{rag_results['queries_tested']}")
    print(f"   • Success rate: {(successful_queries/rag_results['queries_tested']*100):.1f}%")
    
    print(f"\n✅ Analysis complete! Check the detailed results above.")

def main():
    """Main function to test patient data with knowledge graph"""
    print("🏥 Testing Patient Data with Medical Knowledge Graph")
    print("=" * 60)
    
    # Initialize knowledge graph
    print("🔌 Initializing Knowledge Graph...")
    kg = MedicalKnowledgeGraph()
    if not kg.driver:
        print("❌ Failed to connect to Neo4j database")
        return
    
    # Initialize RAG pipeline
    print("🤖 Initializing RAG Pipeline...")
    try:
        pipeline = RAGKnowledgeGraphPipeline()
        print("✅ RAG pipeline initialized")
    except Exception as e:
        print(f"❌ Failed to initialize RAG pipeline: {e}")
        return
    
    # Get first 20 patients
    print("\n📁 Loading Patient Data...")
    patient_files = get_first_20_patients()
    print(f"Found {len(patient_files)} patient files")
    
    # Load patient documents
    documents = load_patient_documents(patient_files)
    print(f"✅ Loaded {len(documents)} patient documents")
    
    if not documents:
        print("❌ No patient documents loaded. Exiting.")
        return
    
    # Test medical keywords
    keyword_results = test_medical_keywords_in_patients(kg, documents)
    
    # Test RAG queries
    rag_results = test_rag_queries_with_patients(pipeline, documents)
    
    # Print summary report
    print_summary_report(keyword_results, rag_results)
    
    # Save results to file
    results_file = "patient_data_analysis_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'keyword_analysis': keyword_results,
            'rag_analysis': rag_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    # Cleanup
    pipeline.close()
    kg.close()
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
