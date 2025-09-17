# 🏥 MIMIC IV Patient Query System - Quick Start Guide

## ✅ System Status: READY TO USE!

Your MIMIC IV patient query system is now fully operational with 200 patients indexed and searchable.

## 🚀 Quick Commands

### 1. **Search for Patients (Command Line)**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Search for diabetes patients
python mimic_query_cli.py "diabetes"

# Search specific patients
python mimic_query_cli.py "chest pain" --patients "10019957,10023771"

# Search with medical categories
python mimic_query_cli.py "hypertension" --categories "diagnoses,vitals"
```

### 2. **Web Interface**
```bash
# Start web interface
source .venv/bin/activate
python mimic_web_interface.py

# Then open browser to: http://localhost:5000
```

### 3. **Interactive Mode**
```bash
source .venv/bin/activate
python mimic_query_cli.py --interactive
```

### 4. **Run Examples**
```bash
source .venv/bin/activate
python mimic_examples.py
```

## 🔍 Example Queries to Try

### Medical Conditions
- `"coronary artery disease"` - Heart disease patients
- `"diabetes mellitus"` - Diabetic patients
- `"hypertension"` - High blood pressure patients
- `"pneumonia"` - Lung infection patients
- `"stroke"` - Stroke patients

### Procedures
- `"CABG"` - Coronary artery bypass surgery
- `"catheterization"` - Heart catheterization
- `"surgery"` - Any surgical procedures
- `"valve replacement"` - Heart valve surgery

### Medications
- `"aspirin"` - Patients on aspirin
- `"warfarin"` - Blood thinner patients
- `"metoprolol"` - Beta blocker patients
- `"insulin"` - Insulin-dependent patients

### Symptoms
- `"chest pain"` - Patients with chest pain
- `"shortness of breath"` - Breathing problems
- `"fatigue"` - Tired patients
- `"nausea"` - Nausea symptoms

### Lab Values
- `"hemoglobin"` - Blood count issues
- `"creatinine"` - Kidney function
- `"glucose"` - Blood sugar levels
- `"troponin"` - Heart enzyme levels

## 📊 Database Statistics

- **Total Patients**: 200
- **Total Keywords**: 2,334
- **Total Medical Terms**: 137
- **Top Services**: MEDICINE (106), SURGERY (22), NEUROLOGY (17)
- **Top Diagnoses**: MI (200), DM (200), Hypertension (100)
- **Top Medications**: ASA (139), Aspirin (105), Metoprolol (66)

## 🎯 Use Cases

### Clinical Research
```bash
# Find all patients with specific condition
python mimic_query_cli.py "coronary artery disease" --max-results 20

# Find patients who had specific procedure
python mimic_query_cli.py "CABG" --categories "procedures"
```

### Medical Education
```bash
# Study specific patient cases
python mimic_query_cli.py --patient-info 10019957

# Compare treatment approaches
python mimic_query_cli.py "aspirin warfarin" --max-results 10
```

### Quality Assurance
```bash
# Find patients with complications
python mimic_query_cli.py "complications" --categories "symptoms"

# Review medication patterns
python mimic_query_cli.py "medication" --categories "medications"
```

## 🔧 Advanced Features

### Patient-Specific Search
```bash
# Search only specific patients
python mimic_query_cli.py "diabetes" --patients "10019957,10023771,10026161"
```

### Category Filtering
```bash
# Search only in diagnoses
python mimic_query_cli.py "heart" --categories "diagnoses"

# Search multiple categories
python mimic_query_cli.py "pain" --categories "symptoms,diagnoses"
```

### Complex Queries
```bash
# Multiple conditions
python mimic_query_cli.py "diabetes hypertension"

# Procedure and medication
python mimic_query_cli.py "CABG aspirin"

# Symptoms and lab values
python mimic_query_cli.py "chest pain troponin"
```

## 📱 Web Interface Features

The web interface provides:
- **Visual Search**: Easy-to-use search form
- **Real-time Results**: Instant search results
- **Patient Details**: Click to see full patient information
- **Category Selection**: Filter by medical categories
- **Export Options**: Save search results

## 🆘 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   source .venv/bin/activate
   pip install flask pandas
   ```

2. **"No results found"**
   - Try broader search terms
   - Check spelling
   - Use partial matches

3. **Slow performance**
   - Reduce max-results
   - Use specific patient IDs
   - Filter by categories

### Getting Help

1. **Run examples**: `python mimic_examples.py`
2. **Interactive mode**: `python mimic_query_cli.py --interactive`
3. **Check stats**: `python mimic_query_cli.py --stats`
4. **List patients**: `python mimic_query_cli.py --list-patients 20`

## 🎉 You're All Set!

Your MIMIC IV patient query system is ready to use. Start with simple queries and explore the rich medical data from your 200 patients.

**Happy Querying! 🏥🔍**
