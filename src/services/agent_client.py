import base64
import json
import requests
from typing import Optional
from src.config import Config

class AgentClient:
    def __init__(self):
        self.ocr_url = Config.OCR_VL_URL
        self.maas_url = Config.MAAS_URL_V2
        self.maas_key = Config.MAAS_API_KEY

    def _maas_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.maas_key}"
        }

    def _headers(self):
        return {"Content-Type": "application/json"}

    def ocr_paddle_vl(self, image_bytes: bytes) -> str:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{b64}"
        payload = {
            "model": "PaddleOCR-VL-0.9B",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": data_url}},
                        {"type": "text", "text": "OCR"}
                    ]
                }
            ],
            "temperature": 0.0
        }
        try:
            resp = requests.post(self.ocr_url, headers=self._headers(), data=json.dumps(payload), timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                if "choices" in data and data["choices"]:
                    msg = data["choices"][0].get("message", {})
                    content = msg.get("content")
                    if isinstance(content, list):
                        texts = [c.get("text", "") for c in content if c.get("type") == "text"]
                        return " ".join([t for t in texts if t]).strip()
                    if isinstance(content, str):
                        return content.strip()
                return ""
            return ""
        except Exception:
            return ""

    def deepseek_check(self, text: str, prompt: str) -> str:
        payload = {
            "model": "deepseek-v3.2-exp",
            "messages": [
                {"role": "system", "content": prompt or "You are a helpful assistant."},
                {"role": "user", "content": text}
            ],
            "thinking": {"type": "enabled"}
        }
        try:
            # [SECURITY NOTE] verify=False is used here for development/testing environments where
            # SSL certificates might not be fully configured. For production, it is recommended to
            # enable SSL verification (verify=True) or provide a valid CA bundle.
            resp = requests.post(self.maas_url, headers=self._maas_headers(), data=json.dumps(payload), timeout=60, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                if "choices" in data and data["choices"]:
                    msg = data["choices"][0].get("message", {})
                    content = msg.get("content")
                    if isinstance(content, str):
                        return content.strip()
                    if isinstance(content, list):
                        texts = [c.get("text", "") for c in content if c.get("type") == "text"]
                        return " ".join([t for t in texts if t]).strip()
                return ""
            return ""
        except Exception:
            return ""

    def deepseek_translate(self, text: str, prompt: str) -> str:
        return self.deepseek_check(text, prompt)
