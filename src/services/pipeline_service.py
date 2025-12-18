import os
import time
from typing import Optional, Dict
from src.services.agent_client import AgentClient
from src.utils.image_processor import ocr_image_bytes
from src.utils.text_processor import TextProcessor
from src.services.sis_service import SisService
from src.config import Config
from src.utils.versioning import bump_patch, current_version

class PipelineService:
    def __init__(self):
        self.agent = AgentClient()
        self.sis: Optional[SisService] = None

    def _read_prompt(self, path: str) -> str:
        candidates = [path]
        name = os.path.basename(path)
        if name == "prompt_translate.txt":
            candidates.append(os.path.join("reference", "prompt_translate.txt"))
            candidates.append(os.path.join("reference", "prompt_translated.txt"))
        elif name == "prompt_answers.txt":
            candidates.append(os.path.join("reference", "prompt_answers.txt"))
        else:
            candidates.append(os.path.join("reference", name))
        for p in candidates:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                continue
        return ""

    def process(self, image_bytes: bytes, question_id: str, synthesize: bool = True, input_text: str = "") -> Dict:
        print("Step1: OCR start")
        run_ts = int(time.time())
        run_dir = os.path.join(Config.OUTPUT_ROOT, str(run_ts))
        os.makedirs(run_dir, exist_ok=True)
        steps_log_path = os.path.join(run_dir, "steps.log")
        ocr_text = ""
        engine = ""
        if input_text:
            ocr_text = input_text
            engine = "manual"
        else:
            remote_ocr = self.agent.ocr_paddle_vl(image_bytes)
            if remote_ocr:
                ocr_text = remote_ocr
                engine = "PaddleOCR-VL-0.9B"
            else:
                ocr_text, engine = ocr_image_bytes(image_bytes)
                if not ocr_text:
                    return {"status": "error", "message": "OCR failed"}
        print(f"Step1: OCR done using {engine}")
        try:
            with open(os.path.join(run_dir, "1_ocr.txt"), "w", encoding="utf-8") as f:
                f.write(ocr_text)
            with open(steps_log_path, "a", encoding="utf-8") as f:
                f.write(f"Step1 OCR engine: {engine}\n")
        except Exception:
            pass

        print("Step2: Normalize text start")
        normalized = TextProcessor.normalize_math_symbols(ocr_text)
        print("Step2: Normalize text done")
        try:
            with open(os.path.join(run_dir, "2_normalized.txt"), "w", encoding="utf-8") as f:
                f.write(normalized)
            with open(steps_log_path, "a", encoding="utf-8") as f:
                f.write("Step2 normalized written\n")
        except Exception:
            pass

        print("Step3: Answer check start")
        prompt_answers = self._read_prompt("prompt_answers.txt")
        answer_text = self.agent.deepseek_check(normalized, prompt_answers) or normalized
        print("Step3: Answer check done")
        try:
            with open(os.path.join(run_dir, "3_answer.txt"), "w", encoding="utf-8") as f:
                f.write(answer_text)
            with open(steps_log_path, "a", encoding="utf-8") as f:
                f.write("Step3 answer written\n")
        except Exception:
            pass

        print("Step4: Translate to natural language start")
        prompt_translate = self._read_prompt("prompt_translate.txt")
        natural_text = self.agent.deepseek_translate(answer_text, prompt_translate) or answer_text
        print("Step4: Translate to natural language done")
        try:
            with open(os.path.join(run_dir, "4_natural.txt"), "w", encoding="utf-8") as f:
                f.write(natural_text)
            with open(steps_log_path, "a", encoding="utf-8") as f:
                f.write("Step4 natural written\n")
        except Exception:
            pass

        audio_path = ""
        if synthesize:
            print("Step5: Synthesize start")
            if not self.sis:
                self.sis = SisService()
            save_dir = run_dir
            final_filename = "audio.mp3"
            audio_path = os.path.join(save_dir, final_filename)
            chunks = TextProcessor.split_text(natural_text, max_length=450)
            temp_files = []
            for i, chunk in enumerate(chunks):
                temp_path = os.path.join(save_dir, f"audio_part{i}.mp3")
                ok = self.sis.synthesize(chunk, temp_path, "chinese_xiaoyan_common")
                if not ok:
                    return {"status": "error", "message": f"SIS synth failed at chunk {i}"}
                temp_files.append(temp_path)
            with open(audio_path, "wb") as out:
                for t in temp_files:
                    with open(t, "rb") as inp:
                        out.write(inp.read())
            for t in temp_files:
                try:
                    os.remove(t)
                except:
                    pass
            print("Step5: Synthesize done")
            try:
                with open(steps_log_path, "a", encoding="utf-8") as f:
                    f.write(f"Step5 audio saved: {audio_path}\n")
            except Exception:
                pass

        v = bump_patch()
        print(f"Version updated to {v}")
        try:
            with open(steps_log_path, "a", encoding="utf-8") as f:
                f.write(f"Version updated: {v}\n")
        except Exception:
            pass

        return {
            "status": "success",
            "ocr_engine": engine,
            "ocr_text": ocr_text,
            "normalized_text": normalized,
            "answer_text": answer_text,
            "natural_text": natural_text,
            "audio_path": os.path.abspath(audio_path) if audio_path else "",
            "run_dir": os.path.abspath(run_dir)
        }
