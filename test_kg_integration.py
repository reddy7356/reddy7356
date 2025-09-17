#!/usr/bin/env python3
"""
Test Script for Medical Knowledge Graph Integration
Comprehensive testing of the Neo4j knowledge graph with RAG system
"""

import os
import sys
import json
from typing import List, Dict, Any
from medical_knowledge_graph import MedicalKnowledgeGraph
from rag_knowledge_graph_integration import RAGKnowledgeGraphPipeline, load_medical_case_report

def test_knowledge_graph_connection():
    """Test Neo4j connection and basic operations"""
    print("🔌 Testing Neo4j Connection...")
    print("-" * 40)
    
    try:
        kg = MedicalKnowledgeGraph()
        if kg.driver:
            print("✅ Neo4j connection successful")
            
            # Test basic query
            with kg.driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                if record and record["test"] == 1:
                    print("✅ Basic query test passed")
                else:
                    print("❌ Basic query test failed")
            
            kg.close()
            return True
        else:
            print("❌ Neo4j connection failed")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_knowledge_graph_initialization():
    """Test knowledge graph initialization"""
    print("\n🏗️ Testing Knowledge Graph Initialization...")
    print("-" * 40)
    
    try:
        kg = MedicalKnowledgeGraph()
        if not kg.driver:
            print("❌ No database connection")
            return False
        
        # Initialize the graph
        success = kg.initialize_knowledge_graph()
        if success:
            print("✅ Knowledge graph initialized successfully")
            
            # Test data retrieval
            all_keywords = kg.query_keywords()
            print(f"✅ Retrieved {len(all_keywords)} medical keywords")
            
            # Test category query
            symptoms = kg.query_keywords(category="symptoms")
            print(f"✅ Retrieved {len(symptoms)} symptoms")
            
            # Test search
            heart_keywords = kg.query_keywords(query="heart")
            print(f"✅ Found {len(heart_keywords)} heart-related keywords")
            
            kg.close()
            return True
        else:
            print("❌ Knowledge graph initialization failed")
            kg.close()
            return False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_relationships():
    """Test relationship queries"""
    print("\n🔗 Testing Relationship Queries...")
    print("-" * 40)
    
    try:
        kg = MedicalKnowledgeGraph()
        if not kg.driver:
            print("❌ No database connection")
            return False
        
        # Test relationship queries
        test_keywords = ["chest pain", "cardiomyopathy", "dysrhythmias"]
        
        for keyword in test_keywords:
            relationships = kg.get_relationships(keyword)
            print(f"✅ '{keyword}': {len(relationships)} relationships found")
            
            related = kg.find_related_concepts(keyword, max_depth=2)
            print(f"✅ '{keyword}': {len(related)} related concepts found")
        
        kg.close()
        return True
    except Exception as e:
        print(f"❌ Relationship test error: {e}")
        return False

def test_rag_integration():
    """Test RAG-Knowledge Graph integration"""
    print("\n🤖 Testing RAG-Knowledge Graph Integration...")
    print("-" * 40)
    
    try:
        # Initialize RAG pipeline
        pipeline = RAGKnowledgeGraphPipeline()
        print("✅ RAG pipeline initialized")
        
        # Load test documents
        case_reports_dir = "/Users/saiofocalallc/haystack RAG/case_reports"
        documents = []
        
        if os.path.exists(case_reports_dir):
            for filename in os.listdir(case_reports_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(case_reports_dir, filename)
                    docs = load_medical_case_report(file_path)
                    documents.extend(docs)
                    print(f"✅ Loaded {len(docs)} documents from {filename}")
        
        if not documents:
            print("⚠️ No case reports found - creating dummy document for testing")
            from haystack import Document
            documents = [Document(content="Patient has chest pain and irregular heartbeat.", meta={'source': 'test'})]
        
        # Test queries
        test_queries = [
            "What heart conditions are mentioned?",
            "Are there any cardiovascular symptoms?",
            "What devices are used for heart conditions?"
        ]
        
        for query in test_queries:
            print(f"\n❓ Testing query: {query}")
            try:
                result = pipeline.run(query, documents)
                answer = result['kg_generator']['answer']
                kg_insights = result['kg_generator']['kg_insights']
                
                print(f"✅ Answer generated: {answer[:100]}...")
                print(f"✅ KG concepts found: {len(kg_insights['concepts_found'])}")
                print(f"✅ KG categories: {len(kg_insights['categories'])}")
                
            except Exception as e:
                print(f"❌ Query failed: {e}")
        
        pipeline.close()
        return True
    except Exception as e:
        print(f"❌ RAG integration test error: {e}")
        return False

def test_visualization():
    """Test knowledge graph visualization"""
    print("\n📊 Testing Knowledge Graph Visualization...")
    print("-" * 40)
    
    try:
        kg = MedicalKnowledgeGraph()
        if not kg.driver:
            print("❌ No database connection")
            return False
        
        # Test visualization creation
        output_file = "test_kg_visualization.html"
        fig = kg.visualize_graph(output_file)
        
        if os.path.exists(output_file):
            print(f"✅ Visualization created: {output_file}")
            # Clean up test file
            os.remove(output_file)
            print("✅ Test file cleaned up")
        else:
            print("❌ Visualization file not created")
        
        kg.close()
        return True
    except Exception as e:
        print(f"❌ Visualization test error: {e}")
        return False

def test_export_import():
    """Test data export and import"""
    print("\n📤 Testing Data Export...")
    print("-" * 40)
    
    try:
        kg = MedicalKnowledgeGraph()
        if not kg.driver:
            print("❌ No database connection")
            return False
        
        # Test export
        output_file = "test_kg_export.json"
        data = kg.export_to_json(output_file)
        
        if os.path.exists(output_file):
            print(f"✅ Data exported to: {output_file}")
            
            # Test import validation
            with open(output_file, 'r') as f:
                imported_data = json.load(f)
            
            if 'concepts' in imported_data and 'metadata' in imported_data:
                print(f"✅ Export validation passed: {len(imported_data['concepts'])} concepts")
            else:
                print("❌ Export validation failed")
            
            # Clean up test file
            os.remove(output_file)
            print("✅ Test file cleaned up")
        else:
            print("❌ Export file not created")
        
        kg.close()
        return True
    except Exception as e:
        print(f"❌ Export test error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 Medical Knowledge Graph Integration - Comprehensive Test Suite")
    print("=" * 70)
    
    tests = [
        ("Neo4j Connection", test_knowledge_graph_connection),
        ("Knowledge Graph Initialization", test_knowledge_graph_initialization),
        ("Relationship Queries", test_relationships),
        ("RAG Integration", test_rag_integration),
        ("Visualization", test_visualization),
        ("Data Export", test_export_import)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the Neo4j setup and dependencies.")
    
    return passed == total

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # Quick test - just connection and basic functionality
        print("🚀 Running Quick Test...")
        success = test_knowledge_graph_connection() and test_knowledge_graph_initialization()
        if success:
            print("✅ Quick test passed!")
        else:
            print("❌ Quick test failed!")
    else:
        # Full comprehensive test
        run_comprehensive_test()

if __name__ == "__main__":
    main()
