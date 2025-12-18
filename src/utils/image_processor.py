import os
import io
from typing import Optional, Tuple

def ocr_image_bytes(image_bytes: bytes) -> Tuple[str, str]:
    text = ""
    engine = ""
    try:
        try:
            from rapidocr import RapidOCR
            ocr = RapidOCR()
            result, _ = ocr(io.BytesIO(image_bytes))
            if result:
                text = " ".join([item[1] for item in result])
            engine = "RapidOCR"
        except Exception:
            try:
                from rapidocr_onnxruntime import RapidOCR
                ocr = RapidOCR()
                result, _ = ocr(io.BytesIO(image_bytes))
                if result:
                    text = " ".join([item[1] for item in result])
                engine = "RapidOCR-ONNX"
            except Exception:
                try:
                    import pytesseract
                    from PIL import Image
                    image = Image.open(io.BytesIO(image_bytes))
                    text = pytesseract.image_to_string(image)
                    engine = "pytesseract"
                except Exception:
                    pass
    except Exception:
        pass
    return text.strip(), engine
