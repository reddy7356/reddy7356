#!/usr/bin/env python3
"""
Medical Knowledge Graph Runner
Easy script to run the medical knowledge graph system
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Main function to run the medical knowledge graph system"""
    print("🏥 Medical Knowledge Graph System Runner")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists(".venv"):
        print("❌ Virtual environment not found. Please run:")
        print("   python -m venv .venv")
        print("   source .venv/bin/activate")
        print("   pip install -r requirements.txt")
        return
    
    # Check if Neo4j is running
    print("🔍 Checking Neo4j database...")
    neo4j_running = run_command("docker ps | grep medical-neo4j", "Checking Neo4j container")
    
    if not neo4j_running:
        print("🚀 Starting Neo4j database...")
        start_neo4j = run_command(
            "docker run --name medical-neo4j -p 7474:7474 -p 7687:7687 -d --env NEO4J_AUTH=neo4j/medical123 neo4j:latest",
            "Starting Neo4j container"
        )
        if not start_neo4j:
            print("❌ Failed to start Neo4j. Please check Docker installation.")
            return
        
        print("⏳ Waiting for Neo4j to start...")
        import time
        time.sleep(10)
    
    # Test the system
    print("\n🧪 Testing Medical Knowledge Graph System...")
    
    # Test basic functionality
    test_cmd = "source .venv/bin/activate && python -c \"from medical_knowledge_graph import MedicalKnowledgeGraph; kg = MedicalKnowledgeGraph(); print('✅ System ready!' if kg.driver else '❌ Connection failed'); kg.close()\""
    if run_command(test_cmd, "Testing knowledge graph connection"):
        print("\n🎉 Medical Knowledge Graph System is ready!")
        print("\n📋 Available Commands:")
        print("  • Interactive Interface: source .venv/bin/activate && python kg_query_interface.py")
        print("  • RAG Integration: source .venv/bin/activate && python rag_knowledge_graph_integration.py")
        print("  • Search Keywords: source .venv/bin/activate && python kg_query_interface.py --command search --args heart")
        print("  • Get Relationships: source .venv/bin/activate && python kg_query_interface.py --command relationships --args 'chest pain'")
        print("  • RAG Query: source .venv/bin/activate && python kg_query_interface.py --command rag --args 'What heart conditions are mentioned?'")
        
        print("\n🌐 Neo4j Browser: http://localhost:7474")
        print("   Username: neo4j")
        print("   Password: medical123")
    else:
        print("❌ System test failed. Please check the setup.")

if __name__ == "__main__":
    main()
