#!/usr/bin/env python3
"""
MIMIC IV Patient Query System
Advanced keyword search and retrieval system for 200 MIMIC IV patients
"""

import os
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from collections import defaultdict, Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PatientInfo:
    """Patient information structure"""
    patient_id: str
    file_path: str
    content: str
    metadata: Dict[str, Any]
    keywords: List[str]
    medical_terms: Dict[str, List[str]]

@dataclass
class SearchResult:
    """Search result structure"""
    patient_id: str
    relevance_score: float
    matched_sections: List[str]
    matched_keywords: List[str]
    context: str
    metadata: Dict[str, Any]

class MIMICPatientIndexer:
    """Indexes and manages MIMIC IV patient data"""
    
    def __init__(self, patient_data_dir: str = "patient_txt_200"):
        self.patient_data_dir = Path(patient_data_dir)
        self.patients: Dict[str, PatientInfo] = {}
        self.keyword_index: Dict[str, List[str]] = defaultdict(list)
        self.medical_term_index: Dict[str, List[str]] = defaultdict(list)
        self.patient_metadata: Dict[str, Dict] = {}
        
        # Medical terminology categories
        self.medical_categories = {
            'diagnoses': [
                'coronary artery disease', 'cad', 'myocardial infarction', 'mi', 'heart attack',
                'aortic stenosis', 'hypertension', 'diabetes', 'diabetes mellitus', 'dm',
                'pneumonia', 'sepsis', 'stroke', 'cva', 'cerebrovascular accident',
                'cancer', 'carcinoma', 'tumor', 'metastasis', 'oncology',
                'kidney disease', 'renal failure', 'ckd', 'chronic kidney disease',
                'liver disease', 'hepatitis', 'cirrhosis', 'copd', 'asthma',
                'depression', 'anxiety', 'bipolar', 'schizophrenia', 'dementia'
            ],
            'procedures': [
                'surgery', 'operation', 'procedure', 'cath', 'catheterization',
                'cabg', 'coronary artery bypass', 'stent', 'angioplasty',
                'valve replacement', 'avr', 'mvr', 'pacemaker', 'defibrillator',
                'biopsy', 'endoscopy', 'colonoscopy', 'mri', 'ct scan',
                'ultrasound', 'echo', 'echocardiogram', 'stress test'
            ],
            'medications': [
                'aspirin', 'asa', 'warfarin', 'coumadin', 'heparin', 'plavix',
                'clopidogrel', 'metoprolol', 'atenolol', 'lisinopril', 'amlodipine',
                'simvastatin', 'atorvastatin', 'insulin', 'metformin', 'furosemide',
                'lasix', 'digoxin', 'nitroglycerin', 'morphine', 'fentanyl',
                'propofol', 'midazolam', 'vancomycin', 'ceftriaxone', 'levofloxacin'
            ],
            'vitals': [
                'blood pressure', 'bp', 'heart rate', 'hr', 'temperature', 'temp',
                'oxygen saturation', 'o2 sat', 'respiratory rate', 'rr',
                'weight', 'height', 'bmi', 'body mass index'
            ],
            'lab_values': [
                'hemoglobin', 'hgb', 'hematocrit', 'hct', 'white blood cell', 'wbc',
                'platelet', 'plt', 'creatinine', 'bun', 'glucose', 'sodium', 'na',
                'potassium', 'k', 'chloride', 'cl', 'troponin', 'bnp', 'ck-mb'
            ],
            'symptoms': [
                'chest pain', 'angina', 'shortness of breath', 'dyspnea', 'sob',
                'fatigue', 'weakness', 'nausea', 'vomiting', 'diarrhea', 'constipation',
                'headache', 'dizziness', 'syncope', 'confusion', 'altered mental status',
                'fever', 'chills', 'sweating', 'palpitations', 'edema', 'swelling'
            ]
        }
        
    def load_all_patients(self) -> None:
        """Load all patient files and create indexes"""
        logger.info(f"Loading patients from {self.patient_data_dir}")
        
        if not self.patient_data_dir.exists():
            raise FileNotFoundError(f"Patient data directory not found: {self.patient_data_dir}")
        
        patient_files = list(self.patient_data_dir.glob("*.txt"))
        logger.info(f"Found {len(patient_files)} patient files")
        
        for file_path in patient_files:
            try:
                patient_id = file_path.stem
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract metadata from content
                metadata = self._extract_metadata(content, patient_id)
                
                # Extract keywords and medical terms
                keywords = self._extract_keywords(content)
                medical_terms = self._extract_medical_terms(content)
                
                # Create patient info
                patient_info = PatientInfo(
                    patient_id=patient_id,
                    file_path=str(file_path),
                    content=content,
                    metadata=metadata,
                    keywords=keywords,
                    medical_terms=medical_terms
                )
                
                self.patients[patient_id] = patient_info
                
                # Update indexes
                for keyword in keywords:
                    self.keyword_index[keyword.lower()].append(patient_id)
                
                for category, terms in medical_terms.items():
                    for term in terms:
                        self.medical_term_index[term.lower()].append(patient_id)
                
                self.patient_metadata[patient_id] = metadata
                
            except Exception as e:
                logger.error(f"Error loading patient {file_path}: {e}")
        
        logger.info(f"Successfully loaded {len(self.patients)} patients")
        logger.info(f"Created keyword index with {len(self.keyword_index)} unique keywords")
        logger.info(f"Created medical term index with {len(self.medical_term_index)} unique terms")
    
    def _extract_metadata(self, content: str, patient_id: str) -> Dict[str, Any]:
        """Extract metadata from patient content"""
        metadata = {
            'patient_id': patient_id,
            'sex': None,
            'age': None,
            'admission_date': None,
            'discharge_date': None,
            'service': None,
            'chief_complaint': None,
            'discharge_diagnosis': [],
            'allergies': [],
            'medications': [],
            'procedures': []
        }
        
        # Extract sex
        sex_match = re.search(r'Sex:\s*([MF])', content, re.IGNORECASE)
        if sex_match:
            metadata['sex'] = sex_match.group(1)
        
        # Extract service
        service_match = re.search(r'Service:\s*([^\n]+)', content, re.IGNORECASE)
        if service_match:
            metadata['service'] = service_match.group(1).strip()
        
        # Extract chief complaint
        complaint_match = re.search(r'Chief Complaint:\s*([^\n]+)', content, re.IGNORECASE)
        if complaint_match:
            metadata['chief_complaint'] = complaint_match.group(1).strip()
        
        # Extract discharge diagnosis
        diagnosis_section = re.search(r'Discharge Diagnosis:([\s\S]*?)(?=\n\n|\n[A-Z]|$)', content, re.IGNORECASE)
        if diagnosis_section:
            diagnoses = re.findall(r'[^\n]+', diagnosis_section.group(1))
            metadata['discharge_diagnosis'] = [d.strip() for d in diagnoses if d.strip()]
        
        # Extract allergies
        allergy_section = re.search(r'Allergies:\s*([^\n]+)', content, re.IGNORECASE)
        if allergy_section:
            allergies = allergy_section.group(1).strip()
            if allergies and 'no known allergies' not in allergies.lower():
                metadata['allergies'] = [allergies]
        
        return metadata
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract important keywords from content"""
        # Convert to lowercase for processing
        content_lower = content.lower()
        
        # Extract medical terms, medications, procedures, etc.
        keywords = set()
        
        # Add all medical category terms that appear in content
        for category, terms in self.medical_categories.items():
            for term in terms:
                if term.lower() in content_lower:
                    keywords.add(term)
        
        # Extract other important terms using regex patterns
        patterns = [
            r'\b\d+\s*(mg|mcg|ml|cc|units?)\b',  # Dosages
            r'\b\d+\s*(year|yr)s?\s*old\b',      # Age references
            r'\b\d+/\d+\b',                      # Ratios (like blood pressure)
            r'\b[A-Z]{2,}\b',                    # Acronyms
            r'\b\d+\.\d+\b',                     # Decimal numbers
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content_lower)
            keywords.update(matches)
        
        return list(keywords)
    
    def _extract_medical_terms(self, content: str) -> Dict[str, List[str]]:
        """Extract medical terms by category"""
        content_lower = content.lower()
        found_terms = {}
        
        for category, terms in self.medical_categories.items():
            found_terms[category] = []
            for term in terms:
                if term.lower() in content_lower:
                    found_terms[category].append(term)
        
        return found_terms

class MIMICPatientSearcher:
    """Advanced search functionality for MIMIC patients"""
    
    def __init__(self, indexer: MIMICPatientIndexer):
        self.indexer = indexer
    
    def search_patients(self, 
                       query: str, 
                       patient_ids: Optional[List[str]] = None,
                       categories: Optional[List[str]] = None,
                       max_results: int = 10) -> List[SearchResult]:
        """
        Search for patients based on query
        
        Args:
            query: Search query string
            patient_ids: Specific patient IDs to search (None for all)
            categories: Medical categories to focus on
            max_results: Maximum number of results to return
        """
        query_lower = query.lower()
        query_words = query_lower.split()
        
        results = []
        search_patients = patient_ids if patient_ids else list(self.indexer.patients.keys())
        
        for patient_id in search_patients:
            if patient_id not in self.indexer.patients:
                continue
                
            patient = self.indexer.patients[patient_id]
            relevance_score = self._calculate_relevance_score(query_lower, query_words, patient, categories)
            
            if relevance_score > 0:
                matched_sections = self._find_matched_sections(query_lower, patient.content)
                matched_keywords = self._find_matched_keywords(query_words, patient.keywords)
                context = self._extract_context(query_lower, patient.content)
                
                result = SearchResult(
                    patient_id=patient_id,
                    relevance_score=relevance_score,
                    matched_sections=matched_sections,
                    matched_keywords=matched_keywords,
                    context=context,
                    metadata=patient.metadata
                )
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:max_results]
    
    def _calculate_relevance_score(self, 
                                 query_lower: str, 
                                 query_words: List[str], 
                                 patient: PatientInfo,
                                 categories: Optional[List[str]]) -> float:
        """Calculate relevance score for a patient"""
        score = 0.0
        content_lower = patient.content.lower()
        
        # Exact phrase match (highest score)
        if query_lower in content_lower:
            score += 100
        
        # Individual word matches
        for word in query_words:
            if len(word) > 2:  # Ignore short words
                word_count = content_lower.count(word)
                score += word_count * 10
        
        # Medical category matches
        if categories:
            for category in categories:
                if category in patient.medical_terms:
                    score += len(patient.medical_terms[category]) * 5
        
        # Keyword matches
        for keyword in patient.keywords:
            if any(word in keyword.lower() for word in query_words):
                score += 3
        
        # Metadata matches
        for field, value in patient.metadata.items():
            if value and isinstance(value, str):
                if any(word in value.lower() for word in query_words):
                    score += 5
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and any(word in item.lower() for word in query_words):
                        score += 5
        
        return score
    
    def _find_matched_sections(self, query_lower: str, content: str) -> List[str]:
        """Find sections of content that match the query"""
        sections = []
        content_lower = content.lower()
        
        # Split content into sections
        content_sections = re.split(r'\n\n+', content)
        
        for section in content_sections:
            if query_lower in section.lower():
                # Truncate long sections
                if len(section) > 500:
                    section = section[:500] + "..."
                sections.append(section.strip())
        
        return sections[:3]  # Return top 3 matching sections
    
    def _find_matched_keywords(self, query_words: List[str], patient_keywords: List[str]) -> List[str]:
        """Find keywords that match the query"""
        matched = []
        for keyword in patient_keywords:
            if any(word in keyword.lower() for word in query_words):
                matched.append(keyword)
        return matched[:10]  # Return top 10 matches
    
    def _extract_context(self, query_lower: str, content: str) -> str:
        """Extract context around query matches"""
        content_lower = content.lower()
        if query_lower not in content_lower:
            return ""
        
        # Find the first occurrence
        start_pos = content_lower.find(query_lower)
        context_start = max(0, start_pos - 200)
        context_end = min(len(content), start_pos + len(query_lower) + 200)
        
        context = content[context_start:context_end]
        return context.strip()
    
    def get_patient_summary(self, patient_id: str) -> Dict[str, Any]:
        """Get comprehensive summary for a specific patient"""
        if patient_id not in self.indexer.patients:
            return {}
        
        patient = self.indexer.patients[patient_id]
        
        summary = {
            'patient_id': patient_id,
            'metadata': patient.metadata,
            'medical_conditions': patient.medical_terms.get('diagnoses', []),
            'procedures': patient.medical_terms.get('procedures', []),
            'medications': patient.medical_terms.get('medications', []),
            'key_keywords': patient.keywords[:20],  # Top 20 keywords
            'content_length': len(patient.content),
            'file_path': patient.file_path
        }
        
        return summary
    
    def get_patient_statistics(self) -> Dict[str, Any]:
        """Get statistics about the patient database"""
        stats = {
            'total_patients': len(self.indexer.patients),
            'total_keywords': len(self.indexer.keyword_index),
            'total_medical_terms': len(self.indexer.medical_term_index),
            'services': Counter(),
            'common_diagnoses': Counter(),
            'common_medications': Counter(),
            'common_procedures': Counter()
        }
        
        for patient in self.indexer.patients.values():
            # Service distribution
            if patient.metadata.get('service'):
                stats['services'][patient.metadata['service']] += 1
            
            # Common diagnoses
            for diagnosis in patient.medical_terms.get('diagnoses', []):
                stats['common_diagnoses'][diagnosis] += 1
            
            # Common medications
            for medication in patient.medical_terms.get('medications', []):
                stats['common_medications'][medication] += 1
            
            # Common procedures
            for procedure in patient.medical_terms.get('procedures', []):
                stats['common_procedures'][procedure] += 1
        
        return stats

class MIMICQueryInterface:
    """User interface for querying MIMIC patients"""
    
    def __init__(self, patient_data_dir: str = "patient_txt_200"):
        self.indexer = MIMICPatientIndexer(patient_data_dir)
        self.searcher = MIMICPatientSearcher(self.indexer)
        self._load_data()
    
    def _load_data(self):
        """Load patient data and create indexes"""
        logger.info("Loading MIMIC patient data...")
        self.indexer.load_all_patients()
        logger.info("Data loading complete!")
    
    def search(self, 
               query: str, 
               patient_ids: Optional[List[str]] = None,
               categories: Optional[List[str]] = None,
               max_results: int = 10) -> List[SearchResult]:
        """Search for patients"""
        return self.searcher.search_patients(query, patient_ids, categories, max_results)
    
    def get_patient_info(self, patient_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific patient"""
        return self.searcher.get_patient_summary(patient_id)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self.searcher.get_patient_statistics()
    
    def list_patients(self, limit: int = 20) -> List[str]:
        """List available patient IDs"""
        return list(self.indexer.patients.keys())[:limit]
    
    def interactive_search(self):
        """Interactive search interface"""
        print("🏥 MIMIC IV Patient Query System")
        print("=" * 50)
        print(f"Loaded {len(self.indexer.patients)} patients")
        print("\nAvailable commands:")
        print("- search <query> [patient_id1,patient_id2,...]")
        print("- patient <patient_id>")
        print("- stats")
        print("- list [limit]")
        print("- quit")
        print()
        
        while True:
            try:
                command = input("MIMIC> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                elif command.lower() == 'stats':
                    self._show_stats()
                elif command.lower().startswith('list'):
                    self._show_patient_list(command)
                elif command.lower().startswith('patient'):
                    self._show_patient_info(command)
                elif command.lower().startswith('search'):
                    self._perform_search(command)
                else:
                    print("Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("Goodbye!")
    
    def _show_stats(self):
        """Show database statistics"""
        stats = self.get_database_stats()
        print(f"\n📊 Database Statistics:")
        print(f"Total Patients: {stats['total_patients']}")
        print(f"Total Keywords: {stats['total_keywords']}")
        print(f"Total Medical Terms: {stats['total_medical_terms']}")
        
        print(f"\n🏥 Top Services:")
        for service, count in stats['services'].most_common(5):
            print(f"  {service}: {count}")
        
        print(f"\n🩺 Top Diagnoses:")
        for diagnosis, count in stats['common_diagnoses'].most_common(5):
            print(f"  {diagnosis}: {count}")
        
        print(f"\n💊 Top Medications:")
        for medication, count in stats['common_medications'].most_common(5):
            print(f"  {medication}: {count}")
        print()
    
    def _show_patient_list(self, command: str):
        """Show list of patients"""
        parts = command.split()
        limit = 20
        if len(parts) > 1:
            try:
                limit = int(parts[1])
            except ValueError:
                pass
        
        patients = self.list_patients(limit)
        print(f"\n👥 Patient List (showing {len(patients)} of {len(self.indexer.patients)}):")
        for i, patient_id in enumerate(patients, 1):
            print(f"  {i:3d}. {patient_id}")
        print()
    
    def _show_patient_info(self, command: str):
        """Show detailed patient information"""
        parts = command.split()
        if len(parts) < 2:
            print("Usage: patient <patient_id>")
            return
        
        patient_id = parts[1]
        info = self.get_patient_info(patient_id)
        
        if not info:
            print(f"Patient {patient_id} not found.")
            return
        
        print(f"\n👤 Patient {patient_id}:")
        print(f"Sex: {info['metadata'].get('sex', 'Unknown')}")
        print(f"Service: {info['metadata'].get('service', 'Unknown')}")
        print(f"Chief Complaint: {info['metadata'].get('chief_complaint', 'Unknown')}")
        
        if info['medical_conditions']:
            print(f"Medical Conditions: {', '.join(info['medical_conditions'][:5])}")
        
        if info['procedures']:
            print(f"Procedures: {', '.join(info['procedures'][:5])}")
        
        if info['medications']:
            print(f"Medications: {', '.join(info['medications'][:5])}")
        
        print(f"Content Length: {info['content_length']} characters")
        print()
    
    def _perform_search(self, command: str):
        """Perform search and display results"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print("Usage: search <query> [patient_id1,patient_id2,...]")
            return
        
        query = parts[1]
        patient_ids = None
        
        # Check if specific patient IDs are provided
        if ',' in query:
            query_parts = query.split(',')
            query = query_parts[0].strip()
            patient_ids = [pid.strip() for pid in query_parts[1:]]
        
        results = self.search(query, patient_ids, max_results=5)
        
        if not results:
            print(f"No results found for query: '{query}'")
            return
        
        print(f"\n🔍 Search Results for '{query}' ({len(results)} results):")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. Patient {result.patient_id} (Score: {result.relevance_score:.1f})")
            print(f"   Service: {result.metadata.get('service', 'Unknown')}")
            print(f"   Chief Complaint: {result.metadata.get('chief_complaint', 'Unknown')}")
            
            if result.matched_keywords:
                print(f"   Keywords: {', '.join(result.matched_keywords[:5])}")
            
            if result.context:
                context = result.context[:200] + "..." if len(result.context) > 200 else result.context
                print(f"   Context: {context}")
            print()

def main():
    """Main function"""
    try:
        interface = MIMICQueryInterface()
        interface.interactive_search()
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
