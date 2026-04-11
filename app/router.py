from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from service import process_image

router = APIRouter()

@router.post("/process")
async def process(
    file: UploadFile = File(...),
    threshold1: int = Form(...),
    threshold2: int = Form(...),
    blur: int = Form(...),
    thickness: int = Form(...),
    min_area: int = Form(...),
    color: str = Form(...),
    mode: str = Form(...),
):
    result = await process_image(
        file=file,
        threshold1=threshold1,
        threshold2=threshold2,
        blur=blur,
        thickness=thickness,
        min_area=min_area,
        color=color,
        mode=mode,
    )
    return StreamingResponse(result, media_type="image/png")
