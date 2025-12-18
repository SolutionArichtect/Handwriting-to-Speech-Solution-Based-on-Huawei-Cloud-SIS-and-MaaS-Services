import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the local SDK to the python path so imports work
    sdk_path = os.path.join(os.getcwd(), "huaweicloud-python-sdk-sis-1.8.5")
    if os.path.exists(sdk_path):
        sys.path.append(sdk_path)
        print(f"Added SDK to path: {sdk_path}")
    else:
        print(f"Warning: SDK path not found at {sdk_path}")

    # Run the uvicorn server
    # Equivalent to: uvicorn src.main:app --host 127.0.0.1 --port 8000
    print("Starting server at http://127.0.0.1:8000...")
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
