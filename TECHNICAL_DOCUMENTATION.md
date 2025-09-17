# 🏥 Intelligent Medical RAG System - Technical Documentation

## 📋 **Table of Contents**

1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Data Flow](#data-flow)
4. [Extraction Patterns](#extraction-patterns)
5. [Pipeline Configuration](#pipeline-configuration)
6. [File Structure](#file-structure)
7. [API Reference](#api-reference)
8. [Performance Characteristics](#performance-characteristics)
9. [Error Handling](#error-handling)
10. [Customization Guide](#customization-guide)

---

## 🏗️ **System Architecture**

### **High-Level Overview**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Case Reports │    │  Document Loader │    │  Haystack Docs │
│   (Text Files) │───▶│  (Multi-Encoding)│───▶│  (Chunked)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  User Query    │───▶│  Multi-Case      │───▶│  Intelligent    │
│  (Natural Lang)│    │  Retriever       │    │  Extractor      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Structured    │◀───│  Specific Answer │◀───│  Pattern        │
│  Output        │    │  Generator       │    │  Matching       │
│  (Bullet List) │    │  (Haystack Comp) │    │  (Regex Engine) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **Component Interaction Flow**
1. **Document Loading**: Multi-encoding text file loader
2. **Document Processing**: Haystack Document creation with metadata
3. **Query Processing**: Natural language query analysis
4. **Retrieval**: Multi-case document retrieval with medical terminology
5. **Extraction**: Regex-based pattern matching for specific information
6. **Generation**: Structured answer formatting and output

---

## 🔧 **Core Components**

### **1. IntelligentMedicalExtractor Class**

#### **Purpose**
Core extraction engine that uses regex patterns to identify and extract specific medical information from text documents.

#### **Key Methods**
```python
class IntelligentMedicalExtractor:
    def __init__(self):
        # Initialize extraction patterns
        
    def extract_specific_info(self, documents: List[Document], query: str) -> Dict[str, Any]:
        # Main extraction method
        
    def _extract_ages(self, documents: List[Document]) -> List[str]:
        # Age extraction logic
        
    def _extract_diagnoses(self, documents: List[Document]) -> List[str]:
        # Diagnosis extraction logic
```

#### **Pattern Categories**
- **Demographics**: Age, sex, gender
- **Medical**: Diagnoses, conditions, diseases
- **Treatment**: Medications, procedures, surgeries
- **Outcomes**: Complications, results, discharges

### **2. SpecificAnswerGenerator Component**

#### **Purpose**
Haystack component that integrates with the extraction engine to provide structured answers.

#### **Component Interface**
```python
@component
class SpecificAnswerGenerator:
    @component.output_types(answer=str)
    def run(self, query: str, documents: List[Document]):
        # Process query and generate structured answer
```

#### **Answer Formatting Methods**
- `_format_age_answer()`: Patient age information
- `_format_diagnosis_answer()`: Medical diagnoses
- `_format_medication_answer()`: Drug and treatment information
- `_format_procedure_answer()`: Surgical and medical procedures

### **3. MultiCaseMedicalRetriever**

#### **Purpose**
Enhanced retriever component that handles multiple case reports with medical terminology optimization.

#### **Features**
- **Medical Term Mapping**: Prioritizes medical terminology
- **Multi-Case Support**: Simultaneous retrieval from multiple sources
- **Configurable Top-K**: Adjustable retrieval depth
- **Metadata Preservation**: Maintains case report source information

---

## 🔄 **Data Flow**

### **1. Document Loading Phase**
```
Text Files → Encoding Detection → Text Processing → Haystack Documents
     ↓              ↓                ↓              ↓
case_reports/   utf-8/latin-1   Paragraph      Document objects
                auto-detect      Chunking      with metadata
```

### **2. Query Processing Phase**
```
User Query → Query Analysis → Pattern Matching → Information Extraction
     ↓            ↓              ↓                ↓
Natural Lang   Keyword        Regex Engine    Structured Data
Question      Identification  Pattern Match   Dictionary
```

### **3. Answer Generation Phase**
```
Extracted Data → Format Selection → Answer Generation → Structured Output
      ↓              ↓               ↓                ↓
Raw Results    Query Type      Formatting        Bullet Points
Dictionary     Detection       Methods           Clean Text
```

---

## 🧠 **Extraction Patterns**

### **Age Extraction Patterns**
```python
'age': [
    r'(\d+)-year-old',                    # "74-year-old"
    r'(\d+)\s*year[s]?\s*old',           # "74 years old"
    r'age[:\s]+(\d+)',                   # "age: 74"
    r'in\s*his\s*(\d+)s',                # "in his 70s"
    r'in\s*her\s*(\d+)s',                # "in her 70s"
    r'(\d+)-year-old\s*(male|female|man|woman)',  # "74-year-old woman"
]
```

### **Diagnosis Extraction Patterns**
```python
'diagnosis': [
    r'diagnosis[:\s]+([^.]+)',           # "diagnosis: heart failure"
    r'history\s+of\s+([^.]+)',           # "history of diabetes"
    r'(\w+\s+\w+\s+\w+)\s+(cancer|carcinoma|disease|failure|apnea|amyloidosis)',
    r'(obstructive\s+sleep\s+apnea|obstructive\s+sleep\s+apnoea)',
    r'(heart\s+failure)',
    r'(coronary\s+artery\s+disease)',
    r'(diabetes\s+mellitus)',
    r'(hypertension)',
    r'(atrial\s+fibrillation)'
]
```

### **Medication Extraction Patterns**
```python
'medications': [
    r'(\w+)\s+(\d+)\s*(mg|mcg|ml|units?)\s*(IV|PO|IM|SC)',  # "propofol 100 mg IV"
    r'(\w+)\s+(drip|infusion|injection)',                     # "propofol drip"
    r'(propofol|remifentanil|rivaroxaban|naproxen|vasopressor)\s+(drip|infusion|injection|mg|mcg)',
]
```

### **Procedure Extraction Patterns**
```python
'procedures': [
    r'(surgery|operation|procedure|intervention)[:\s]+([^.]+)',
    r'performed\s+([^.]+)',              # "performed PCI"
    r'underwent\s+([^.]+)',              # "underwent surgery"
    r'placed\s+([^.]+)',                 # "placed endotracheal tube"
]
```

---

## ⚙️ **Pipeline Configuration**

### **Basic Pipeline Structure**
```python
def create_intelligent_pipeline() -> Pipeline:
    # Create components
    retriever = MultiCaseMedicalRetriever(top_k=5)
    generator = SpecificAnswerGenerator()
    
    # Create pipeline
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("generator", generator)
    pipeline.connect("retriever.documents", "generator.documents")
    
    return pipeline
```

### **Pipeline Execution Flow**
```python
# Run query
result = pipeline.run({
    "retriever": {
        "query": question,
        "documents": documents
    },
    "generator": {
        "query": question
    }
})
```

### **Component Configuration Options**
- **Retriever**: `top_k`, medical term mapping, case report sources
- **Generator**: Extraction patterns, formatting options, output types
- **Pipeline**: Component connections, execution order, error handling

---

## 📁 **File Structure**

### **Core System Files**
```
intelligent_medical_extractor.py     # Main extraction engine
multi_case_rag.py                    # Multi-case RAG implementation
ask_specific_question.py             # Single question interface
query_multiple_cases.py              # Multi-case query interface
```

### **Support Files**
```
add_case_report.py                   # Case report management
save_answers.py                      # Batch processing and saving
chatbot.py                          # Interactive interface
app.py                              # Main application entry point
```

### **Configuration Files**
```
case_reports_config.json             # Case report paths and metadata
requirements.txt                     # Python dependencies
```

### **Documentation Files**
```
README.md                           # User guide and quick start
TECHNICAL_DOCUMENTATION.md          # This technical document
HOW_TO_ADD_CASE_REPORTS.md         # Case report management guide
```

---

## 🔌 **API Reference**

### **Main Functions**

#### **query_with_intelligent_extraction()**
```python
def query_with_intelligent_extraction(
    question: str, 
    case_reports_config: Dict[str, str]
) -> str:
    """
    Main function for querying the intelligent extraction system.
    
    Args:
        question: Natural language question about medical cases
        case_reports_config: Dictionary mapping case names to file paths
        
    Returns:
        Structured answer string with extracted information
        
    Raises:
        Exception: If pipeline execution fails
    """
```

#### **load_multiple_case_reports()**
```python
def load_multiple_case_reports(
    case_reports_config: Dict[str, str]
) -> List[Document]:
    """
    Load multiple case reports with automatic encoding detection.
    
    Args:
        case_reports_config: Case report configuration dictionary
        
    Returns:
        List of Haystack Document objects
        
    Raises:
        FileNotFoundError: If case report files not found
        UnicodeDecodeError: If encoding detection fails
    """
```

### **Class Methods**

#### **IntelligentMedicalExtractor.extract_specific_info()**
```python
def extract_specific_info(
    self, 
    documents: List[Document], 
    query: str
) -> Dict[str, Any]:
    """
    Extract specific information based on query type.
    
    Args:
        documents: List of Haystack Document objects
        query: Natural language query string
        
    Returns:
        Dictionary containing extracted information by category
    """
```

---

## 📊 **Performance Characteristics**

### **Processing Speed**
- **Document Loading**: ~100-500ms per case report (depending on size)
- **Query Processing**: ~200-1000ms per query (depending on complexity)
- **Pattern Matching**: ~50-200ms per document chunk
- **Answer Generation**: ~100-300ms per response

### **Memory Usage**
- **Base Memory**: ~50-100MB for system components
- **Per Case Report**: ~10-50MB depending on text size
- **Document Chunks**: ~5-20MB per chunk
- **Total Memory**: ~200-500MB for typical 9-case setup

### **Scalability Factors**
- **Linear Scaling**: Processing time scales linearly with case report count
- **Chunk Optimization**: Smaller chunks improve retrieval speed
- **Pattern Efficiency**: Regex complexity affects matching speed
- **Memory Management**: Document cleanup prevents memory bloat

---

## ⚠️ **Error Handling**

### **Common Error Types**

#### **1. File Loading Errors**
```python
try:
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
except UnicodeDecodeError:
    # Try next encoding in list
    continue
except FileNotFoundError:
    print(f"Error: Case report file not found: {file_path}")
    return None
```

#### **2. Pipeline Execution Errors**
```python
try:
    result = pipeline.run(pipeline_input)
    return result['generator']['answer']
except Exception as e:
    return f"Error processing query: {str(e)}"
```

#### **3. Pattern Matching Errors**
```python
try:
    matches = re.findall(pattern, content, re.IGNORECASE)
    # Process matches
except re.error as e:
    print(f"Invalid regex pattern: {pattern}")
    continue
```

### **Error Recovery Strategies**
- **Encoding Fallback**: Multiple encoding attempts
- **Pattern Validation**: Regex syntax checking
- **Graceful Degradation**: Partial results when possible
- **User Feedback**: Clear error messages and suggestions

---

## 🛠️ **Customization Guide**

### **Adding New Extraction Patterns**

#### **1. Define New Pattern Category**
```python
self.extraction_patterns['new_category'] = [
    r'pattern1([^.]*)',
    r'pattern2([^.]*)',
    r'pattern3([^.]*)'
]
```

#### **2. Add Extraction Method**
```python
def _extract_new_category(self, documents: List[Document]) -> List[str]:
    """Extract new category information"""
    results = []
    for doc in documents:
        content = doc.content
        for pattern in self.extraction_patterns['new_category']:
            matches = re.findall(pattern, content, re.IGNORECASE)
            results.extend([match.strip() for match in matches])
    return list(set(results))
```

#### **3. Update Main Extraction Logic**
```python
if any(term in query_lower for term in ['new_category', 'related_terms']):
    extracted_info['new_category'] = self._extract_new_category(documents)
```

#### **4. Add Formatting Method**
```python
def _format_new_category_answer(self, info: Dict[str, Any]) -> str:
    if 'new_category' in info and info['new_category']:
        return f"New Category found:\n" + "\n".join([f"• {item}" for item in info['new_category']])
    return "No new category information found."
```

### **Modifying Answer Formatting**

#### **Custom Output Formats**
```python
def _format_custom_answer(self, info: Dict[str, Any]) -> str:
    # Custom formatting logic
    if 'diagnoses' in info:
        return f"📋 Diagnoses:\n" + "\n".join([f"🏥 {diag}" for diag in info['diagnoses']])
    return "No diagnoses found."
```

#### **JSON Output**
```python
def _format_json_answer(self, info: Dict[str, Any]) -> str:
    return json.dumps(info, indent=2, ensure_ascii=False)
```

### **Performance Tuning**

#### **Retriever Optimization**
```python
# Adjust retrieval depth
retriever = MultiCaseMedicalRetriever(top_k=10)  # More comprehensive

# Custom medical term mapping
retriever.medical_terms.update({
    'custom_term': ['synonym1', 'synonym2', 'synonym3']
})
```

#### **Pattern Optimization**
```python
# Use compiled regex for better performance
import re
compiled_patterns = {
    'age': re.compile(r'(\d+)-year-old', re.IGNORECASE),
    'diagnosis': re.compile(r'diagnosis[:\s]+([^.]+)', re.IGNORECASE)
}
```

---

## 🔍 **Debugging and Testing**

### **Debug Mode**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
print(f"Processing document: {doc.meta.get('case_name', 'Unknown')}")
print(f"Pattern matches: {matches}")
```

### **Pattern Testing**
```python
# Test individual patterns
def test_pattern(pattern: str, test_text: str):
    matches = re.findall(pattern, test_text, re.IGNORECASE)
    print(f"Pattern: {pattern}")
    print(f"Test text: {test_text}")
    print(f"Matches: {matches}")
    print("-" * 40)
```

### **Performance Profiling**
```python
import time
import cProfile

def profile_function(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    profiler.disable()
    profiler.print_stats(sort='cumulative')
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    return result
```

---

## 📈 **Future Enhancements**

### **Planned Features**
1. **Machine Learning Integration**: Neural pattern recognition
2. **Multi-Language Support**: International medical terminology
3. **Real-time Updates**: Live case report monitoring
4. **Advanced Analytics**: Statistical analysis and trends
5. **API Endpoints**: REST API for external integration

### **Architecture Improvements**
1. **Microservices**: Component-based deployment
2. **Caching Layer**: Redis-based result caching
3. **Async Processing**: Non-blocking query processing
4. **Distributed Processing**: Multi-node deployment support

---

## 📞 **Technical Support**

### **Getting Help**
- **Code Issues**: Check error logs and stack traces
- **Performance Problems**: Use profiling tools and monitoring
- **Pattern Problems**: Test regex patterns independently
- **Integration Issues**: Verify Haystack version compatibility

### **Development Resources**
- **Haystack Documentation**: https://docs.haystack.deepset.ai/
- **Python Regex**: https://docs.python.org/3/library/re.html
- **Medical NLP**: Healthcare AI and NLP communities
- **Performance Optimization**: Python profiling and optimization guides

---

*This technical documentation provides comprehensive information about the Intelligent Medical RAG System architecture, components, and customization options. For user-level information, refer to the README.md file.*
