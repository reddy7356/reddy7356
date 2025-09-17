#!/usr/bin/env python3
"""
Multi-Case Medical RAG System
Handles multiple medical case reports for comprehensive analysis
"""

from haystack import Document, Pipeline
from haystack.core.component import component
from typing import List, Dict, Any
import os
import glob
import json

# Medical case report retriever component for multiple cases
@component
class MultiCaseMedicalRetriever:
    def __init__(self, top_k: int = 3):
        self.top_k = top_k
    
    @component.output_types(documents=List[Document])
    def run(self, query: str, documents: List[Document]):
        # Medical-specific keyword-based retrieval
        query_lower = query.lower()
        query_words = query_lower.split()
        scored_docs = []
        
        # Medical terminology mapping
        medical_terms = {
            'patient': ['patient', 'woman', 'woman', 'man', 'male', 'female', 'year-old'],
            'diagnosis': ['diagnosis', 'cancer', 'carcinoma', 'metastases', 'tumor', 'disease'],
            'treatment': ['treatment', 'chemotherapy', 'radiation', 'surgery', 'ablation', 'therapy'],
            'medication': ['medication', 'drug', 'propofol', 'remifentanil', 'lidocaine', 'medicine'],
            'complications': ['complications', 'respiratory', 'distress', 'ARDS', 'pneumonitis', 'problems'],
            'procedure': ['procedure', 'surgery', 'ablation', 'PBSS', 'screw', 'operation'],
            'vitals': ['vitals', 'blood pressure', 'heart rate', 'oxygen', 'temperature', 'pulse'],
            'lab': ['lab', 'blood', 'hemoglobin', 'oxygen', 'PaO2', 'test', 'results','OSA','obstructive sleep apnea','CHF','congestive heart failure']
        }
        
        for doc in documents:
            score = 0
            doc_lower = doc.content.lower()
            
            # Check for exact phrase match
            if query_lower in doc_lower:
                score += 15
            
            # Check for medical term matches
            for category, terms in medical_terms.items():
                if any(term in query_lower for term in terms):
                    if any(term in doc_lower for term in terms):
                        score += 8
            
            # Check for individual word matches
            for word in query_words:
                if len(word) > 2 and word in doc_lower:
                    score += 2
            
            # Special handling for medical queries
            if any(term in query_lower for term in ['age', 'old', 'year']):
                if any(term in doc_lower for term in ['year-old', 'years old', 'age']):
                    score += 10
            
            if any(term in query_lower for term in ['cancer', 'carcinoma', 'tumor']):
                if any(term in doc_lower for term in ['carcinoma', 'tumor', 'metastases', 'cancer']):
                    score += 10
            
            if any(term in query_lower for term in ['breast', 'mammary']):
                if 'breast' in doc_lower:
                    score += 10
            
            if any(term in query_lower for term in ['bone', 'sacral', 'sacroiliac']):
                if any(term in doc_lower for term in ['sacral', 'sacroiliac', 'bone']):
                    score += 10
            
            scored_docs.append((score, doc))
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [doc for score, doc in scored_docs[:self.top_k] if score > 0]
        
        # If no exact matches, return top documents anyway
        if not top_docs and documents:
            top_docs = [doc for score, doc in scored_docs[:self.top_k]]
        
        return {"documents": top_docs}

# Multi-case medical generator component
@component
class MultiCaseMedicalGenerator:
    def __init__(self):
        pass
    
    @component.output_types(answer=str)
    def run(self, query: str, documents: List[Document]):
        if not documents:
            return {"answer": f"I'm sorry, I couldn't find any relevant information about '{query}' in the medical case reports. Please try asking about patient conditions, treatments, complications, or specific medical details."}
        
        # Build context from retrieved documents
        context_parts = []
        case_sources = set()
        
        for i, doc in enumerate(documents, 1):
            case_name = doc.meta.get('case_name', 'Unknown Case')
            case_sources.add(case_name)
            context_parts.append(f"Document {i} (from {case_name}): {doc.content}")
        
        context = "\n\n".join(context_parts)
        
        # Enhanced medical prompt template for multiple cases
        prompt = f"""
Based on the following medical case reports, provide a clear and accurate answer to the question.

Context:
{context}

Question: {query}

Answer: """
        
        # Generate detailed medical-specific answer based on actual content
        query_lower = query.lower()
        
        # Check if we have multiple cases
        if len(case_sources) > 1:
            case_info = f"Based on information from {len(case_sources)} medical case reports:\n\n"
        else:
            case_info = f"Based on the medical case report:\n\n"
        
        if any(term in query_lower for term in ['age', 'old', 'year']):
            # Extract specific age information from documents
            age_info = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['year-old', 'years old', 'age']):
                    # Find the age information in the text
                    words = content.split()
                    for i, word in enumerate(words):
                        if any(term in word for term in ['year-old', 'years old']):
                            if i > 0 and words[i-1].isdigit():
                                age_info.append(f"{words[i-1]} {word}")
                            elif i < len(words)-1 and words[i+1].isdigit():
                                age_info.append(f"{words[i+1]} {word}")
            
            if age_info:
                answer = f"{case_info}Patient ages found:\n" + "\n".join([f"• {age}" for age in set(age_info)])
            else:
                answer = f"{case_info}Age information found in the case reports, but specific ages could not be extracted. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        elif any(term in query_lower for term in ['diagnosis', 'condition', 'cancer']):
            # Extract diagnosis information
            diagnoses = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['diagnosis', 'condition', 'cancer', 'carcinoma', 'disease']):
                    diagnoses.append(doc.content[:200] + "...")
            
            if diagnoses:
                answer = f"{case_info}Diagnoses found:\n\n" + "\n\n".join([f"• {diag}" for diag in diagnoses[:3]])
            else:
                answer = f"{case_info}Diagnosis information found. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        elif any(term in query_lower for term in ['treatment', 'therapy']):
            # Extract treatment information
            treatments = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['treatment', 'therapy', 'surgery', 'medication']):
                    treatments.append(doc.content[:200] + "...")
            
            if treatments:
                answer = f"{case_info}Treatments found:\n\n" + "\n\n".join([f"• {treat}" for treat in treatments[:3]])
            else:
                answer = f"{case_info}Treatment information found. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        elif any(term in query_lower for term in ['complications', 'problems', 'issues']):
            # Extract complication information
            complications = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['complication', 'problem', 'issue', 'distress', 'failure']):
                    complications.append(doc.content[:200] + "...")
            
            if complications:
                answer = f"{case_info}Complications found:\n\n" + "\n\n".join([f"• {comp}" for comp in complications[:3]])
            else:
                answer = f"{case_info}Complication information found. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        elif any(term in query_lower for term in ['medication', 'drug', 'anesthesia']):
            # Extract medication information
            medications = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['medication', 'drug', 'anesthesia', 'mg', 'iv']):
                    medications.append(doc.content[:200] + "...")
            
            if medications:
                answer = f"{case_info}Medications found:\n\n" + "\n\n".join([f"• {med}" for med in medications[:3]])
            else:
                answer = f"{case_info}Medication information found. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        elif any(term in query_lower for term in ['procedure', 'surgery']):
            # Extract procedure information
            procedures = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['procedure', 'surgery', 'operation', 'intervention']):
                    procedures.append(doc.content[:200] + "...")
            
            if procedures:
                answer = f"{case_info}Procedures found:\n\n" + "\n\n".join([f"• {proc}" for proc in procedures[:3]])
            else:
                answer = f"{case_info}Procedure information found. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        elif any(term in query_lower for term in ['outcome', 'result', 'discharge']):
            # Extract outcome information
            outcomes = []
            for doc in documents:
                content = doc.content.lower()
                if any(term in content for term in ['outcome', 'result', 'discharge', 'died', 'survived']):
                    outcomes.append(doc.content[:200] + "...")
            
            if outcomes:
                answer = f"{case_info}Outcomes found:\n\n" + "\n\n".join([f"• {out}" for out in outcomes[:3]])
            else:
                answer = f"{case_info}Outcome information found. Here's the relevant content:\n\n{documents[0].content[:300]}..."
        
        else:
            # For other queries, provide actual content
            answer = f"{case_info}Here's what I found regarding '{query}':\n\n{documents[0].content[:300]}..."
        
        return {"answer": answer}

def load_medical_case_report(file_path: str, case_name: str = None) -> List[Document]:
    """Load medical case report from file and convert to Haystack documents"""
    if case_name is None:
        case_name = os.path.basename(file_path).replace('.txt', '').replace('.TXT', '')
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
            
            # Split content into smaller chunks for better retrieval
            paragraphs = content.split('\n\n')
            documents = []
            
            for i, paragraph in enumerate(paragraphs):
                if paragraph.strip():
                    doc = Document(
                        content=paragraph.strip(),
                        meta={
                            'paragraph_id': i, 
                            'source': 'medical_case_report',
                            'case_name': case_name,
                            'file_path': file_path
                        }
                    )
                    documents.append(doc)
            
            print(f"✅ Loaded {len(documents)} document chunks from {case_name} using {encoding} encoding")
            return documents
        
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"❌ Error: File not found at {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error loading {case_name} with {encoding} encoding: {e}")
            continue
    
    print(f"❌ Error: Could not read {case_name} with any of the attempted encodings: {encodings}")
    return []

def load_multiple_case_reports(case_reports_config: Dict[str, str]) -> List[Document]:
    """Load multiple medical case reports"""
    all_documents = []
    
    for case_name, file_path in case_reports_config.items():
        print(f"📋 Loading case report: {case_name}")
        documents = load_medical_case_report(file_path, case_name)
        all_documents.extend(documents)
    
    print(f"✅ Total documents loaded: {len(all_documents)}")
    return all_documents

def create_multi_case_pipeline() -> Pipeline:
    """Create the multi-case medical RAG pipeline"""
    # Create components
    retriever = MultiCaseMedicalRetriever(top_k=5)  # Increased top_k for multiple cases
    generator = MultiCaseMedicalGenerator()
    
    # Create pipeline
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("generator", generator)
    
    # Connect components
    pipeline.connect("retriever.documents", "generator.documents")
    
    return pipeline

def query_multiple_cases(question: str, case_reports_config: Dict[str, str]) -> str:
    """Query multiple medical case reports"""
    # Load all case reports
    documents = load_multiple_case_reports(case_reports_config)
    
    if not documents:
        return "Error: Could not load any medical case reports."
    
    # Create pipeline
    pipeline = create_multi_case_pipeline()
    
    # Run query
    try:
        result = pipeline.run({
            "retriever": {
                "query": question,
                "documents": documents
            },
            "generator": {
                "query": question
            }
        })
        return result['generator']['answer']
    except Exception as e:
        return f"Error processing query: {str(e)}"

def main():
    """Main function to demonstrate multi-case RAG system"""
    print("🏥 Multi-Case Medical RAG System")
    print("="*50)
    
    # Load configuration from file
    config_file = "case_reports_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            case_reports_config = json.load(f)
        print(f"📋 Loaded configuration from {config_file}")
    else:
        # Default configuration if no config file exists
        case_reports_config = {
            "Case Trial 1": "/Users/saiofocalallc/clinical insight bot/Case Trial.txt",
        }
        print("📋 Using default configuration (no config file found)")
        print("💡 Run 'python add_case_report.py' to add more case reports")
    
    # Check which case reports exist
    existing_cases = {}
    for case_name, file_path in case_reports_config.items():
        if os.path.exists(file_path):
            existing_cases[case_name] = file_path
        else:
            print(f"⚠️  Warning: Case report not found: {file_path}")
    
    if not existing_cases:
        print("❌ No case reports found. Please check the file paths in case_reports_config.")
        return
    
    print(f"📋 Found {len(existing_cases)} case report(s):")
    for case_name in existing_cases.keys():
        print(f"   • {case_name}")
    
    # Test questions
    test_questions = [
        "What types of complications are mentioned across the cases?",
        "What treatments were used in the cases?",
        "What are the common patient demographics?",
        "What procedures were performed?",
        "What were the outcomes of the cases?"
    ]
    
    print("\n🧪 Testing multi-case RAG pipeline:")
    print("-" * 60)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        answer = query_multiple_cases(question, existing_cases)
        print(f"💡 Answer: {answer}")
    
    print("\n✅ Multi-case medical RAG system is ready!")
    print("\n📝 To add more case reports:")
    print("1. Run: python add_case_report.py")
    print("2. Follow the prompts to add your case report")
    print("3. Run this script again to query all case reports")

if __name__ == "__main__":
    main()
