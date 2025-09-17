# 🚀 Quick Reference Guide - Intelligent Medical RAG System

## ⚡ **Start Here - Quick Commands**

```bash
# 🧠 Test the entire system
python intelligent_medical_extractor.py

# ❓ Ask a single question
python ask_specific_question.py "What are the patient ages?"

# 💬 Start interactive chatbot
python chatbot.py

# 🔍 Query multiple cases
python query_multiple_cases.py "What complications occurred?"

# ➕ Add new case report
python add_case_report.py

# 💾 Save analysis results
python save_answers.py
```

---

## 🎯 **Common Questions & Commands**

### **Patient Demographics**
```bash
# Get patient ages
python ask_specific_question.py "What are the patient ages?"

# Get patient sex/gender
python ask_specific_question.py "What is the patient sex?"

# Get patient demographics
python ask_specific_question.py "What are the patient demographics?"
```

### **Medical Information**
```bash
# Get diagnoses
python ask_specific_question.py "What are the diagnoses?"

# Get medications
python ask_specific_question.py "What medications were used?"

# Get procedures
python ask_specific_question.py "What procedures were performed?"

# Get complications
python ask_specific_question.py "What complications occurred?"

# Get outcomes
python ask_specific_question.py "What are the patient outcomes?"
```

### **Specific Medical Terms**
```bash
# Heart-related
python ask_specific_question.py "What heart conditions are present?"

# Respiratory
python ask_specific_question.py "What respiratory issues occurred?"

# Cancer-related
python ask_specific_question.py "What cancer diagnoses are mentioned?"

# Anesthesia
python ask_specific_question.py "What anesthesia was used?"
```

---

## 📊 **Example Outputs**

### **Patient Ages**
```
❓ Question: What are the patient ages?
💡 Answer:
Patient ages found:
• 74-year-old woman
• 84
• 74
• 84-year-old woman
```

### **Medications**
```
❓ Question: What medications were used?
💡 Answer:
Medications found:
• propofol drip
• remifentanil drip
• vasopressor drip
• at 130 mcg
• was 100 mL
```

### **Diagnoses**
```
❓ Question: What are the diagnoses?
💡 Answer:
Key Diagnoses found:
• obstructive sleep apnea
• atrial fibrillation
• coronary artery disease
• infiltrating ductal carcinoma of the breast
• heart failure
• diabetes mellitus
```

---

## 🔧 **Troubleshooting Quick Fixes**

### **File Not Found Error**
```bash
# Check if case reports exist
ls -la case_reports/

# Verify configuration
cat case_reports_config.json
```

### **Import Errors**
```bash
# Activate virtual environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### **Encoding Issues**
```bash
# The system automatically handles multiple encodings
# If issues persist, check file format
file case_reports/your_file.txt
```

### **Memory Issues**
```bash
# Reduce retrieval depth in multi_case_rag.py
# Change top_k from 5 to 3
```

---

## 📁 **File Locations**

### **Core System Files**
- **Main System**: `intelligent_medical_extractor.py`
- **Multi-Case**: `multi_case_rag.py`
- **Single Query**: `ask_specific_question.py`
- **Interactive**: `chatbot.py`

### **Configuration**
- **Case Reports**: `case_reports/` directory
- **Config File**: `case_reports_config.json`
- **Dependencies**: `requirements.txt`

### **Documentation**
- **User Guide**: `README.md`
- **Technical Docs**: `TECHNICAL_DOCUMENTATION.md`
- **Case Management**: `HOW_TO_ADD_CASE_REPORTS.md`

---

## 🆕 **Adding New Case Reports**

### **Quick Add (Recommended)**
```bash
python add_case_report.py
# Follow prompts to add your case report
```

### **Manual Add**
1. Copy file to `case_reports/` directory
2. Edit `case_reports_config.json`
3. Add entry: `"Case Name": "case_reports/filename.txt"`

---

## 📈 **Performance Tips**

### **Fast Queries**
- Use specific questions instead of general ones
- Reduce `top_k` parameter for faster responses
- Process fewer case reports simultaneously

### **Comprehensive Analysis**
- Increase `top_k` parameter for more thorough retrieval
- Use batch processing with `save_answers.py`
- Run comprehensive tests with `intelligent_medical_extractor.py`

---

## 🔍 **Advanced Usage**

### **Custom Questions**
```bash
# Ask about specific conditions
python ask_specific_question.py "What sleep disorders are present?"

# Ask about specific procedures
python ask_specific_question.py "What cardiac procedures were performed?"

# Ask about specific medications
python ask_specific_question.py "What vasopressors were used?"
```

### **Batch Processing**
```bash
# Save results to file
python save_answers.py

# This will process multiple questions and save to timestamped file
```

---

## 📞 **Need Help?**

### **Quick Checks**
1. ✅ Virtual environment activated?
2. ✅ Dependencies installed?
3. ✅ Case reports in correct directory?
4. ✅ Configuration file updated?

### **Common Solutions**
- **Restart**: Deactivate and reactivate virtual environment
- **Reinstall**: `pip install -r requirements.txt`
- **Check Paths**: Verify file paths in configuration
- **Test System**: Run `python intelligent_medical_extractor.py`

---

## 🎯 **Success Indicators**

### **System Working Correctly**
- ✅ Loads all case reports without errors
- ✅ Processes queries in 1-3 seconds
- ✅ Returns structured, bullet-pointed answers
- ✅ Handles multiple question types
- ✅ Shows clean, organized output

### **Expected Performance**
- **Startup**: 2-5 seconds
- **Query Processing**: 1-3 seconds
- **Memory Usage**: 200-500MB
- **File Loading**: 100-500ms per case report

---

## 🚀 **Pro Tips**

1. **Start Simple**: Begin with basic questions like "What are the patient ages?"
2. **Be Specific**: Ask targeted questions for better results
3. **Use Keywords**: Include medical terms in your questions
4. **Batch Process**: Use `save_answers.py` for multiple questions
5. **Regular Testing**: Run `intelligent_medical_extractor.py` to verify system health

---

**🎉 You're all set! Start with `python intelligent_medical_extractor.py` to test your system!**
