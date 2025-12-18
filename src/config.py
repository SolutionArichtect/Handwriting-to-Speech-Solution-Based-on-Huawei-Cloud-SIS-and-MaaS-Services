import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if exists
load_dotenv()

class Config:
    HUAWEI_AK: str = ""
    HUAWEI_SK: str = ""
    REGION: str = ""
    PROJECT_ID: str = ""
    MAAS_API_KEY: str = ""
    MAAS_URL_V2: str = "https://api.modelarts-maas.com/v2/chat/completions"
    OCR_VL_URL: str = "http://1.95.143.9:8080/v1/chat/completions"
    
    # Audio settings
    AUDIO_SAVE_PATH: str = "./audio_output"
    OUTPUT_ROOT: str = "./output"
    
    @classmethod
    def load_config(cls):
        # 1. Try environment variables first
        cls.HUAWEI_AK = os.getenv("HUAWEICLOUD_SIS_AK", "")
        cls.HUAWEI_SK = os.getenv("HUAWEICLOUD_SIS_SK", "")
        cls.REGION = os.getenv("HUAWEICLOUD_REGION", "")
        cls.PROJECT_ID = os.getenv("HUAWEICLOUD_PROJECT_ID", "")
        cls.MAAS_API_KEY = os.getenv("MAAS_API_KEY", "")
        
        # 2. If not found, try reading key.txt
        # We assume key.txt is in the project root (CWD)
        if not (cls.HUAWEI_AK and cls.HUAWEI_SK and cls.REGION):
            try:
                key_candidates = [
                    "key.txt",
                    "../key.txt",
                    "reference/key.txt",
                    "../reference/key.txt",
                ]
                key_path = None
                for p in key_candidates:
                    if os.path.exists(p):
                        key_path = p
                        break
                if not key_path:
                    raise FileNotFoundError("key.txt not found")
                with open(key_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or ":" not in line:
                            continue
                        
                        key, value = line.split(":", 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == "huawei_ak":
                            cls.HUAWEI_AK = value
                        elif key == "huawei_sk":
                            cls.HUAWEI_SK = value
                        elif key == "region":
                            cls.REGION = value
                        elif key == "project_id":
                            cls.PROJECT_ID = value
                        elif key.upper() == "MAAS":
                            cls.MAAS_API_KEY = value
                            
            except FileNotFoundError:
                print("Warning: key.txt not found and env vars not set.")
                
        # Create output directory
        for p in [cls.AUDIO_SAVE_PATH, cls.OUTPUT_ROOT]:
            if not os.path.exists(p):
                os.makedirs(p)

# Initialize config
Config.load_config()
