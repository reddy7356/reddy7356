#!/usr/bin/env python3
"""
Simple Command-Line Keyword Search
Quick keyword search without interactive menu
"""

import sys
import json
import os
from keyword_search import KeywordSearcher, format_keyword_results
from multi_case_rag import load_multiple_case_reports

def search_keywords_command(keywords_str: str, case_sensitive: bool = False, exact_match: bool = False):
    """Search for keywords using command line arguments"""
    
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
    
    # Parse keywords
    keywords = [k.strip() for k in keywords_str.split(',')]
    
    # Create searcher and search
    searcher = KeywordSearcher()
    print(f"\n🔍 Searching for: {', '.join(keywords)}")
    results = searcher.search_keywords(documents, keywords, case_sensitive, exact_match)
    print(format_keyword_results(results))

def search_category_command(category: str):
    """Search by category using command line arguments"""
    
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
    
    # Create searcher and search
    searcher = KeywordSearcher()
    print(f"\n🔍 Searching category: {category}")
    results = searcher.search_by_category(documents, category)
    print(format_keyword_results(results))

def show_categories():
    """Show available categories"""
    searcher = KeywordSearcher()
    categories = searcher.get_available_categories()
    
    print("📋 Available Keyword Categories:")
    print("=" * 40)
    for i, category in enumerate(categories, 1):
        print(f"{i:2d}. {category}")
        keywords = searcher.get_category_keywords(category)
        print(f"    Keywords: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
        print()

def show_category_keywords(category: str):
    """Show keywords for a specific category"""
    searcher = KeywordSearcher()
    
    if category not in searcher.get_available_categories():
        print(f"❌ Category '{category}' not found.")
        print(f"Available categories: {', '.join(searcher.get_available_categories())}")
        return
    
    keywords = searcher.get_category_keywords(category)
    print(f"🔑 Keywords in '{category}' category:")
    print("=" * 40)
    for keyword in keywords:
        print(f"• {keyword}")

def main():
    """Main function with command line argument parsing"""
    if len(sys.argv) < 2:
        print("🔍 Keyword Search - Usage Examples:")
        print("=" * 50)
        print("1. Search specific keywords:")
        print("   python search_keywords.py 'age,74,woman'")
        print("   python search_keywords.py 'propofol,drip,mg' --case-sensitive")
        print("   python search_keywords.py 'heart failure' --exact-match")
        print()
        print("2. Search by category:")
        print("   python search_keywords.py --category demographics")
        print("   python search_keywords.py --category medications")
        print("   python search_keywords.py --category diagnoses")
        print()
        print("3. Show available categories:")
        print("   python search_keywords.py --show-categories")
        print()
        print("4. Show keywords in category:")
        print("   python search_keywords.py --show-keywords demographics")
        print()
        print("Available categories: demographics, diagnoses, medications, procedures, complications, outcomes, vital_signs, lab_values")
        return
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if '--show-categories' in args:
        show_categories()
        return
    
    if '--show-keywords' in args:
        try:
            category_index = args.index('--show-keywords') + 1
            if category_index < len(args):
                category = args[category_index]
                show_category_keywords(category)
            else:
                print("❌ Please specify a category name after --show-keywords")
        except (ValueError, IndexError):
            print("❌ Please specify a category name after --show-keywords")
        return
    
    if '--category' in args:
        try:
            category_index = args.index('--category') + 1
            if category_index < len(args):
                category = args[category_index]
                search_category_command(category)
            else:
                print("❌ Please specify a category name after --category")
        except (ValueError, IndexError):
            print("❌ Please specify a category name after --category")
        return
    
    # Search specific keywords
    keywords_str = args[0]
    case_sensitive = '--case-sensitive' in args
    exact_match = '--exact-match' in args
    
    search_keywords_command(keywords_str, case_sensitive, exact_match)

if __name__ == "__main__":
    main()
