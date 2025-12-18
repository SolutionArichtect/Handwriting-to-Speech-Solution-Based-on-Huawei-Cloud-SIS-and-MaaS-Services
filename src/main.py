import os
import time
import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from src.config import Config
from src.utils.text_processor import TextProcessor
from src.services.sis_service import SisService
from src.services.pipeline_service import PipelineService
from fastapi import UploadFile, File, Form, Query
import logging

# Setup logging
logging.basicConfig(filename='log/error_log', level=logging.ERROR)
logger = logging.getLogger("api")
app = FastAPI(title="Math Audio Synthesizer", version="0.0.1")
pipeline_service = PipelineService()

# Models
class SynthesisRequest(BaseModel):
    text: str
    question_id: str
    voice: Optional[str] = "chinese_xiaoyan_common"

class SynthesisResponse(BaseModel):
    status: str
    audio_path: str
    message: Optional[str] = None

class PipelineResponse(BaseModel):
    status: str
    ocr_engine: Optional[str] = None
    ocr_text: Optional[str] = None
    normalized_text: Optional[str] = None
    answer_text: Optional[str] = None
    natural_text: Optional[str] = None
    audio_path: Optional[str] = None
    run_dir: Optional[str] = None

# Service Instance
sis_service = None

@app.on_event("startup")
async def startup_event():
    if not os.path.exists("log"):
        os.makedirs("log")

@app.post("/synthesize", response_model=SynthesisResponse)
async def synthesize_text(request: SynthesisRequest):
    global sis_service
    if not sis_service:
        try:
            sis_service = SisService()
        except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))

    # 1. Normalize Text
    normalized_text = TextProcessor.normalize_math_symbols(request.text)
    
    # 2. Split Text
    chunks = TextProcessor.split_text(normalized_text, max_length=450)
    
    # 3. Prepare Output Path
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = int(time.time())
    save_dir = os.path.join(Config.AUDIO_SAVE_PATH, date_str)
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    final_filename = f"{request.question_id}_{timestamp}.mp3"
    final_path = os.path.join(save_dir, final_filename)
    
    # 4. Synthesize Chunks
    temp_files = []
    try:
        for i, chunk in enumerate(chunks):
            temp_filename = f"{request.question_id}_{timestamp}_part{i}.mp3"
            temp_path = os.path.join(save_dir, temp_filename)
            
            success = sis_service.synthesize(chunk, temp_path, request.voice)
            if not success:
                raise Exception(f"Failed to synthesize chunk {i}")
            
            temp_files.append(temp_path)
            
        # 5. Merge Files (Simple Concatenation for MP3)
        with open(final_path, 'wb') as outfile:
            for temp_file in temp_files:
                with open(temp_file, 'rb') as infile:
                    outfile.write(infile.read())
                    
        # 6. Cleanup Temp Files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass
                
        # Log success
        with open("log/version_log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: Synthesized {request.question_id} successfully.\n")

        return SynthesisResponse(
            status="success",
            audio_path=os.path.abspath(final_path)
        )

    except Exception as e:
        logger.error(f"Synthesis failed for {request.question_id}: {str(e)}")
        # Cleanup potential partial files
        for temp_file in temp_files:
             if os.path.exists(temp_file):
                os.remove(temp_file)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-image", response_model=PipelineResponse)
async def process_image(
    question_id: Optional[str] = Form(None),
    question_id_q: Optional[str] = Query(None),
    file: UploadFile = File(...),
    synthesize: bool = Form(True),
    text: Optional[str] = Form(None)
):
    try:
        content = await file.read()
        qid = question_id or question_id_q
        if not qid:
            raise HTTPException(status_code=422, detail="question_id required")
        result = pipeline_service.process(content, qid, synthesize, input_text=text or "")
        if result.get("status") != "success":
            raise HTTPException(status_code=500, detail=result.get("message", "Pipeline failed"))
        with open("log/version_log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.datetime.now()}: Pipeline processed {qid}.\n")
        return PipelineResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
