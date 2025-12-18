import requests
import os

def run_test():
    url = "http://127.0.0.1:8000/process-image"
    img_path = os.path.join("data", "3.png")
    if not os.path.exists(img_path):
        candidates = [
            os.path.join("data", "1.jpg"),
            os.path.join("data", "2.jpg"),
        ]
        img_path = next((p for p in candidates if os.path.exists(p)), None)
    if not img_path:
        print("no image found in data/")
        return
    print("Image:", img_path)
    files = {"file": open(img_path, "rb")}
    data = {"question_id": "pipe_001", "synthesize": "true"}
    
    try:
        resp = requests.post(url, files=files, data=data, timeout=300)
        print("Status:", resp.status_code)
        print("Body:", resp.text)
    except Exception as e:
        print("Failed:", str(e))

if __name__ == "__main__":
    run_test()
