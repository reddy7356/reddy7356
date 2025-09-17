#!/usr/bin/env python3
"""
Intelligent Medical Information Extractor
Provides specific, structured answers to medical questions
"""

import re
import json
import os
from typing import Dict, List, Any
from haystack import Document, Pipeline
from haystack.core.component import component
from multi_case_rag import load_multiple_case_reports

class IntelligentMedicalExtractor:
    def __init__(self):
        # Medical information extraction patterns
        self.extraction_patterns = {
            'age': [
                r'(\d+)-year-old',
                r'(\d+)\s*year[s]?\s*old',
                r'age[:\s]+(\d+)',
                r'(\d+)\s*years?\s*of\s*age',
                r'in\s*his\s*(\d+)s',
                r'in\s*her\s*(\d+)s',
                r'(\d+)-year-old\s*(male|female|man|woman)',
                r'(\d+)\s*year[s]?\s*old\s*(male|female|man|woman)'
            ],
            'sex': [
                r'(male|female|man|woman)',
                r'(\d+)[-\s]year[s]?\s*old\s*(male|female|man|woman)'
            ],
            'diagnosis': [
                r'diagnosis[:\s]+([^.]+)',
                r'condition[:\s]+([^.]+)',
                r'history\s+of\s+([^.]+)',
                r'presented\s+with\s+([^.]+)',
                r'with\s+a\s+medical\s+history\s+of\s+([^.]+)',
                r'history\s+of\s+([^.]+?)(?:,|\.|and)',
                r'(\w+\s+\w+\s+\w+)\s+(cancer|carcinoma|disease|failure|apnea|amyloidosis)',
                r'(obstructive\s+sleep\s+apnea|obstructive\s+sleep\s+apnoea)',
                r'(heart\s+failure)',
                r'(coronary\s+artery\s+disease)',
                r'(diabetes\s+mellitus)',
                r'(hypertension)',
                r'(atrial\s+fibrillation)'
            ],
            'medications': [
                r'(\w+)\s+(\d+)\s*(mg|mcg|ml|units?)\s*(IV|PO|IM|SC)',
                r'(\w+)\s+(\d+)\s*(mg|mcg|ml|units?)',
                r'(\w+)\s+(drip|infusion|injection)',
                r'(\w+)\s+(\d+)\s*(mg|mcg|ml|units?)/\s*(kg|min|hour)',
                r'(propofol|remifentanil|rivaroxaban|naproxen|vasopressor)\s+(drip|infusion|injection|mg|mcg)',
                r'(\w+)\s+(\d+)\s*(mg|mcg|ml|units?)',
                r'(\w+)\s+(drip)'
            ],
            'procedures': [
                r'(surgery|operation|procedure|intervention)[:\s]+([^.]+)',
                r'performed\s+([^.]+)',
                r'underwent\s+([^.]+)',
                r'placed\s+([^.]+)'
            ],
            'complications': [
                r'complication[:\s]+([^.]+)',
                r'developed\s+([^.]+)',
                r'experienced\s+([^.]+)',
                r'occurred[:\s]+([^.]+)'
            ],
            'outcomes': [
                r'outcome[:\s]+([^.]+)',
                r'result[:\s]+([^.]+)',
                r'discharged\s+([^.]+)',
                r'died|survived|recovered'
            ]
        }
    
    def extract_specific_info(self, documents: List[Document], query: str) -> Dict[str, Any]:
        """Extract specific information based on the query"""
        query_lower = query.lower()
        extracted_info = {}
        
        # Extract patient demographics
        if any(term in query_lower for term in ['age', 'old', 'year']):
            extracted_info['ages'] = self._extract_ages(documents)
        
        if any(term in query_lower for term in ['sex', 'gender', 'male', 'female']):
            extracted_info['sex'] = self._extract_sex(documents)
        
        if any(term in query_lower for term in ['diagnosis', 'diagnoses', 'condition', 'disease', 'diseases']):
            extracted_info['diagnoses'] = self._extract_diagnoses(documents)
        
        if any(term in query_lower for term in ['medication', 'drug', 'medicine']):
            extracted_info['medications'] = self._extract_medications(documents)
        
        if any(term in query_lower for term in ['procedure', 'surgery', 'operation']):
            extracted_info['procedures'] = self._extract_procedures(documents)
        
        if any(term in query_lower for term in ['complication', 'problem', 'issue']):
            extracted_info['complications'] = self._extract_complications(documents)
        
        if any(term in query_lower for term in ['outcome', 'result', 'discharge']):
            extracted_info['outcomes'] = self._extract_outcomes(documents)
        
        return extracted_info
    
    def _extract_ages(self, documents: List[Document]) -> List[str]:
        """Extract specific patient ages"""
        ages = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['age']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        # Handle patterns with multiple groups
                        if 'in his' in pattern or 'in her' in pattern:
                            # Format: "in his 70s" -> "70s"
                            ages.append(f"{match[0]}s")
                        elif len(match) >= 2 and any(term in str(match[1]).lower() for term in ['male', 'female', 'man', 'woman']):
                            # Format: "74-year-old woman" -> "74-year-old woman"
                            ages.append(f"{match[0]}-year-old {match[1]}")
                        else:
                            ages.append(" ".join(match))
                    else:
                        ages.append(match)
        return list(set(ages))
    
    def _extract_sex(self, documents: List[Document]) -> List[str]:
        """Extract patient sex/gender"""
        sexes = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['sex']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                sexes.extend(matches)
        return list(set(sexes))
    
    def _extract_diagnoses(self, documents: List[Document]) -> List[str]:
        """Extract specific diagnoses"""
        diagnoses = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['diagnosis']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        # Handle patterns with multiple groups
                        if len(match) >= 2:
                            # Format: "infiltrating ductal carcinoma" + "cancer"
                            diagnoses.append(f"{match[0]} {match[1]}")
                        else:
                            diagnoses.append(match[0])
                    else:
                        diagnoses.append(match.strip())
        return list(set(diagnoses))
    
    def _extract_medications(self, documents: List[Document]) -> List[str]:
        """Extract specific medications with dosages"""
        medications = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['medications']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        if len(match) >= 2:
                            med_info = f"{match[0]} {match[1]}"
                            if len(match) > 2 and match[2]:
                                med_info += f" {match[2]}"
                            medications.append(med_info.strip())
                    else:
                        medications.append(match.strip())
        return list(set(medications))
    
    def _extract_procedures(self, documents: List[Document]) -> List[str]:
        """Extract specific procedures"""
        procedures = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['procedures']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        procedures.extend([m.strip() for m in match if m])
                    else:
                        procedures.append(match.strip())
        return list(set(procedures))
    
    def _extract_complications(self, documents: List[Document]) -> List[str]:
        """Extract specific complications"""
        complications = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['complications']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                complications.extend([match.strip() for match in matches])
        return list(set(complications))
    
    def _extract_outcomes(self, documents: List[Document]) -> List[str]:
        """Extract specific outcomes"""
        outcomes = []
        for doc in documents:
            content = doc.content
            for pattern in self.extraction_patterns['outcomes']:
                matches = re.findall(pattern, content, re.IGNORECASE)
                outcomes.extend([match.strip() for match in matches])
        return list(set(outcomes))

@component
class SpecificAnswerGenerator:
    def __init__(self):
        self.extractor = IntelligentMedicalExtractor()
    
    @component.output_types(answer=str)
    def run(self, query: str, documents: List[Document]):
        """Generate specific, structured answers"""
        if not documents:
            return {"answer": f"No relevant documents found for query: {query}"}
        
        # Extract specific information
        extracted_info = self.extractor.extract_specific_info(documents, query)
        
        # Generate structured answer
        query_lower = query.lower()
        
        if any(term in query_lower for term in ['age', 'old', 'year']):
            answer = self._format_age_answer(extracted_info)
        elif any(term in query_lower for term in ['sex', 'gender', 'male', 'female']):
            answer = self._format_sex_answer(extracted_info)
        elif any(term in query_lower for term in ['diagnosis', 'diagnoses', 'condition', 'disease', 'diseases']):
            answer = self._format_diagnosis_answer(extracted_info)
        elif any(term in query_lower for term in ['medication', 'drug', 'medicine']):
            answer = self._format_medication_answer(extracted_info)
        elif any(term in query_lower for term in ['procedure', 'surgery', 'operation']):
            answer = self._format_procedure_answer(extracted_info)
        elif any(term in query_lower for term in ['complication', 'problem', 'issue']):
            answer = self._format_complication_answer(extracted_info)
        elif any(term in query_lower for term in ['outcome', 'result', 'discharge']):
            answer = self._format_outcome_answer(extracted_info)
        else:
            answer = self._format_general_answer(extracted_info, query)
        
        return {"answer": answer}
    
    def _format_age_answer(self, info: Dict[str, Any]) -> str:
        if 'ages' in info and info['ages']:
            return f"Patient ages found:\n" + "\n".join([f"• {age}" for age in info['ages']])
        return "No specific age information found in the case reports."
    
    def _format_sex_answer(self, info: Dict[str, Any]) -> str:
        if 'sex' in info and info['sex']:
            return f"Patient sex/gender:\n" + "\n".join([f"• {sex}" for sex in info['sex']])
        return "No specific sex/gender information found in the case reports."
    
    def _format_diagnosis_answer(self, info: Dict[str, Any]) -> str:
        if 'diagnoses' in info and info['diagnoses']:
            # Clean up and filter diagnoses
            clean_diagnoses = []
            for diag in info['diagnoses']:
                # Filter out very long text chunks and focus on key medical terms
                if len(diag) < 80 and any(keyword in diag.lower() for keyword in [
                    'cancer', 'carcinoma', 'disease', 'failure', 'apnea', 'amyloidosis', 
                    'diabetes', 'hypertension', 'fibrillation', 'obstructive', 'heart',
                    'coronary', 'atrial', 'sleep', 'obstructive', 'cardiac'
                ]):
                    clean_diagnoses.append(diag)
            
            if clean_diagnoses:
                return f"Key Diagnoses found:\n" + "\n".join([f"• {diag}" for diag in clean_diagnoses[:8]])
            else:
                return f"Diagnoses found (showing first 5):\n" + "\n".join([f"• {diag[:60]}..." for diag in info['diagnoses'][:5]])
        return "No specific diagnosis information found in the case reports."
    
    def _format_medication_answer(self, info: Dict[str, Any]) -> str:
        if 'medications' in info and info['medications']:
            return f"Medications found:\n" + "\n".join([f"• {med}" for med in info['medications']])
        return "No specific medication information found in the case reports."
    
    def _format_procedure_answer(self, info: Dict[str, Any]) -> str:
        if 'procedures' in info and info['procedures']:
            return f"Procedures found:\n" + "\n".join([f"• {proc}" for proc in info['procedures']])
        return "No specific procedure information found in the case reports."
    
    def _format_complication_answer(self, info: Dict[str, Any]) -> str:
        if 'complications' in info and info['complications']:
            return f"Complications found:\n" + "\n".join([f"• {comp}" for comp in info['complications']])
        return "No specific complication information found in the case reports."
    
    def _format_outcome_answer(self, info: Dict[str, Any]) -> str:
        if 'outcomes' in info and info['outcomes']:
            return f"Outcomes found:\n" + "\n".join([f"• {out}" for out in info['outcomes']])
        return "No specific outcome information found in the case reports."
    
    def _format_general_answer(self, info: Dict[str, Any], query: str) -> str:
        return f"Information found for '{query}':\n" + json.dumps(info, indent=2)

def create_intelligent_pipeline() -> Pipeline:
    """Create the intelligent medical pipeline"""
    from multi_case_rag import MultiCaseMedicalRetriever
    
    # Create components
    retriever = MultiCaseMedicalRetriever(top_k=5)
    generator = SpecificAnswerGenerator()
    
    # Create pipeline
    pipeline = Pipeline()
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("generator", generator)
    pipeline.connect("retriever.documents", "generator.documents")
    
    return pipeline

def query_with_intelligent_extraction(question: str, case_reports_config: Dict[str, str]) -> str:
    """Query with intelligent information extraction"""
    # Load case reports
    documents = load_multiple_case_reports(case_reports_config)
    
    if not documents:
        return "Error: Could not load any medical case reports."
    
    # Create pipeline
    pipeline = create_intelligent_pipeline()
    
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
    """Test the intelligent extraction system"""
    print("🧠 Intelligent Medical Information Extractor")
    print("="*50)
    
    # Load configuration
    config_file = "case_reports_config.json"
    
    if not os.path.exists(config_file):
        print("❌ No case reports configured.")
        return
    
    with open(config_file, 'r') as f:
        case_reports_config = json.load(f)
    
    # Test questions
    test_questions = [
        "What are the patient ages?",
        "What is the patient sex/gender?",
        "What medications were used?",
        "What procedures were performed?",
        "What complications occurred?",
        "What are the diagnoses?"
    ]
    
    print("\n🧪 Testing intelligent extraction:")
    print("-" * 60)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        answer = query_with_intelligent_extraction(question, case_reports_config)
        print(f"💡 Answer:\n{answer}")
        print("-" * 40)

if __name__ == "__main__":
    main()
