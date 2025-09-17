#!/usr/bin/env python3
"""
Keyword-Based Medical Case Report Search System
Search for specific keywords in medical case reports
"""

import re
import json
import os
from typing import Dict, List, Any, Set
from haystack import Document
from multi_case_rag import load_multiple_case_reports

class KeywordSearcher:
    def __init__(self):
        # Medical keyword categories
        self.keyword_categories = {
            'demographics': [
                'age', 'old', 'year', 'male', 'female', 'man', 'woman', 'sex', 'gender'
            ],
            'diagnoses': [
                'diagnosis', 'condition', 'disease', 'cancer', 'carcinoma', 'failure', 
                'apnea', 'amyloidosis', 'diabetes', 'hypertension', 'fibrillation',
                'obstructive', 'sleep', 'heart', 'coronary', 'atrial', 'cardiac'
            ],
            'medications': [
                'medication', 'drug', 'medicine', 'propofol', 'remifentanil', 'rivaroxaban',
                'naproxen', 'vasopressor', 'drip', 'infusion', 'injection', 'mg', 'mcg', 'ml'
            ],
            'procedures': [
                'procedure', 'surgery', 'operation', 'intervention', 'performed', 'underwent',
                'placed', 'PCI', 'ablation', 'intubation', 'catheter', 'endotracheal'
            ],
            'complications': [
                'complication', 'problem', 'issue', 'hypotension', 'fibrillation', 'pressure',
                'drop', 'tachycardic', 'bradycardic', 'arrhythmia'
            ],
            'outcomes': [
                'outcome', 'result', 'discharge', 'died', 'survived', 'recovered', 'improved',
                'transferred', 'ICU', 'SICU', 'ward'
            ],
            'vital_signs': [
                'blood pressure', 'heart rate', 'HR', 'BP', 'ABP', 'bpm', 'mm Hg', 'oxygen',
                'saturation', 'temperature', 'pulse', 'respiratory rate'
            ],
            'lab_values': [
                'lab', 'laboratory', 'blood', 'test', 'result', 'value', 'level', 'count',
                'hemoglobin', 'hematocrit', 'glucose', 'creatinine', 'BUN'
            ]
        }
        
        # Common medical terms that might appear in case reports
        self.medical_terms = [
            'anesthesia', 'sedation', 'ventilation', 'respiratory', 'cardiac', 'pulmonary',
            'neurological', 'gastrointestinal', 'renal', 'hepatic', 'endocrine', 'hematologic',
            'oncology', 'surgery', 'postoperative', 'preoperative', 'intraoperative'
        ]
    
    def search_keywords(self, documents: List[Document], keywords: List[str], 
                       case_sensitive: bool = False, exact_match: bool = False) -> Dict[str, Any]:
        """
        Search for keywords in case reports
        
        Args:
            documents: List of Haystack Document objects
            keywords: List of keywords to search for
            case_sensitive: Whether search should be case sensitive
            exact_match: Whether to match exact words only
            
        Returns:
            Dictionary with search results
        """
        results = {
            'keywords_found': [],
            'keywords_not_found': [],
            'matches_by_case': {},
            'total_matches': 0,
            'case_reports_searched': len(documents)
        }
        
        # Prepare keywords for searching
        search_keywords = []
        for keyword in keywords:
            if case_sensitive:
                search_keywords.append(keyword)
            else:
                search_keywords.append(keyword.lower())
        
        # Search through each document
        for doc in documents:
            case_name = doc.meta.get('case_name', 'Unknown Case')
            content = doc.content
            
            if not case_sensitive:
                content = content.lower()
            
            case_matches = {
                'case_name': case_name,
                'matches': [],
                'match_count': 0
            }
            
            # Search for each keyword
            for i, keyword in enumerate(search_keywords):
                original_keyword = keywords[i]  # Keep original case for display
                
                if exact_match:
                    # Search for exact word boundaries
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    matches = re.findall(pattern, content)
                else:
                    # Search for keyword anywhere in text
                    matches = re.findall(re.escape(keyword), content)
                
                if matches:
                    match_count = len(matches)
                    case_matches['matches'].append({
                        'keyword': original_keyword,
                        'count': match_count,
                        'context': self._get_keyword_context(content, keyword, original_keyword)
                    })
                    case_matches['match_count'] += match_count
                    
                    if original_keyword not in results['keywords_found']:
                        results['keywords_found'].append(original_keyword)
                else:
                    if original_keyword not in results['keywords_not_found']:
                        results['keywords_not_found'].append(original_keyword)
            
            if case_matches['matches']:
                results['matches_by_case'][case_name] = case_matches
                results['total_matches'] += case_matches['match_count']
        
        return results
    
    def _get_keyword_context(self, content: str, keyword: str, original_keyword: str, 
                           context_length: int = 50) -> List[str]:
        """Get context around keyword matches"""
        contexts = []
        pattern = re.escape(keyword)
        
        for match in re.finditer(pattern, content):
            start = max(0, match.start() - context_length)
            end = min(len(content), match.end() + context_length)
            context = content[start:end]
            contexts.append(context.strip())
        
        return contexts[:3]  # Return first 3 contexts
    
    def search_by_category(self, documents: List[Document], category: str) -> Dict[str, Any]:
        """Search for keywords in a specific category"""
        if category not in self.keyword_categories:
            return {'error': f'Category "{category}" not found. Available categories: {list(self.keyword_categories.keys())}'}
        
        keywords = self.keyword_categories[category]
        return self.search_keywords(documents, keywords)
    
    def get_available_categories(self) -> List[str]:
        """Get list of available keyword categories"""
        return list(self.keyword_categories.keys())
    
    def get_category_keywords(self, category: str) -> List[str]:
        """Get keywords for a specific category"""
        return self.keyword_categories.get(category, [])

def format_keyword_results(results: Dict[str, Any]) -> str:
    """Format keyword search results for display"""
    if 'error' in results:
        return f"❌ {results['error']}"
    
    output = []
    output.append("🔍 Keyword Search Results")
    output.append("=" * 50)
    
    # Summary
    output.append(f"📊 Summary:")
    output.append(f"   • Keywords found: {len(results['keywords_found'])}")
    output.append(f"   • Keywords not found: {len(results['keywords_not_found'])}")
    output.append(f"   • Total matches: {results['total_matches']}")
    output.append(f"   • Case reports searched: {results['case_reports_searched']}")
    output.append("")
    
    # Keywords found
    if results['keywords_found']:
        output.append("✅ Keywords Found:")
        for keyword in results['keywords_found']:
            output.append(f"   • {keyword}")
        output.append("")
    
    # Keywords not found
    if results['keywords_not_found']:
        output.append("❌ Keywords Not Found:")
        for keyword in results['keywords_not_found']:
            output.append(f"   • {keyword}")
        output.append("")
    
    # Matches by case
    if results['matches_by_case']:
        output.append("📋 Matches by Case Report:")
        for case_name, case_data in results['matches_by_case'].items():
            output.append(f"\n🏥 {case_name} ({case_data['match_count']} matches):")
            for match in case_data['matches']:
                output.append(f"   • '{match['keyword']}' found {match['count']} time(s)")
                if match['context']:
                    output.append(f"     Context: ...{match['context'][0]}...")
    
    return "\n".join(output)

def main():
    """Main function for keyword search"""
    print("🔍 Keyword-Based Medical Case Report Search")
    print("=" * 50)
    
    # Load configuration
    config_file = "case_reports_config.json"
    
    if not os.path.exists(config_file):
        print("❌ No case reports configured.")
        return
    
    with open(config_file, 'r') as f:
        case_reports_config = json.load(f)
    
    # Load case reports
    print("📋 Loading case reports...")
    documents = load_multiple_case_reports(case_reports_config)
    
    if not documents:
        print("❌ Could not load any case reports.")
        return
    
    print(f"✅ Loaded {len(documents)} case reports")
    
    # Create searcher
    searcher = KeywordSearcher()
    
    while True:
        print("\n" + "=" * 50)
        print("🔍 Keyword Search Options:")
        print("1. Search specific keywords")
        print("2. Search by category")
        print("3. Show available categories")
        print("4. Show category keywords")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            # Search specific keywords
            keywords_input = input("Enter keywords to search (comma-separated): ").strip()
            if keywords_input:
                keywords = [k.strip() for k in keywords_input.split(',')]
                
                case_sensitive = input("Case sensitive search? (y/n): ").strip().lower() == 'y'
                exact_match = input("Exact word match only? (y/n): ").strip().lower() == 'y'
                
                print(f"\n🔍 Searching for: {', '.join(keywords)}")
                results = searcher.search_keywords(documents, keywords, case_sensitive, exact_match)
                print(format_keyword_results(results))
        
        elif choice == '2':
            # Search by category
            print(f"\nAvailable categories: {', '.join(searcher.get_available_categories())}")
            category = input("Enter category name: ").strip()
            
            if category in searcher.get_available_categories():
                print(f"\n🔍 Searching category: {category}")
                results = searcher.search_by_category(documents, category)
                print(format_keyword_results(results))
            else:
                print(f"❌ Category '{category}' not found.")
        
        elif choice == '3':
            # Show available categories
            print("\n📋 Available Categories:")
            for i, category in enumerate(searcher.get_available_categories(), 1):
                print(f"   {i}. {category}")
        
        elif choice == '4':
            # Show category keywords
            print(f"\nAvailable categories: {', '.join(searcher.get_available_categories())}")
            category = input("Enter category name: ").strip()
            
            if category in searcher.get_available_categories():
                keywords = searcher.get_category_keywords(category)
                print(f"\n🔑 Keywords in '{category}' category:")
                for keyword in keywords:
                    print(f"   • {keyword}")
            else:
                print(f"❌ Category '{category}' not found.")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
