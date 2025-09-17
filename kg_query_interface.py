#!/usr/bin/env python3
"""
Knowledge Graph Query Interface
Interactive command-line interface for querying the medical knowledge graph
"""

import os
import json
import argparse
from typing import List, Dict, Any, Optional
from medical_knowledge_graph import MedicalKnowledgeGraph
from rag_knowledge_graph_integration import RAGKnowledgeGraphPipeline, load_medical_case_report

class KnowledgeGraphQueryInterface:
    """Interactive interface for querying the medical knowledge graph"""
    
    def __init__(self, kg_uri: str = "bolt://localhost:7687", kg_user: str = "neo4j", kg_password: str = "medical123"):
        """
        Initialize the query interface
        
        Args:
            kg_uri: Neo4j database URI
            kg_user: Neo4j username
            kg_password: Neo4j password
        """
        self.kg = MedicalKnowledgeGraph(kg_uri, kg_user, kg_password)
        self.rag_pipeline = None
        
        # Available commands
        self.commands = {
            'search': self._search_keywords,
            'category': self._search_by_category,
            'relationships': self._get_relationships,
            'related': self._get_related_concepts,
            'visualize': self._visualize_graph,
            'export': self._export_data,
            'rag': self._rag_query,
            'help': self._show_help,
            'quit': self._quit_interface
        }
    
    def _search_keywords(self, args: List[str]) -> None:
        """Search for keywords in the knowledge graph"""
        if not args:
            print("❌ Please provide a search term")
            return
        
        query = ' '.join(args)
        results = self.kg.query_keywords(query=query)
        
        if results:
            print(f"🔍 Search results for '{query}':")
            print("-" * 50)
            for result in results:
                category = result['category'] or 'uncategorized'
                print(f"• {result['name']} (Category: {category})")
        else:
            print(f"❌ No results found for '{query}'")
    
    def _search_by_category(self, args: List[str]) -> None:
        """Search keywords by category"""
        if not args:
            print("❌ Please provide a category name")
            print("Available categories:")
            for category in self.kg.medical_ontology.keys():
                print(f"  • {category}")
            return
        
        category = args[0]
        results = self.kg.query_keywords(category=category)
        
        if results:
            print(f"📁 Keywords in category '{category}':")
            print("-" * 50)
            for result in results:
                print(f"• {result['name']}")
        else:
            print(f"❌ No keywords found in category '{category}'")
            print("Available categories:")
            for cat in self.kg.medical_ontology.keys():
                print(f"  • {cat}")
    
    def _get_relationships(self, args: List[str]) -> None:
        """Get relationships for a specific keyword"""
        if not args:
            print("❌ Please provide a keyword")
            return
        
        keyword = ' '.join(args)
        relationships = self.kg.get_relationships(keyword)
        
        if relationships:
            print(f"🔗 Relationships for '{keyword}':")
            print("-" * 50)
            for rel in relationships:
                direction_symbol = "→" if rel['direction'] == 'outgoing' else "←"
                print(f"• {rel['type']} {direction_symbol} {rel['related_concept']}")
        else:
            print(f"❌ No relationships found for '{keyword}'")
    
    def _get_related_concepts(self, args: List[str]) -> None:
        """Get related concepts for a keyword"""
        if not args:
            print("❌ Please provide a keyword")
            return
        
        keyword = ' '.join(args)
        max_depth = 2
        if len(args) > 1 and args[-1].isdigit():
            max_depth = int(args[-1])
        
        related = self.kg.find_related_concepts(keyword, max_depth=max_depth)
        
        if related:
            print(f"🌐 Related concepts for '{keyword}' (max depth: {max_depth}):")
            print("-" * 50)
            for concept in related:
                print(f"• {concept['concept']} (depth: {concept['depth']})")
        else:
            print(f"❌ No related concepts found for '{keyword}'")
    
    def _visualize_graph(self, args: List[str]) -> None:
        """Create a visualization of the knowledge graph"""
        output_file = "medical_knowledge_graph.html"
        if args:
            output_file = args[0]
        
        try:
            fig = self.kg.visualize_graph(output_file)
            print(f"✅ Knowledge graph visualization created: {output_file}")
            print("💡 Open the HTML file in your browser to view the interactive graph")
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
    
    def _export_data(self, args: List[str]) -> None:
        """Export knowledge graph data to JSON"""
        output_file = "medical_knowledge_graph.json"
        if args:
            output_file = args[0]
        
        try:
            data = self.kg.export_to_json(output_file)
            print(f"✅ Knowledge graph data exported to: {output_file}")
            print(f"📊 Exported {len(data['concepts'])} concepts")
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def _rag_query(self, args: List[str]) -> None:
        """Run a RAG query with knowledge graph integration"""
        if not args:
            print("❌ Please provide a query")
            return
        
        query = ' '.join(args)
        
        # Initialize RAG pipeline if not already done
        if not self.rag_pipeline:
            try:
                self.rag_pipeline = RAGKnowledgeGraphPipeline()
                print("✅ RAG pipeline initialized")
            except Exception as e:
                print(f"❌ Failed to initialize RAG pipeline: {e}")
                return
        
        # Load case reports
        case_reports_dir = "/Users/saiofocalallc/haystack RAG/case_reports"
        documents = []
        
        if os.path.exists(case_reports_dir):
            for filename in os.listdir(case_reports_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(case_reports_dir, filename)
                    docs = load_medical_case_report(file_path)
                    documents.extend(docs)
        
        if not documents:
            print("❌ No case reports found to query")
            return
        
        try:
            result = self.rag_pipeline.run(query, documents)
            
            print(f"❓ Query: {query}")
            print(f"💡 Answer: {result['kg_generator']['answer']}")
            
            # Display KG insights
            kg_insights = result['kg_generator']['kg_insights']
            if kg_insights['concepts_found']:
                print(f"🔍 KG Concepts: {', '.join(kg_insights['concepts_found'])}")
            if kg_insights['categories']:
                print(f"📁 KG Categories: {', '.join(kg_insights['categories'])}")
                
        except Exception as e:
            print(f"❌ Error running RAG query: {e}")
    
    def _show_help(self, args: List[str]) -> None:
        """Show help information"""
        print("🏥 Medical Knowledge Graph Query Interface")
        print("=" * 50)
        print("Available commands:")
        print("  search <term>           - Search for keywords containing the term")
        print("  category <name>         - Show all keywords in a category")
        print("  relationships <keyword> - Show relationships for a keyword")
        print("  related <keyword> [depth] - Show related concepts (default depth: 2)")
        print("  visualize [filename]    - Create knowledge graph visualization")
        print("  export [filename]       - Export data to JSON")
        print("  rag <query>             - Run RAG query with KG integration")
        print("  help                    - Show this help message")
        print("  quit                    - Exit the interface")
        print("\nExamples:")
        print("  search heart")
        print("  category symptoms")
        print("  relationships chest pain")
        print("  related cardiomyopathy 3")
        print("  rag What heart conditions are mentioned?")
    
    def _quit_interface(self, args: List[str]) -> None:
        """Quit the interface"""
        print("👋 Goodbye!")
        if self.rag_pipeline:
            self.rag_pipeline.close()
        self.kg.close()
        exit(0)
    
    def run_interactive(self):
        """Run the interactive interface"""
        print("🏥 Medical Knowledge Graph Query Interface")
        print("=" * 50)
        print("Type 'help' for available commands or 'quit' to exit")
        
        while True:
            try:
                user_input = input("\nkg> ").strip()
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Cleanup
        if self.rag_pipeline:
            self.rag_pipeline.close()
        self.kg.close()

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Medical Knowledge Graph Query Interface")
    parser.add_argument("--uri", default="bolt://localhost:7687", help="Neo4j database URI")
    parser.add_argument("--user", default="neo4j", help="Neo4j username")
    parser.add_argument("--password", default="medical123", help="Neo4j password")
    parser.add_argument("--command", help="Command to execute (non-interactive mode)")
    parser.add_argument("--args", nargs="*", help="Arguments for the command")
    
    args = parser.parse_args()
    
    # Initialize interface
    interface = KnowledgeGraphQueryInterface(args.uri, args.user, args.password)
    
    if not interface.kg.driver:
        print("❌ Cannot connect to Neo4j database")
        print("💡 Make sure Neo4j is running and credentials are correct")
        return
    
    # Check if knowledge graph is initialized
    try:
        # Try to query the graph
        test_results = interface.kg.query_keywords()
        if not test_results:
            print("🏗️ Knowledge graph appears to be empty. Initializing...")
            interface.kg.initialize_knowledge_graph()
    except Exception as e:
        print(f"❌ Error checking knowledge graph: {e}")
        return
    
    if args.command:
        # Non-interactive mode
        if args.command in interface.commands:
            interface.commands[args.command](args.args or [])
        else:
            print(f"❌ Unknown command: {args.command}")
            interface._show_help([])
    else:
        # Interactive mode
        interface.run_interactive()

if __name__ == "__main__":
    main()
