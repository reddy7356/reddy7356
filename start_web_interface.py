#!/usr/bin/env python3
"""
Simple script to start the MIMIC IV Patient Query Web Interface
"""

import subprocess
import sys
import os

def main():
    print("🏥 Starting MIMIC IV Patient Query Web Interface...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('mimic_web_interface.py'):
        print("❌ Error: mimic_web_interface.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if virtual environment exists
    if not os.path.exists('.venv'):
        print("❌ Error: Virtual environment not found!")
        print("Please create a virtual environment first:")
        print("  python -m venv .venv")
        print("  source .venv/bin/activate")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ Virtual environment found")
    print("✅ Web interface script found")
    print()
    print("🚀 Starting web server on port 8080...")
    print("📱 Open your browser and go to: http://localhost:8080")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the web interface
        subprocess.run([sys.executable, 'mimic_web_interface.py'])
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
