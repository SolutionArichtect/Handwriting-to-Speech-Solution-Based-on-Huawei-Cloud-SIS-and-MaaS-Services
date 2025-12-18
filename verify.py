import os
import sys

# Add current directory to path so we can import src
sys.path.append(os.getcwd())

from src.config import Config
from src.utils.text_processor import TextProcessor

def test_config():
    print("Testing Config...")
    try:
        Config.load_config()
        print(f"AK: {'*' * 5}{Config.HUAWEI_AK[-4:] if Config.HUAWEI_AK else 'Not Found'}")
        print(f"Region: {Config.REGION}")
        print(f"Project ID: {Config.PROJECT_ID}")
        print("Config test passed.")
    except Exception as e:
        print(f"Config test failed: {e}")

def test_text_processor():
    print("\nTesting Text Processor...")
    input_text = "f(x) = x^2 + √4"
    expected = "f(x) = x平方 + 根号4"
    result = TextProcessor.normalize_math_symbols(input_text)
    print(f"Input: {input_text}")
    print(f"Output: {result}")
    
    if "平方" in result and "根号" in result:
        print("Text Processor test passed.")
    else:
        print("Text Processor test failed.")

def test_imports():
    print("\nTesting Imports...")
    try:
        from src.services.sis_service import SisService
        print("SisService imported successfully.")
        import fastapi
        print("fastapi imported successfully.")
    except ImportError as e:
        print(f"Import failed: {e}")

if __name__ == "__main__":
    test_config()
    test_text_processor()
    test_imports()
