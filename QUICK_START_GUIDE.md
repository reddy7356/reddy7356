# 🚀 Medical Knowledge Graph - Quick Start Guide

## ✅ System Status
Your medical knowledge graph system is **fully operational** with:
- ✅ Neo4j database running in Docker
- ✅ 17 medical keywords organized into 6 categories
- ✅ 13 medical relationships
- ✅ RAG integration with your existing system
- ✅ Interactive query interface

## 🎯 Your Medical Keywords

### Cardiovascular Conditions
- significant acquired or congenital heart disease
- coronary heart disease
- cardiomyopathy
- congestive heart failure
- moderate to severe valvular disease

### Symptoms
- chest pain
- angina
- irregular heart beat
- syncope
- current heart murmur

### Acute Events
- myocardial infarction within 6 months
- dysrhythmias

### Risk Factors
- uncontrolled hypertension
- rheumatic fever

### Complications
- cerebrovascular and peripheral vascular disease

### Devices
- pacemaker
- defibrillator

## 🚀 Quick Commands

### 1. Start the System
```bash
# Easy way - run the system checker
python run_medical_kg.py

# Manual way - activate virtual environment
source .venv/bin/activate
```

### 2. Interactive Query Interface
```bash
source .venv/bin/activate && python kg_query_interface.py
```

**Available Commands:**
- `search heart` - Find heart-related keywords
- `category symptoms` - Show all symptoms
- `relationships chest pain` - Show relationships for chest pain
- `related cardiomyopathy 2` - Show related concepts (depth 2)
- `rag What heart conditions are mentioned?` - RAG query with KG
- `help` - Show all commands
- `quit` - Exit

### 3. Command Line Queries
```bash
# Search for keywords
source .venv/bin/activate && python kg_query_interface.py --command search --args heart

# Get relationships
source .venv/bin/activate && python kg_query_interface.py --command relationships --args "chest pain"

# Get symptoms
source .venv/bin/activate && python kg_query_interface.py --command category --args symptoms

# RAG integration
source .venv/bin/activate && python kg_query_interface.py --command rag --args "What heart conditions are mentioned?"
```

### 4. RAG Integration Test
```bash
source .venv/bin/activate && python rag_knowledge_graph_integration.py
```

## 🔗 Medical Relationships

### CAUSES
- coronary heart disease → chest pain
- coronary heart disease → angina
- cardiomyopathy → irregular heart beat
- uncontrolled hypertension → cardiomyopathy
- rheumatic fever → moderate to severe valvular disease

### LEADS_TO
- myocardial infarction within 6 months → cardiomyopathy
- dysrhythmias → syncope
- congestive heart failure → cerebrovascular and peripheral vascular disease

### TREATED_BY
- dysrhythmias → pacemaker
- dysrhythmias → defibrillator
- cardiomyopathy → defibrillator

### ASSOCIATED_WITH
- significant acquired or congenital heart disease ↔ coronary heart disease
- chest pain ↔ angina
- irregular heart beat ↔ dysrhythmias

## 🌐 Neo4j Browser Access

**URL:** http://localhost:7474
**Username:** neo4j
**Password:** medical123

**Sample Queries for Neo4j Browser:**
```cypher
// Get all medical concepts
MATCH (mc:MedicalConcept) RETURN mc.name

// Get all relationships
MATCH (source:MedicalConcept)-[r]->(target:MedicalConcept) 
RETURN source.name, type(r), target.name

// Find heart-related concepts
MATCH (mc:MedicalConcept) 
WHERE toLower(mc.name) CONTAINS 'heart' 
RETURN mc.name

// Get relationships for chest pain
MATCH (mc:MedicalConcept {name: 'chest pain'})-[r]-(related:MedicalConcept)
RETURN mc.name, type(r), related.name
```

## 🧪 Example Queries

### Search Examples
```bash
# Find all heart-related keywords
search heart

# Find all symptoms
category symptoms

# Find cardiovascular conditions
category cardiovascular_conditions

# Find devices
category devices
```

### Relationship Examples
```bash
# Get relationships for chest pain
relationships chest pain

# Get relationships for cardiomyopathy
relationships cardiomyopathy

# Get relationships for dysrhythmias
relationships dysrhythmias
```

### RAG Integration Examples
```bash
# Ask about heart conditions
rag What heart conditions are mentioned in the case reports?

# Ask about symptoms
rag What symptoms are related to heart disease?

# Ask about devices
rag What devices are mentioned for heart conditions?

# Ask about risk factors
rag Are there any cardiovascular risk factors mentioned?
```

## 🔧 Troubleshooting

### If Neo4j is not running:
```bash
# Start Neo4j container
docker run --name medical-neo4j -p 7474:7474 -p 7687:7687 -d --env NEO4J_AUTH=neo4j/password neo4j:latest

# Wait 10 seconds for startup
sleep 10
```

### If virtual environment issues:
```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### If import errors:
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Verify Neo4j is installed
python -c "import neo4j; print('✅ Neo4j installed')"
```

## 📊 System Information

- **Database:** Neo4j 5.x running in Docker
- **Python:** 3.13 with virtual environment
- **Medical Concepts:** 17 keywords
- **Categories:** 6 medical categories
- **Relationships:** 13 medical relationships
- **RAG Integration:** Enhanced with knowledge graph context

## 🎉 Success!

Your medical knowledge graph system is now fully operational and ready to enhance your RAG system with structured medical knowledge and relationships!

**Next Steps:**
1. Try the interactive interface: `source .venv/bin/activate && python kg_query_interface.py`
2. Test RAG integration: `source .venv/bin/activate && python rag_knowledge_graph_integration.py`
3. Explore Neo4j browser: http://localhost:7474
4. Add more medical concepts as needed
