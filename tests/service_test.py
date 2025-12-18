import json
import requests
import time

def run_test():
    url = "http://127.0.0.1:8000/synthesize"
    payload = {
        "text": "已知函数 f(x)=x^2，当x等于2时，函数值为4。",
        "question_id": f"svc_{int(time.time())}",
        "voice": "chinese_xiaoyan_common"
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        print("Status:", resp.status_code)
        print("Body:", resp.text)
    except Exception as e:
        print("Request failed:", str(e))

if __name__ == "__main__":
    run_test()
