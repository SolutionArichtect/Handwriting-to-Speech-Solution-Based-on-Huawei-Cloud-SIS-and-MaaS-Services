import os
import time
import json
import logging
import importlib
from typing import Optional
from src.config import Config

logger = logging.getLogger(__name__)

class SisService:
    def __init__(self):
        try:
            sis_client_module = importlib.import_module("huaweicloud_sis.client.tts_client")
            bean_req_module = importlib.import_module("huaweicloud_sis.bean.tts_request")
            bean_cfg_module = importlib.import_module("huaweicloud_sis.bean.sis_config")
            exc_module = importlib.import_module("huaweicloud_sis.exception.exceptions")
        except Exception as e:
            logger.error(str(e))
            raise ImportError("huaweicloud_sis SDK not installed")

        self._TtsCustomizationClient = getattr(sis_client_module, "TtsCustomizationClient")
        self._TtsCustomRequest = getattr(bean_req_module, "TtsCustomRequest")
        self._SisConfig = getattr(bean_cfg_module, "SisConfig")
        self._ClientException = getattr(exc_module, "ClientException")
        self._ServerException = getattr(exc_module, "ServerException")

        self.ak = Config.HUAWEI_AK
        self.sk = Config.HUAWEI_SK
        self.region = Config.REGION
        self.project_id = Config.PROJECT_ID
        
        if not self.ak or not self.sk or not self.region:
            logger.error("Huawei Cloud credentials missing!")
            raise ValueError("Huawei Cloud credentials missing")

        self.config = self._SisConfig()
        self.config.set_connect_timeout(10)
        self.config.set_read_timeout(10)
        
        self.client = self._TtsCustomizationClient(
            self.ak, self.sk, self.region, self.project_id, sis_config=self.config
        )

    def synthesize(self, text: str, output_path: str, voice: str = 'chinese_xiaoyan_common') -> bool:
        try:
            ttsc_request = self._TtsCustomRequest(text)
            ttsc_request.set_property(voice)
            ttsc_request.set_audio_format('mp3')
            ttsc_request.set_sample_rate('16000')
            ttsc_request.set_volume(50)
            ttsc_request.set_pitch(0)
            ttsc_request.set_speed(0)
            ttsc_request.set_saved(True)
            ttsc_request.set_saved_path(output_path)

            for attempt in range(3):
                try:
                    result = self.client.get_ttsc_response(ttsc_request)
                    logger.info(f"Synthesis successful for {output_path}")
                    return True
                except (self._ClientException, self._ServerException) as e:
                    logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
                    if attempt == 0 and self.region == "cn-east-3":
                        self.region = "cn-north-4"
                        self.client = self._TtsCustomizationClient(
                            self.ak, self.sk, self.region, self.project_id, sis_config=self.config
                        )
                    if attempt == 2:
                        raise e
                    time.sleep(1)
            
            return False

        except Exception as e:
            logger.error(f"Error during synthesis: {str(e)}")
            return False
