# 🔍 Keyword Search System - User Guide

## 🎯 **What This System Does**

Instead of asking natural language questions like "What are the patient ages?", you can now search for **specific keywords** directly in your medical case reports. This gives you precise control over what you're looking for.

## 🚀 **Quick Start**

### **1. Search Specific Keywords**
```bash
# Search for age-related terms
python search_keywords.py "age,74,woman"

# Search for medications
python search_keywords.py "propofol,drip,mg"

# Search for procedures
python search_keywords.py "PCI,ablation,intubation"
```

### **2. Search by Category**
```bash
# Search all demographic keywords
python search_keywords.py --category demographics

# Search all medication keywords
python search_keywords.py --category medications

# Search all diagnosis keywords
python search_keywords.py --category diagnoses
```

### **3. Show Available Options**
```bash
# Show all available categories
python search_keywords.py --show-categories

# Show keywords in a specific category
python search_keywords.py --show-keywords medications
```

## 📋 **Available Categories**

### **1. Demographics**
- **Keywords**: age, old, year, male, female, man, woman, sex, gender
- **Use**: Find patient demographic information

### **2. Diagnoses**
- **Keywords**: diagnosis, condition, disease, cancer, carcinoma, failure, apnea, amyloidosis, diabetes, hypertension, fibrillation, obstructive, sleep, heart, coronary, atrial, cardiac
- **Use**: Find medical diagnoses and conditions

### **3. Medications**
- **Keywords**: medication, drug, medicine, propofol, remifentanil, rivaroxaban, naproxen, vasopressor, drip, infusion, injection, mg, mcg, ml
- **Use**: Find medications and dosages

### **4. Procedures**
- **Keywords**: procedure, surgery, operation, intervention, performed, underwent, placed, PCI, ablation, intubation, catheter, endotracheal
- **Use**: Find medical procedures and surgeries

### **5. Complications**
- **Keywords**: complication, problem, issue, hypotension, fibrillation, pressure, drop, tachycardic, bradycardic, arrhythmia
- **Use**: Find complications and problems

### **6. Outcomes**
- **Keywords**: outcome, result, discharge, died, survived, recovered, improved, transferred, ICU, SICU, ward
- **Use**: Find patient outcomes and results

### **7. Vital Signs**
- **Keywords**: blood pressure, heart rate, HR, BP, ABP, bpm, mm Hg, oxygen, saturation, temperature, pulse, respiratory rate
- **Use**: Find vital signs and measurements

### **8. Lab Values**
- **Keywords**: lab, laboratory, blood, test, result, value, level, count, hemoglobin, hematocrit, glucose, creatinine, BUN
- **Use**: Find laboratory results and values

## 🔧 **Advanced Options**

### **Case Sensitive Search**
```bash
# Search with case sensitivity
python search_keywords.py "Propofol,Drip" --case-sensitive
```

### **Exact Word Match**
```bash
# Search for exact words only (not partial matches)
python search_keywords.py "heart failure" --exact-match
```

### **Combined Options**
```bash
# Case sensitive + exact match
python search_keywords.py "Heart Failure" --case-sensitive --exact-match
```

## 📊 **Understanding Results**

### **Summary Section**
```
📊 Summary:
   • Keywords found: 3          # How many keywords were found
   • Keywords not found: 2      # How many keywords were not found
   • Total matches: 23          # Total number of matches across all cases
   • Case reports searched: 20  # Number of case reports analyzed
```

### **Keywords Found/Not Found**
```
✅ Keywords Found:
   • age
   • 74
   • woman

❌ Keywords Not Found:
   • height
   • weight
```

### **Matches by Case Report**
```
🏥 Case Trial 1 (4 matches):
   • 'age' found 2 time(s)
     Context: ...a 74-year-old woman with a history of infiltrating ductal carcinoma...
   • '74' found 1 time(s)
     Context: ...a 74-year-old woman with a history of infiltrating ductal carcinoma...
```

## 🎯 **Common Use Cases**

### **1. Find Patient Ages**
```bash
python search_keywords.py "age,old,year,74,84"
```

### **2. Find Specific Medications**
```bash
python search_keywords.py "propofol,remifentanil,vasopressor"
```

### **3. Find Heart Conditions**
```bash
python search_keywords.py "heart,failure,coronary,atrial,fibrillation"
```

### **4. Find Procedures**
```bash
python search_keywords.py "PCI,ablation,intubation,catheter"
```

### **5. Find Complications**
```bash
python search_keywords.py "hypotension,complication,problem,issue"
```

### **6. Find Vital Signs**
```bash
python search_keywords.py "blood pressure,heart rate,HR,BP,bpm"
```

## 💡 **Pro Tips**

### **1. Use Multiple Keywords**
- Search for related terms together: `"age,old,year,74,84"`
- This gives you comprehensive coverage

### **2. Use Categories for Broad Searches**
- `--category medications` searches all medication-related keywords
- `--category diagnoses` searches all diagnosis-related keywords

### **3. Combine Specific and General**
- Use specific terms: `"propofol,remifentanil"`
- Use general terms: `"drip,infusion,mg"`

### **4. Use Exact Match for Precision**
- `--exact-match` prevents partial matches
- Useful for specific terms like "heart failure"

### **5. Use Case Sensitive for Proper Nouns**
- `--case-sensitive` for drug names, proper nouns
- Useful for "Propofol" vs "propofol"

## 🔍 **Interactive Mode**

For a more interactive experience, use the full keyword search system:

```bash
python keyword_search.py
```

This provides a menu-driven interface with options to:
1. Search specific keywords
2. Search by category
3. Show available categories
4. Show category keywords
5. Exit

## 📈 **Performance**

- **Fast**: Keyword search is much faster than natural language processing
- **Precise**: You get exact matches for what you're looking for
- **Comprehensive**: Search across all case reports simultaneously
- **Flexible**: Multiple search options and categories

## 🆚 **Keyword Search vs Natural Language**

| Feature | Keyword Search | Natural Language |
|---------|----------------|------------------|
| **Speed** | ⚡ Very Fast | 🐌 Slower |
| **Precision** | 🎯 Exact | 📝 Interpreted |
| **Control** | 🎮 Full Control | 🤖 AI Interpretation |
| **Flexibility** | 🔧 Highly Flexible | 📋 Limited |
| **Learning Curve** | 📚 Easy | 🧠 Requires Understanding |

## 🚀 **Get Started Now!**

```bash
# Start with a simple search
python search_keywords.py "age,74,woman"

# Try a category search
python search_keywords.py --category medications

# Explore available options
python search_keywords.py --show-categories
```

**🎉 You now have precise control over searching your medical case reports!**
