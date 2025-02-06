from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter, Depends, status, Query
from typing import Any, List, Optional, Union
from app.services.user import CurrentUserDep
from app.db import SessionDep
from app.services.openai import OpenAIService
import os
from pdfminer.high_level import extract_text


router = APIRouter(tags=["CV Analyzer"], prefix="/cv_analyzer")
openAIService = OpenAIService()

@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload(
    current_user: CurrentUserDep,
    file: UploadFile = File(...)
):
    print('')
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        contents = await file.read()
        with open("temp_cv.pdf", "wb") as f:
            f.write(contents)

        cv_text = extract_text("temp_cv.pdf")
        if not cv_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        # Get OpenAI evaluation
        feedback = await openAIService.assess_application(cv_text)
        return feedback

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.remove("temp_cv.pdf")
