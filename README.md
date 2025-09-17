# 🏥 MIMIC IV Patient Query System

A comprehensive system for querying and analyzing MIMIC IV patient records with advanced keyword search capabilities. This system provides multiple interfaces to search through 200 MIMIC IV patient records with medical terminology recognition and intelligent relevance scoring.

## 🌟 Features

- **🔍 Advanced Medical Search**: Intelligent keyword search with medical terminology recognition
- **📊 Patient Indexing**: 200 MIMIC IV patients fully indexed and searchable
- **🎯 Multiple Interfaces**: CLI, Web, and Python API
- **📈 Relevance Scoring**: Results ranked by medical relevance
- **🏷️ Category Filtering**: Search by medical categories (diagnoses, procedures, medications, etc.)
- **👥 Patient Filtering**: Search specific patients or all patients
- **📝 Context Extraction**: Shows relevant sections from patient records
- **⚡ Fast Performance**: <1 second search times

## 🚀 Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

### Basic Usage

#### Command Line Interface

```bash
# Search for patients with diabetes
python mimic_query_cli.py "diabetes"

# Search specific patients
python mimic_query_cli.py "chest pain" --patients "10019957,10023771"

# Show database statistics
python mimic_query_cli.py --stats

# Interactive mode
python mimic_query_cli.py --interactive
```

#### Web Interface

```bash
python mimic_web_interface.py
# Open browser to: http://localhost:5000
```

#### Python API

```python
from mimic_patient_query_system import MIMICQueryInterface

# Initialize the system
interface = MIMICQueryInterface()

# Search for patients
results = interface.search("coronary artery disease", max_results=5)

# Get patient information
info = interface.get_patient_info("10019957")
```

## 📁 Project Structure

```
├── mimic_patient_query_system.py    # Core system with indexing and search
├── mimic_query_cli.py               # Command-line interface
├── mimic_web_interface.py           # Flask web interface
├── mimic_examples.py                # Usage examples and demonstrations
├── run_mimic_system.py              # Easy launcher script
├── patient_txt_200/                 # Directory containing 200 patient files
├── requirements.txt                 # Python dependencies
├── QUICK_START_MIMIC.md            # Quick start guide
└── README.md                       # This file
```

## 🔍 Search Capabilities

### Medical Categories

The system automatically recognizes and indexes:

- **Diagnoses**: coronary artery disease, diabetes, hypertension, pneumonia, etc.
- **Procedures**: surgery, catheterization, CABG, stent placement, etc.
- **Medications**: aspirin, warfarin, metoprolol, insulin, etc.
- **Vitals**: blood pressure, heart rate, temperature, oxygen saturation, etc.
- **Lab Values**: hemoglobin, creatinine, glucose, sodium, potassium, etc.
- **Symptoms**: chest pain, shortness of breath, fatigue, nausea, etc.

### Example Queries

```bash
# Medical conditions
python mimic_query_cli.py "coronary artery disease"
python mimic_query_cli.py "diabetes mellitus"
python mimic_query_cli.py "hypertension"

# Procedures
python mimic_query_cli.py "CABG surgery"
python mimic_query_cli.py "catheterization"
python mimic_query_cli.py "valve replacement"

# Medications
python mimic_query_cli.py "aspirin warfarin"
python mimic_query_cli.py "metoprolol"
python mimic_query_cli.py "insulin"

# Symptoms
python mimic_query_cli.py "chest pain"
python mimic_query_cli.py "shortness of breath"
python mimic_query_cli.py "fatigue"

# Lab values
python mimic_query_cli.py "hemoglobin creatinine"
python mimic_query_cli.py "troponin"
```

## 📊 Database Statistics

- **Total Patients**: 200
- **Total Keywords**: 2,334
- **Total Medical Terms**: 137
- **Top Services**: MEDICINE (106), SURGERY (22), NEUROLOGY (17)
- **Top Diagnoses**: MI (200), DM (200), Hypertension (100)
- **Top Medications**: ASA (139), Aspirin (105), Metoprolol (66)

## 🎯 Use Cases

### Clinical Research
- Find patients with specific conditions for research studies
- Identify patients who received particular treatments
- Analyze medication patterns across patient populations

### Medical Education
- Study real patient cases with specific conditions
- Compare treatment approaches across different patients
- Learn from actual clinical documentation

### Quality Assurance
- Identify patients with specific complications
- Review medication administration patterns
- Analyze discharge outcomes

### Data Analysis
- Extract structured data from unstructured clinical notes
- Identify patterns in patient presentations
- Generate reports on specific medical conditions

## 🔧 API Reference

### MIMICQueryInterface

#### Methods

- `search(query, patient_ids=None, categories=None, max_results=10)`
  - Search for patients based on query
  - Returns list of SearchResult objects

- `get_patient_info(patient_id)`
  - Get detailed information about a specific patient
  - Returns dictionary with patient metadata and medical terms

- `get_database_stats()`
  - Get statistics about the patient database
  - Returns dictionary with counts and distributions

- `list_patients(limit=20)`
  - List available patient IDs
  - Returns list of patient ID strings

### SearchResult Object

```python
@dataclass
class SearchResult:
    patient_id: str              # Patient identifier
    relevance_score: float       # Relevance score (0-100+)
    matched_sections: List[str]  # Matching text sections
    matched_keywords: List[str]  # Matching keywords
    context: str                 # Context around matches
    metadata: Dict[str, Any]     # Patient metadata
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/reddy7356/reddy7356.git
cd reddy7356
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run examples:
```bash
python mimic_examples.py
```

## 📈 Performance

- **Indexing**: ~30 seconds for 200 patients
- **Search Speed**: <1 second for most queries
- **Memory Usage**: ~100MB for full dataset
- **Scalability**: Designed to handle thousands of patients

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is designed for educational and research purposes. Please ensure compliance with MIMIC IV data usage agreements.

## 🆘 Support

For issues or questions:
1. Check the examples in `mimic_examples.py`
2. Review the quick start guide: `QUICK_START_MIMIC.md`
3. Test with interactive mode: `python mimic_query_cli.py --interactive`
4. Use the web interface for visual debugging

## 📞 Contact

- GitHub: [reddy7356](https://github.com/reddy7356)
- Repository: [reddy7356/reddy7356](https://github.com/reddy7356/reddy7356)

---

**Happy Querying! 🏥🔍**