# 🏥 Medical Knowledge Graph Setup Guide

This guide will help you set up and use the Neo4j-based medical knowledge graph system with your existing RAG model.

## 📋 Prerequisites

### 1. Neo4j Database
You need to install and run Neo4j database:

#### Option A: Neo4j Desktop (Recommended for beginners)
1. Download Neo4j Desktop from [neo4j.com](https://neo4j.com/download/)
2. Install and create a new project
3. Create a new database (use default settings)
4. Start the database
5. Note the connection details (usually `bolt://localhost:7687`)

#### Option B: Neo4j Community Edition
```bash
# Using Docker (easiest)
docker run \
    --name neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/medical123 \
    neo4j:latest
```

#### Option C: Local Installation
1. Download Neo4j Community Edition
2. Extract and configure
3. Set password in `conf/neo4j.conf`
4. Start with `bin/neo4j start`

### 2. Python Dependencies
```bash
# Install required packages
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Test Neo4j Connection
```bash
# Quick connection test
python test_kg_integration.py --quick
```

### 2. Initialize Knowledge Graph
```bash
# Initialize the medical knowledge graph
python medical_knowledge_graph.py
```

### 3. Test the System
```bash
# Run comprehensive tests
python test_kg_integration.py
```

### 4. Use the Query Interface
```bash
# Interactive query interface
python kg_query_interface.py
```

## 🔧 Configuration

### Database Connection
Edit the connection parameters in the Python files if needed:

```python
# Default connection settings
kg = MedicalKnowledgeGraph(
    uri="bolt://localhost:7687",
    user="neo4j", 
    password="medical123"
)
```

### Medical Keywords
The system comes pre-configured with your medical keywords:

- `significant acquired or congenital heart disease`
- `chest pain`
- `coronary heart disease`
- `angina`
- `myocardial infarction within 6 months`
- `irregular heart beat`
- `dysrhythmias`
- `syncope`
- `cardiomyopathy`
- `uncontrolled hypertension`
- `current heart murmur`
- `rheumatic fever`
- `moderate to severe valvular disease`
- `cerebrovascular and peripheral vascular disease`
- `congestive heart failure`
- `pacemaker`
- `defibrillator`

## 📚 Usage Examples

### 1. Interactive Query Interface
```bash
python kg_query_interface.py
```

Available commands:
- `search heart` - Search for heart-related keywords
- `category symptoms` - Show all symptoms
- `relationships chest pain` - Show relationships for chest pain
- `related cardiomyopathy 2` - Show related concepts
- `rag What heart conditions are mentioned?` - RAG query with KG
- `visualize` - Create knowledge graph visualization
- `export` - Export data to JSON

### 2. Programmatic Usage
```python
from medical_knowledge_graph import MedicalKnowledgeGraph

# Initialize
kg = MedicalKnowledgeGraph()

# Search keywords
results = kg.query_keywords(query="heart")

# Get relationships
relationships = kg.get_relationships("chest pain")

# Find related concepts
related = kg.find_related_concepts("cardiomyopathy", max_depth=2)

# Create visualization
kg.visualize_graph("my_graph.html")
```

### 3. RAG Integration
```python
from rag_knowledge_graph_integration import RAGKnowledgeGraphPipeline

# Initialize integrated pipeline
pipeline = RAGKnowledgeGraphPipeline()

# Run query with KG enhancement
result = pipeline.run("What heart conditions are mentioned?", documents)
print(result['kg_generator']['answer'])
```

## 🎯 Key Features

### 1. Medical Ontology
The system organizes medical keywords into categories:
- **Cardiovascular Conditions**: Heart diseases, cardiomyopathies
- **Symptoms**: Chest pain, angina, syncope
- **Acute Events**: Myocardial infarction, dysrhythmias
- **Risk Factors**: Hypertension, rheumatic fever
- **Complications**: Vascular diseases
- **Devices**: Pacemakers, defibrillators

### 2. Relationship Mapping
Pre-defined relationships between medical concepts:
- **CAUSES**: coronary heart disease → chest pain
- **LEADS_TO**: myocardial infarction → cardiomyopathy
- **TREATED_BY**: dysrhythmias → pacemaker
- **ASSOCIATED_WITH**: chest pain ↔ angina

### 3. Enhanced RAG
- Medical concept extraction from queries
- Knowledge graph context enhancement
- Related concept suggestions
- Category-based filtering

### 4. Visualization
- Interactive HTML visualizations
- Network graph representations
- Category-based color coding
- Relationship path highlighting

## 🔍 Query Examples

### Basic Keyword Search
```bash
kg> search heart
🔍 Search results for 'heart':
• coronary heart disease (Category: cardiovascular_conditions)
• congestive heart failure (Category: cardiovascular_conditions)
• significant acquired or congenital heart disease (Category: cardiovascular_conditions)
```

### Category-based Search
```bash
kg> category symptoms
📁 Keywords in category 'symptoms':
• angina
• chest pain
• current heart murmur
• irregular heart beat
• syncope
```

### Relationship Queries
```bash
kg> relationships chest pain
🔗 Relationships for 'chest pain':
• CAUSES → angina
• ASSOCIATED_WITH → angina
```

### RAG Integration
```bash
kg> rag What heart conditions are mentioned in the case reports?
❓ Query: What heart conditions are mentioned in the case reports?
💡 Answer: Based on the medical case report, the patient has a history of infiltrating ductal carcinoma of the breast with lytic metastases to the sacroiliac region.

🔍 Knowledge Graph Insights:
**Related Medical Concepts:** coronary heart disease, chest pain
**Medical Relationships Found:**
• CAUSES: angina
• ASSOCIATED_WITH: angina
**Related Conditions:** cardiomyopathy, dysrhythmias, syncope
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Neo4j Connection Failed
```
❌ Failed to connect to Neo4j: [Errno 61] Connection refused
```
**Solutions:**
- Ensure Neo4j is running: `neo4j status`
- Check connection details (URI, username, password)
- Verify firewall settings
- Try `bolt://localhost:7687` for local connections

#### 2. Authentication Failed
```
❌ Failed to connect to Neo4j: Authentication failed
```
**Solutions:**
- Check username/password in Neo4j
- Default credentials: `neo4j/medical123`
- Reset password in Neo4j Browser: `:server change-password`

#### 3. Import Errors
```
ModuleNotFoundError: No module named 'neo4j'
```
**Solutions:**
- Install dependencies: `pip install -r requirements.txt`
- Activate virtual environment
- Check Python version compatibility

#### 4. Empty Knowledge Graph
```
❌ No results found for 'heart'
```
**Solutions:**
- Initialize the graph: `python medical_knowledge_graph.py`
- Check if initialization completed successfully
- Verify data was inserted: `python test_kg_integration.py`

### Performance Optimization

#### 1. Large Datasets
- Use indexes for frequently queried properties
- Limit relationship depth in queries
- Use pagination for large result sets

#### 2. Memory Usage
- Close database connections properly
- Use streaming for large exports
- Monitor memory usage during visualization

## 📊 Advanced Usage

### 1. Custom Medical Ontology
Edit `medical_knowledge_graph.py` to add your own medical concepts:

```python
# Add new keywords
self.medical_keywords.extend([
    'your_new_keyword',
    'another_medical_term'
])

# Add new categories
self.medical_ontology['new_category'] = [
    'keyword1',
    'keyword2'
]

# Add new relationships
self.relationships['NEW_RELATIONSHIP'] = [
    ('source_concept', 'target_concept')
]
```

### 2. Custom RAG Enhancement
Modify `rag_knowledge_graph_integration.py` to add domain-specific logic:

```python
# Add custom concept mapping
self.concept_mapping.update({
    'your_term': ['synonym1', 'synonym2']
})

# Custom relationship scoring
def custom_scoring(self, concept, document):
    # Your custom scoring logic
    return score
```

### 3. Integration with External Systems
```python
# Export for external use
data = kg.export_to_json("medical_kg.json")

# Import from external source
with open("external_data.json") as f:
    external_data = json.load(f)
    # Process and insert into Neo4j
```

## 📈 Monitoring and Maintenance

### 1. Database Health
```bash
# Check Neo4j status
neo4j status

# Monitor database size
du -sh ~/neo4j/data/databases/
```

### 2. Performance Monitoring
- Monitor query execution times
- Check memory usage
- Review slow query logs

### 3. Backup and Recovery
```bash
# Backup Neo4j database
neo4j-admin dump --database=neo4j --to=backup.dump

# Restore from backup
neo4j-admin load --database=neo4j --from=backup.dump
```

## 🤝 Support and Contributing

### Getting Help
1. Check this documentation
2. Run the test suite: `python test_kg_integration.py`
3. Check Neo4j logs for database issues
4. Review the troubleshooting section

### Contributing
1. Fork the repository
2. Add your medical concepts and relationships
3. Test thoroughly
4. Submit a pull request

## 📄 License and Compliance

This system is designed for educational and research purposes. When using with real medical data:
- Ensure HIPAA compliance
- Follow institutional data policies
- Use secure database configurations
- Implement proper access controls

---

**Ready to start? Run `python test_kg_integration.py --quick` to test your setup!** 🚀
