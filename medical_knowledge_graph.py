#!/usr/bin/env python3
"""
Medical Knowledge Graph System using Neo4j
Creates and manages a knowledge graph of medical keywords and their relationships
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class MedicalKnowledgeGraph:
    """Medical Knowledge Graph using Neo4j for storing and querying medical keywords"""
    
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "medical123"):
        """
        Initialize the Medical Knowledge Graph
        
        Args:
            uri: Neo4j database URI
            user: Neo4j username
            password: Neo4j password
        """
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self.connect()
        
        # Medical keywords provided by user
        self.medical_keywords = [
            'significant acquired or congenital heart disease',
            'chest pain',
            'coronary heart disease',
            'angina',
            'myocardial infarction within 6 months',
            'irregular heart beat',
            'dysrhythmias',
            'syncope',
            'cardiomyopathy',
            'uncontrolled hypertension',
            'current heart murmur',
            'rheumatic fever',
            'moderate to severe valvular disease',
            'cerebrovascular and peripheral vascular disease',
            'congestive heart failure',
            'pacemaker',
            'defibrillator'
        ]
        
        # Medical keyword categories and relationships
        self.medical_ontology = {
            'cardiovascular_conditions': [
                'significant acquired or congenital heart disease',
                'coronary heart disease',
                'cardiomyopathy',
                'congestive heart failure',
                'moderate to severe valvular disease'
            ],
            'symptoms': [
                'chest pain',
                'angina',
                'irregular heart beat',
                'syncope',
                'current heart murmur'
            ],
            'acute_events': [
                'myocardial infarction within 6 months',
                'dysrhythmias'
            ],
            'risk_factors': [
                'uncontrolled hypertension',
                'rheumatic fever'
            ],
            'complications': [
                'cerebrovascular and peripheral vascular disease'
            ],
            'devices': [
                'pacemaker',
                'defibrillator'
            ]
        }
        
        # Relationships between medical concepts
        self.relationships = {
            'CAUSES': [
                ('coronary heart disease', 'chest pain'),
                ('coronary heart disease', 'angina'),
                ('cardiomyopathy', 'irregular heart beat'),
                ('uncontrolled hypertension', 'cardiomyopathy'),
                ('rheumatic fever', 'moderate to severe valvular disease')
            ],
            'LEADS_TO': [
                ('myocardial infarction within 6 months', 'cardiomyopathy'),
                ('dysrhythmias', 'syncope'),
                ('congestive heart failure', 'cerebrovascular and peripheral vascular disease')
            ],
            'TREATED_BY': [
                ('dysrhythmias', 'pacemaker'),
                ('dysrhythmias', 'defibrillator'),
                ('cardiomyopathy', 'defibrillator')
            ],
            'ASSOCIATED_WITH': [
                ('significant acquired or congenital heart disease', 'coronary heart disease'),
                ('chest pain', 'angina'),
                ('irregular heart beat', 'dysrhythmias')
            ]
        }
    
    def connect(self):
        """Connect to Neo4j database"""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            print("✅ Connected to Neo4j database successfully")
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            print("💡 Make sure Neo4j is running and credentials are correct")
            self.driver = None
    
    def close(self):
        """Close the database connection"""
        if self.driver:
            self.driver.close()
    
    def create_constraints(self):
        """Create database constraints for better performance"""
        constraints = [
            "CREATE CONSTRAINT medical_concept_name IF NOT EXISTS FOR (c:MedicalConcept) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT category_name IF NOT EXISTS FOR (cat:Category) REQUIRE cat.name IS UNIQUE"
        ]
        
        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"✅ Created constraint: {constraint.split('IF NOT EXISTS')[0].strip()}")
                except Exception as e:
                    print(f"⚠️ Constraint may already exist: {e}")
    
    def initialize_knowledge_graph(self):
        """Initialize the medical knowledge graph with keywords and relationships"""
        if not self.driver:
            print("❌ No database connection available")
            return False
        
        print("🏗️ Initializing Medical Knowledge Graph...")
        
        # Create constraints
        self.create_constraints()
        
        with self.driver.session() as session:
            # Clear existing data
            session.run("MATCH (n) DETACH DELETE n")
            print("🧹 Cleared existing data")
            
            # Create categories
            for category, keywords in self.medical_ontology.items():
                session.run(
                    "CREATE (c:Category {name: $name, description: $description})",
                    {"name": category, "description": f"Medical category for {category.replace('_', ' ')}"}
                )
                print(f"📁 Created category: {category}")
            
            # Create medical concepts
            for keyword in self.medical_keywords:
                session.run(
                    "CREATE (mc:MedicalConcept {name: $name, type: 'keyword'})",
                    {"name": keyword}
                )
                print(f"🏷️ Created medical concept: {keyword}")
            
            # Create category relationships
            for category, keywords in self.medical_ontology.items():
                for keyword in keywords:
                    session.run(
                        """
                        MATCH (c:Category {name: $category})
                        MATCH (mc:MedicalConcept {name: $keyword})
                        CREATE (mc)-[:BELONGS_TO]->(c)
                        """,
                        {"category": category, "keyword": keyword}
                    )
            
            # Create concept relationships
            for relationship_type, pairs in self.relationships.items():
                for source, target in pairs:
                    session.run(
                        """
                        MATCH (source:MedicalConcept {name: $source})
                        MATCH (target:MedicalConcept {name: $target})
                        CREATE (source)-[:%s]->(target)
                        """ % relationship_type,
                        {"source": source, "target": target}
                    )
                    print(f"🔗 Created relationship: {source} -[{relationship_type}]-> {target}")
        
        print("✅ Medical Knowledge Graph initialized successfully!")
        return True
    
    def query_keywords(self, query: str = None, category: str = None) -> List[Dict]:
        """
        Query medical keywords from the knowledge graph
        
        Args:
            query: Search query for keyword names
            category: Filter by category
            
        Returns:
            List of matching medical concepts
        """
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            if query is not None and query != "":
                # Search for keywords containing the query
                result = session.run(
                    """
                    MATCH (mc:MedicalConcept)
                    WHERE toLower(mc.name) CONTAINS toLower($query)
                    OPTIONAL MATCH (mc)-[:BELONGS_TO]->(c:Category)
                    RETURN mc.name as name, c.name as category
                    ORDER BY mc.name
                    """,
                    {"query": query}
                )
            elif category:
                # Get all keywords in a specific category
                result = session.run(
                    """
                    MATCH (mc:MedicalConcept)-[:BELONGS_TO]->(c:Category {name: $category})
                    RETURN mc.name as name, c.name as category
                    ORDER BY mc.name
                    """,
                    {"category": category}
                )
            else:
                # Get all keywords
                result = session.run(
                    """
                    MATCH (mc:MedicalConcept)
                    OPTIONAL MATCH (mc)-[:BELONGS_TO]->(c:Category)
                    RETURN mc.name as name, c.name as category
                    ORDER BY mc.name
                    """
                )
            
            return [{"name": record["name"], "category": record["category"]} for record in result]
    
    def get_relationships(self, keyword: str) -> List[Dict]:
        """
        Get all relationships for a specific medical keyword
        
        Args:
            keyword: The medical keyword to get relationships for
            
        Returns:
            List of relationships
        """
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (mc:MedicalConcept {name: $keyword})-[r]->(target:MedicalConcept)
                RETURN type(r) as relationship_type, target.name as related_concept, 'outgoing' as direction
                UNION
                MATCH (source:MedicalConcept)-[r]->(mc:MedicalConcept {name: $keyword})
                RETURN type(r) as relationship_type, source.name as related_concept, 'incoming' as direction
                """,
                {"keyword": keyword}
            )
            
            relationships = []
            for record in result:
                relationships.append({
                    "type": record["relationship_type"],
                    "direction": record["direction"],
                    "related_concept": record["related_concept"]
                })
            
            return relationships
    
    def find_related_concepts(self, keyword: str, max_depth: int = 2) -> List[Dict]:
        """
        Find concepts related to a keyword within a certain depth
        
        Args:
            keyword: The medical keyword to find related concepts for
            max_depth: Maximum relationship depth to traverse
            
        Returns:
            List of related concepts with their relationship paths
        """
        if not self.driver:
            return []
        
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH path = (start:MedicalConcept {name: $keyword})-[*1..%d]-(related:MedicalConcept)
                WHERE start <> related
                RETURN DISTINCT related.name as concept_name, 
                       length(path) as depth,
                       [rel in relationships(path) | type(rel)] as relationship_types
                ORDER BY depth, concept_name
                """ % max_depth,
                {"keyword": keyword}
            )
            
            return [{
                "concept": record["concept_name"],
                "depth": record["depth"],
                "relationship_path": record["relationship_types"]
            } for record in result]
    
    def visualize_graph(self, output_file: str = "medical_knowledge_graph.html"):
        """
        Create an interactive visualization of the medical knowledge graph
        
        Args:
            output_file: Output file for the visualization
        """
        if not self.driver:
            print("❌ No database connection available")
            return
        
        print("📊 Creating knowledge graph visualization...")
        
        # Get all nodes and edges
        with self.driver.session() as session:
            # Get all medical concepts
            concepts_result = session.run(
                """
                MATCH (mc:MedicalConcept)
                OPTIONAL MATCH (mc)-[:BELONGS_TO]->(c:Category)
                RETURN mc.name as name, c.name as category
                """
            )
            
            # Get all relationships
            relationships_result = session.run(
                """
                MATCH (source:MedicalConcept)-[r]->(target:MedicalConcept)
                RETURN source.name as source, target.name as target, type(r) as relationship_type
                """
            )
            
            # Convert results to lists to avoid consumption issues
            concepts_data = list(concepts_result)
            relationships_data = list(relationships_result)
        
        # Create NetworkX graph
        G = nx.DiGraph()
        
        # Add nodes
        concepts = {}
        for record in concepts_data:
            concept_name = record["name"]
            category = record["category"] or "uncategorized"
            concepts[concept_name] = category
            G.add_node(concept_name, category=category)
        
        # Add edges
        for record in relationships_data:
            G.add_edge(
                record["source"], 
                record["target"], 
                relationship=record["relationship_type"]
            )
        
        # Create Plotly visualization
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Prepare data for Plotly
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_info.append(G[edge[0]][edge[1]]['relationship'])
        
        # Create edge trace
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node traces for each category
        node_traces = []
        categories = list(set(concepts.values()))
        colors = px.colors.qualitative.Set3
        
        for i, category in enumerate(categories):
            category_nodes = [node for node, cat in concepts.items() if cat == category]
            
            node_x = [pos[node][0] for node in category_nodes]
            node_y = [pos[node][1] for node in category_nodes]
            
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=category_nodes,
                textposition="middle center",
                marker=dict(
                    size=20,
                    color=colors[i % len(colors)],
                    line=dict(width=2, color='black')
                ),
                name=category.replace('_', ' ').title(),
                textfont=dict(size=8)
            )
            node_traces.append(node_trace)
        
        # Create figure
        fig = go.Figure(data=[edge_trace] + node_traces,
                       layout=go.Layout(
                           title=dict(text='Medical Knowledge Graph', font=dict(size=16)),
                           showlegend=True,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Medical keywords and their relationships",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor='left', yanchor='bottom',
                               font=dict(color="black", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           plot_bgcolor='white'
                       ))
        
        # Save visualization
        fig.write_html(output_file)
        print(f"✅ Knowledge graph visualization saved to: {output_file}")
        
        return fig
    
    def export_to_json(self, output_file: str = "medical_knowledge_graph.json"):
        """
        Export the knowledge graph to JSON format
        
        Args:
            output_file: Output JSON file path
        """
        if not self.driver:
            return
        
        print("📤 Exporting knowledge graph to JSON...")
        
        with self.driver.session() as session:
            # Get all data
            result = session.run(
                """
                MATCH (mc:MedicalConcept)
                OPTIONAL MATCH (mc)-[:BELONGS_TO]->(c:Category)
                OPTIONAL MATCH (mc)-[r]->(target:MedicalConcept)
                RETURN mc.name as concept, c.name as category, 
                       collect(DISTINCT {type: type(r), target: target.name}) as outgoing_relationships
                """
            )
            
            data = {
                "metadata": {
                    "total_concepts": len(self.medical_keywords),
                    "categories": list(self.medical_ontology.keys()),
                    "relationship_types": list(self.relationships.keys())
                },
                "concepts": []
            }
            
            for record in result:
                concept_data = {
                    "name": record["concept"],
                    "category": record["category"],
                    "relationships": [rel for rel in record["outgoing_relationships"] if rel["type"] is not None]
                }
                data["concepts"].append(concept_data)
        
        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Knowledge graph exported to: {output_file}")
        return data

def main():
    """Main function to demonstrate the Medical Knowledge Graph"""
    print("🏥 Medical Knowledge Graph System")
    print("=" * 50)
    
    # Initialize the knowledge graph
    kg = MedicalKnowledgeGraph()
    
    if not kg.driver:
        print("❌ Cannot proceed without database connection")
        print("💡 Please ensure Neo4j is running and accessible")
        return
    
    try:
        # Initialize the graph
        kg.initialize_knowledge_graph()
        
        # Query examples
        print("\n🔍 Query Examples:")
        print("-" * 30)
        
        # Get all keywords
        all_keywords = kg.query_keywords()
        print(f"📋 Total medical keywords: {len(all_keywords)}")
        
        # Search for heart-related keywords
        heart_keywords = kg.query_keywords(query="heart")
        print(f"❤️ Heart-related keywords: {len(heart_keywords)}")
        for kw in heart_keywords:
            print(f"  • {kw['name']}")
        
        # Get keywords by category
        symptoms = kg.query_keywords(category="symptoms")
        print(f"\n🩺 Symptoms: {len(symptoms)}")
        for symptom in symptoms:
            print(f"  • {symptom['name']}")
        
        # Get relationships for a specific keyword
        print(f"\n🔗 Relationships for 'chest pain':")
        relationships = kg.get_relationships("chest pain")
        for rel in relationships:
            print(f"  • {rel['type']} -> {rel['related_concept']}")
        
        # Find related concepts
        print(f"\n🌐 Related concepts to 'cardiomyopathy' (depth 2):")
        related = kg.find_related_concepts("cardiomyopathy", max_depth=2)
        for concept in related[:5]:  # Show first 5
            print(f"  • {concept['concept']} (depth: {concept['depth']})")
        
        # Create visualization
        kg.visualize_graph()
        
        # Export to JSON
        kg.export_to_json()
        
        print("\n✅ Medical Knowledge Graph system is ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        kg.close()

if __name__ == "__main__":
    main()
