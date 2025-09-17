#!/usr/bin/env python3
"""
MIMIC IV Patient Query System - Main Launcher
Provides easy access to all system components
"""

import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='MIMIC IV Patient Query System Launcher')
    parser.add_argument('mode', choices=['cli', 'web', 'examples', 'interactive'], 
                       help='Mode to run: cli, web, examples, or interactive')
    parser.add_argument('--query', '-q', help='Search query (for CLI mode)')
    parser.add_argument('--patients', '-p', help='Comma-separated patient IDs')
    parser.add_argument('--max-results', '-m', type=int, default=10, help='Maximum results')
    
    args = parser.parse_args()
    
    if args.mode == 'cli':
        if args.query:
            cmd = ['python', 'mimic_query_cli.py', args.query]
            if args.patients:
                cmd.extend(['--patients', args.patients])
            if args.max_results:
                cmd.extend(['--max-results', str(args.max_results)])
            subprocess.run(cmd)
        else:
            print("CLI mode requires a query. Use --query or run examples/interactive mode.")
            print("Example: python run_mimic_system.py cli --query 'diabetes'")
    
    elif args.mode == 'web':
        print("Starting web interface...")
        print("Open your browser to: http://localhost:5000")
        subprocess.run(['python', 'mimic_web_interface.py'])
    
    elif args.mode == 'examples':
        subprocess.run(['python', 'mimic_examples.py'])
    
    elif args.mode == 'interactive':
        subprocess.run(['python', 'mimic_query_cli.py', '--interactive'])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🏥 MIMIC IV Patient Query System")
        print("=" * 50)
        print("Available modes:")
        print("  cli         - Command line interface")
        print("  web         - Web browser interface")
        print("  examples    - Run example queries")
        print("  interactive - Interactive command line")
        print()
        print("Examples:")
        print("  python run_mimic_system.py cli --query 'diabetes'")
        print("  python run_mimic_system.py web")
        print("  python run_mimic_system.py examples")
        print("  python run_mimic_system.py interactive")
        print()
        print("For help with specific modes:")
        print("  python run_mimic_system.py cli --help")
    else:
        main()
