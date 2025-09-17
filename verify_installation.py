#!/usr/bin/env python3
"""
Verification script to check that all Haystack 2.x dependencies are properly installed.
"""

def verify_imports():
    """Verify that all required imports work correctly."""
    print("🔍 Verifying imports...")
    
    try:
        from datasets import load_dataset
        print("✅ datasets imported successfully")
    except ImportError as e:
        print(f"❌ datasets import failed: {e}")
        return False
    
    try:
        from haystack import Document, Pipeline
        print("✅ haystack core imports successful")
    except ImportError as e:
        print(f"❌ haystack core imports failed: {e}")
        return False
    
    try:
        from haystack.core.component import component
        print("✅ haystack component decorator imported")
    except ImportError as e:
        print(f"❌ haystack component import failed: {e}")
        return False
    
    try:
        from haystack.core.component.types import InputSocket, OutputSocket
        print("✅ haystack component types imported")
    except ImportError as e:
        print(f"❌ haystack component types import failed: {e}")
        return False
    
    return True

def verify_functionality():
    """Verify that basic functionality works."""
    print("\n🔍 Verifying functionality...")
    
    try:
        from haystack import Document, Pipeline
        from haystack.core.component import component
        from typing import List
        
        # Test Document creation
        doc = Document(content="Test document")
        print("✅ Document creation works")
        
        # Test Pipeline creation
        pipeline = Pipeline()
        print("✅ Pipeline creation works")
        
        # Test custom component creation
        @component
        class TestComponent:
            def __init__(self):
                pass
            
            @component.output_types(result=str)
            def run(self, input_text: str):
                return {"result": f"Processed: {input_text}"}
        
        test_comp = TestComponent()
        print("✅ Custom component creation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def check_versions():
    """Check installed package versions."""
    print("\n📦 Checking package versions...")
    
    try:
        import haystack
        print(f"✅ Haystack version: {haystack.__version__}")
    except Exception as e:
        print(f"❌ Could not get Haystack version: {e}")
    
    try:
        import datasets
        print(f"✅ Datasets version: {datasets.__version__}")
    except Exception as e:
        print(f"❌ Could not get Datasets version: {e}")

def main():
    """Main verification function."""
    print("🚀 Haystack 2.x Installation Verification")
    print("=" * 50)
    
    # Check versions
    check_versions()
    
    # Verify imports
    imports_ok = verify_imports()
    
    # Verify functionality
    functionality_ok = verify_functionality()
    
    print("\n" + "=" * 50)
    if imports_ok and functionality_ok:
        print("🎉 All verifications passed! Your Haystack 2.x installation is working correctly.")
        print("\nYou can now run: python main.py")
    else:
        print("❌ Some verifications failed. Please check your installation.")
        print("\nTry running: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
