import os
import tempfile

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional

from app.services.pipeline_service import run_pipeline

router = APIRouter()


@router.post("/analyze")
async def analyze(
    input_type: str = Form(...),
    text: str = Form(""),
    url: str = Form(""),
    file: Optional[UploadFile] = File(None)
):
    image_path = None

    if input_type == "screenshot":
        if file is None:
            raise HTTPException(
                status_code=400,
                detail="Screenshot file is required"
            )

        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            temp_file.write(await file.read())
            image_path = temp_file.name

    try:
        result = run_pipeline(
            input_type=input_type,
            text=text,
            image_path=image_path,
            url=url
        )

        return result

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)